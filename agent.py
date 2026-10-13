"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
import trace
import mcp_client
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    import re

    session = new_session(query, wardrobe)

    def money(value: float) -> str:
        return f"${value:.0f}" if float(value).is_integer() else f"${value:.2f}"

    # ── parse (regex) ──
    # Price: "under $30", "below 30", "max $25.50", or a bare "$30".
    # Size:  "size M", "size S/M", "size US 9", "size W30".
    # Whatever is left over is the description.
    text = query
    max_price = None
    price_match = re.search(
        r"(?:under|below|less than|max|up to)\s*\$?\s*(\d+(?:\.\d+)?)|\$\s*(\d+(?:\.\d+)?)",
        text, re.I,
    )
    if price_match:
        max_price = float(price_match.group(1) or price_match.group(2))
        text = text.replace(price_match.group(0), " ")

    size = None
    size_match = re.search(
        r"\bsize\s+((?:us|w)\s*\d+(?:\.\d+)?|[a-z0-9]+(?:/[a-z0-9]+)?)",
        text, re.I,
    )
    if size_match:
        size = size_match.group(1).upper()
        text = text.replace(size_match.group(0), " ")

    description = " ".join(re.sub(r"[^\w\s'-]", " ", text).split())
    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    # ── loop ──
    # Each pass runs one step and decides the next one from what it returned.
    count = 0
    next_step = "search"
    while next_step != "done":
        count += 1
        trace.check_iterations(count)

        if next_step == "search":
            parsed = session["parsed"]
            session["search_results"] = mcp_client.call_tool("search_listings", {
                "description": parsed["description"],
                "size": parsed["size"],
                "max_price": parsed["max_price"],
            })
            trace.step(
                "search_listings (via MCP)",
                inputs=parsed,
                returned=session["search_results"],
            )

            # THE BRANCH: nothing found means stop here and say what to change.
            if not session["search_results"]:
                if not parsed["description"]:
                    session["error"] = (
                        f"I couldn't tell what item you want from '{session['query']}'. "
                        f"Describe the piece, like 'vintage graphic tee' or 'black boots'."
                    )
                else:
                    searched = f"Nothing matched '{parsed['description']}'"
                    fixes = []
                    if parsed["size"]:
                        searched += f" in size {parsed['size']}"
                        fixes.append("dropping the size")
                    if parsed["max_price"] is not None:
                        searched += f" under {money(parsed['max_price'])}"
                        fixes.insert(0, f"raising your price limit above {money(parsed['max_price'])}")
                    fixes.append("using broader words (like 'top', 'jeans', or 'jacket')")
                    if len(fixes) > 1:
                        fix_text = ", ".join(fixes[:-1]) + ", or " + fixes[-1]
                    else:
                        fix_text = fixes[0]
                    session["error"] = f"{searched}. Try {fix_text}."
                next_step = "done"
            else:
                session["selected_item"] = session["search_results"][0]
                next_step = "suggest"

        elif next_step == "suggest":
            session["outfit_suggestion"] = suggest_outfit(
                session["selected_item"], session["wardrobe"]
            )
            trace.step(
                "suggest_outfit",
                inputs=session["selected_item"],
                returned=session["outfit_suggestion"],
            )
            if session["outfit_suggestion"].startswith("Couldn't get outfit suggestions"):
                session["error"] = session["outfit_suggestion"]
                next_step = "done"
            else:
                next_step = "card"

        elif next_step == "card":
            session["fit_card"] = create_fit_card(
                session["outfit_suggestion"], session["selected_item"]
            )
            trace.step(
                "create_fit_card",
                inputs=session["selected_item"],
                returned=session["fit_card"],
            )
            if session["fit_card"].startswith("Couldn't write a fit card"):
                session["error"] = session["fit_card"]
                session["fit_card"] = None
            next_step = "done"

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )

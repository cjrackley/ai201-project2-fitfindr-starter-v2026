"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    import re

    def tokens(text: str) -> list[str]:
        return re.findall(r"[a-z0-9.]+", text.lower())

    # Filler words that would otherwise match listing descriptions and inflate
    # scores. Pure numbers are dropped too, so "$30" in a query isn't a keyword.
    stopwords = {
        "a", "an", "the", "and", "or", "for", "with", "in", "of", "to", "on",
        "under", "over", "below", "above", "less", "than", "max", "size",
        "i", "me", "my", "want", "need", "looking", "some", "something",
    }
    keywords = {
        w for w in tokens(description or "")
        if w not in stopwords and not re.fullmatch(r"[\d.]+", w)
    }
    if not keywords:
        return []

    # Size matches on whole tokens, so "M" matches "S/M" and "M/L" but not
    # "XL", and "9" matches "US 9" but not "US 8.5".
    size_tokens = set(tokens(size)) if size else set()

    scored = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size_tokens and not size_tokens <= set(tokens(listing["size"])):
            continue

        text = " ".join([
            listing["title"],
            listing["description"],
            listing["category"],
            " ".join(listing["style_tags"]),
            " ".join(listing["colors"]),
            listing["brand"] or "",
        ])
        score = len(keywords & set(tokens(text)))
        if score > 0:
            scored.append((score, listing))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    from generate import ModelUnavailable

    item_text = (
        f"{new_item.get('title', 'Unnamed item')} "
        f"({new_item.get('category', 'unknown category')}). "
        f"Colors: {', '.join(new_item.get('colors') or []) or 'not listed'}. "
        f"Style: {', '.join(new_item.get('style_tags') or []) or 'not listed'}. "
        f"Description: {new_item.get('description') or 'none'}"
    )

    # A missing wardrobe or missing 'items' key takes the empty-wardrobe path.
    items = (wardrobe or {}).get("items") or []

    if not items:
        system = (
            "You are a thrift stylist. The user owns no wardrobe items yet. "
            "Give general styling advice for the item in 1-2 sentences only. "
            "Talk only about styling this item. Do not mention any specific "
            "pieces the user owns."
        )
        prompt = f"Item:\n{item_text}"
        fallback = (
            f"Style the {new_item.get('title', 'item')} with simple basics in "
            f"neutral colors so it stays the focus of the outfit."
        )
    else:
        wardrobe_lines = []
        for piece in items:
            line = (
                f"- {piece.get('name', 'Unnamed piece')} "
                f"({piece.get('category', 'unknown')}; "
                f"colors: {', '.join(piece.get('colors') or []) or 'not listed'}; "
                f"style: {', '.join(piece.get('style_tags') or []) or 'not listed'})"
            )
            if piece.get("notes"):
                line += f" Notes: {piece['notes']}"
            wardrobe_lines.append(line)

        system = (
            "You are a thrift stylist. Suggest exactly two outfits that pair "
            "the new item with pieces from the user's wardrobe. Label them "
            "'Outfit 1:' and 'Outfit 2:'. Each outfit is 1-2 sentences and "
            "names the wardrobe pieces it uses exactly as they appear in the "
            "wardrobe list. Use only pieces from that list."
        )
        prompt = (
            f"New item:\n{item_text}\n\n"
            f"Wardrobe:\n" + "\n".join(wardrobe_lines)
        )
        fallback = (
            f"Outfit 1: Pair the {new_item.get('title', 'item')} with "
            f"{items[0].get('name', 'a basic from your wardrobe')}."
        )

    try:
        response = generate(prompt, system=system)
    except ModelUnavailable as exc:
        return f"Couldn't get outfit suggestions right now. {exc}"

    return response.strip() or fallback


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    from generate import ModelUnavailable

    title = new_item.get("title", "this item")

    if not outfit or not outfit.strip():
        return f"No outfit was provided for {title}, so there's no fit card to write."

    # Whole-dollar prices read as "$34", others as "$34.50", so the caption and
    # a string check in unit 4 agree on how the price is written.
    price = new_item.get("price")
    if isinstance(price, (int, float)):
        price_text = f"${price:.0f}" if float(price).is_integer() else f"${price:.2f}"
    else:
        price_text = "an unlisted price"
    platform = new_item.get("platform") or "a thrift app"
    colors = ", ".join(new_item.get("colors") or []) or "not listed"

    system = (
        "You write short social media captions about thrift finds. Write 2-4 "
        "plain sentences that read like a real post, not a product "
        "description. Mention the item's title, its price, and the platform "
        "exactly once each, writing the price exactly as given. Mention at "
        "least one of the item's colors. Be specific about the vibe of the "
        "outfit. No emojis and no hashtags."
    )
    prompt = (
        f"Item: {title}\n"
        f"Price: {price_text}\n"
        f"Platform: {platform}\n"
        f"Colors: {colors}\n"
        f"Style: {', '.join(new_item.get('style_tags') or []) or 'not listed'}\n"
        f"Description: {new_item.get('description') or 'none'}\n\n"
        f"Outfit:\n{outfit.strip()}"
    )

    try:
        response = generate(prompt, system=system)
    except ModelUnavailable as exc:
        return f"Couldn't write a fit card right now. {exc}"

    fallback = f"Found the {title} for {price_text} on {platform} and it's already in rotation."
    return response.strip() or fallback

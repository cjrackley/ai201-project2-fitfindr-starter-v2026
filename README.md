# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

This project allows a user to search through a wardrobe with clothes in it. The user can ask for a number of things, an the agent sorts out the details and runs them through tools that output a few different things. It first finds the most relevent piece of clothing relating to the users' query, then it will give outfit advice followed by a small caption style paragraph detailing the item. 

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the wardrobe_schema based on the input provided
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" --> 'description' (string), 'size' (string), 'max_price' (float), all optional inputs so all 3 are not needed.
- **Returns:** list[dict] with possible listing data inside including id, name, category, colors, styletags and notes
- **When it has nothing:** Returns an empty list

### `suggest_outfit`

- **What it does:** suggests outfits based on a new item and current wardrobe
- **Inputs:** 'new_item'(dict), 'wardrobe' (dict)
- **Returns:** A string with outfit suggestions
- **When it has nothing:** Returns general styling advice if no inputs are given

### `create_fit_card`

- **What it does:** Gives a caption that reads like a social media post caption.
- **Inputs:** 'outfit' (string), 'new_item'(dict)
- **Returns:** A String containing a 2-4 sentence caption.
- **When it has nothing:** returns a descriptive message if no outfit is given.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
" If search_listing returns an empty list, a message is placed in session["error"], not a "no results" message. It then returns the session and does not run suggest_outfit. If a list is found, take the first dictionary entry and go to the suggest_outfit session.
**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. A price after "under", "below", "max", "up to", or a bare "$30" becomes `max_price`. "size M", "size S/M", "size US 9", or "size W30" becomes `size`. Whatever is left becomes `description`.

**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` → `selected_item` (first result) → `outfit_suggestion` → `fit_card`. `wardrobe` is set at the start. `error` is set only when the run stops early, and then the later fields stay `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'python app.py ask "purple top under $50"

```


  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit 1: Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash and chunky white sneakers for a casual streetwear look.

Outfit 2: Style the Y2K Baby Tee — Butterfly Print with wide-leg khaki trousers, brown leather belt, and black combat boots for an edgy earth-toned vibe.

  Fit card: I just scored this Y2K Baby Tee — Butterfly Print on depop for $18 and I am obsessed with the white and pink graphic. I styled it with baggy dark wash straight-leg jeans and chunky white sneakers for a casual streetwear look. It has the best fitted crop length and fits like an absolute dream.

0 model calls this session, 2 served from cache



**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```
$ from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))

```
Outfit 1: Pair the Vintage Levi's 501 Jeans — Medium Wash with the White ribbed tank top, Black cropped zip hoodie, and Chunky white sneakers for a classic streetwear look.

Outfit 2: Style the Vintage Levi's 501 Jeans — Medium Wash using the Oversized grey crew
```
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```
Scored these blue Vintage Levi's 501 Jeans on depop for $38 and I am obsessed. The light fading at the knees gives them that perfect lived-in feel without any actual wear and tear. I threw them on with my favorite white sneakers for a chill weekend streetwear vibe.
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* When finishing my criteria, I asked claude to find ways it can be tightend and if certain things stated couldn't be tested.
- *What came back:* It told me I needed to tighten the state criteria and make it less vague
- *What I changed:* I changed the criteria from tracking output/input to just tracking if the id is carried from one tool to another.

**Moment 2**

- *What I asked for:* I instructed claude to build the 3 tools within tools.py. Making sure to not allow any editting outside of the file and keeping within the scope of the instructions already within the codeblocks.
- *What came back:* It gave me the code needed to run the tools effectively
- *What I changed:* Before completing the code, it asked me to clarify on some things. I made sure that the outfit suggestions would give 2 outfits instead of allowing the model to decide. I also changed how it would handle inputs, instead of trusting that there would always be a non-empty input, it treats missing as an empty wardrobe.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS |FAIL | MET(4/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. selected item carries into suggest_outfit | 5 of 5 | FAIL | PASS | PASS | PASS | PASS | FAIL(4/5) |
| 4. fit card quality | 4 of 5 | FAIL | PASS | PASS | FAIL | PASS | FAIL(3/5) |
| 5. empty wardrobe card complete | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Critera 1 Try**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Outfit 1: Balance the Y2K butterfly baby tee with Baggy straight-leg jeans, dark wash and Chunky white sneakers for a classic streetwear silhouette.

Outfit 2: Layer the baby tee under the Vintage black denim jacket and pair it with Wide-leg khaki trousers and Black combat boots for an edgy, contrasting look.
```

Fit card:

```
I just scored this Y2K Baby Tee with Butterfly Print on depop for $18. The white, pink, and purple shades make it super easy to style. I am pairing it with baggy straight-leg jeans and chunky white sneakers for a classic streetwear silhouette.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1: Balance the Y2K butterfly baby tee with Baggy straight-leg jeans, dark wash and Chunky white sneaker…
[3] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: I just scored this Y2K Baby Tee with Butterfly Print on depop for $18. The white, pink, and purple shades make…
```

**Criteria 2 Try**

- stopped early: yes — Nothing matched 'designer ballgown' in size XXS under $5. Try raising your price limit above $5, dropping the size, or using broader words (like 'top', 'jeans', or 'jacket').
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
```
**Criteria 3 Try**

- stopped early: yes — Couldn't get outfit suggestions right now. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}
- selected_item: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
- search_results: 10

Outfit suggestion:

```
Couldn't get outfit suggestions right now. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: 90s Track Jacket — Navy/White Stripe, Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash … +7 more
[2] suggest_outfit
      in:  90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      out: Couldn't get outfit suggestions right now. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, …
```
**Criteria 4 Try**

- stopped early: no
- selected_item: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
- search_results: 2

Outfit suggestion:

```
Outfit 1: Layer the White ribbed tank top underneath the 90s Silk Slip Dress for a casual 90s streetwear vibe, paired with the Chunky white sneakers.

Outfit 2: Throw the Oversized grey crewneck sweatshirt right over the 90s Silk Slip Dress to give the feminine slip a cozy texture contrast, finished with the Black combat boots.
```

Fit card:

```
Scored this ivory 90s Silk Slip Dress on depop for $30 and it has the prettiest dusty pink and green floral print. I layered a white ribbed tank underneath and threw on some chunky sneakers for that effortless 90s streetwear look. It is giving major cozy cottagecore vibes without trying too hard.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 2 items: 90s Silk Slip Dress — Floral, Midi Length, Silk Button-Down — Sage Green
[2] suggest_outfit
      in:  90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
      out: Outfit 1: Layer the White ribbed tank top underneath the 90s Silk Slip Dress for a casual 90s streetwear vibe,…
[3] create_fit_card
      in:  90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
      out: Scored this ivory 90s Silk Slip Dress on depop for $30 and it has the prettiest dusty pink and green floral pr…
```

**Criteria 5 Try**

- stopped early: no
- selected_item: Corduroy Wide-Leg Pants — Rust ($32.0, depop)
- search_results: 2

Outfit suggestion:

```
Anchor the rich, earthy hue of these high-waisted cords with a tucked-in cream lace blouse and chunky wooden-soled clogs for an effortless 1970s aesthetic. Layer with a fitted knit turtleneck and a cropped corduroy jacket in an olive or mustard tone to play up the autumnal cottagecore texture.
```

Fit card:

```
I finally tracked down these Corduroy Wide-Leg Pants over on depop for $32. The gorgeous rust shade brings the ultimate 1970s aesthetic to life, especially when I pair them with a cream lace blouse and chunky clogs. It is the kind of earthy, textured look I live for all autumn long.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 2 items: Corduroy Wide-Leg Pants — Rust, Low-Rise Cargo Pants — Khaki
[2] suggest_outfit
      in:  Corduroy Wide-Leg Pants — Rust ($32.0, depop)
      out: Anchor the rich, earthy hue of these high-waisted cords with a tucked-in cream lace blouse and chunky wooden-s…
[3] create_fit_card
      in:  Corduroy Wide-Leg Pants — Rust ($32.0, depop)
      out: I finally tracked down these Corduroy Wide-Leg Pants over on depop for $32. The gorgeous rust shade brings the…
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | Met target |
| 2. impossible query stops early | 5 of 5 | PASS | Met target |
| 3. selected item carries into suggest_outfit | 5 of 5 | FAIL | Failed 1 try |
| 4. fit card quality | 4 of 5 | FAIL | Failed 2 tries |
| 5. empty wardrobe card complete | 5 of 5 | PASS | Met target |

**Diagnoses**

All tries that failed occured entirely because the model was delaying the calls due to activity. The 2nd and 3rd tools failed during the delays.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 5 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +2 more
[2] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Outfit 1: Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash and chunky white sn…
[3] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: I just scored this Y2K Baby Tee — Butterfly Print on depop for $18 and I am obsessed with the white and pink g…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Outfit 1: Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash and chunky white sneakers for a casual streetwear look.

Outfit 2: Style the Y2K Baby Tee — Butterfly Print with wide-leg khaki trousers, brown leather belt, and black combat boots for an edgy earth-toned vibe.

  Fit card: I just scored this Y2K Baby Tee — Butterfly Print on depop for $18 and I am obsessed with the white and pink graphic. I styled it with baggy dark wash straight-leg jeans and chunky white sneakers for a casual streetwear look. It has the best fitted crop length and fits like an absolute dream.

0 model calls this session, 2 served from cache
```

**Empty search**

```
(running with an empty wardrobe)
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)

  I couldn't tell what item you want from '...'. Describe the piece, like 'vintage graphic tee' or 'black boots'.

0 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything behaved differently afterwards. If the rewire didn't work, say exactly where it broke — the error text and the last thing that worked. That earns the point in full. -->

The parameter section of the direct call for search_listings had to be tweaked slightly so the system could understand the inputs, otherwise everything worked as intended.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Criterion 3: state. Several listings match this query (lst_004, lst_007,
        # lst_010, ...), so if the wrong one gets passed along, the ids won't match.
        # Check: session["selected_item"]["id"] == the id that reached suggest_outfit.
        "name": "selected item carries into suggest_outfit",
        "query": "vintage jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: fit card. Same item every run (lst_013) so the 5 cards can be
        # compared. It has 3 colors and no brand, so it's harder to describe.
        # Check: under 4 sentences, mentions name, price ($30) and a color.
        "name": "fit card quality",
        "query": "silk slip dress",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5: empty wardrobe. This branch uses a different prompt.
        # lst_005 has no brand, which is a common way for the card to fail.
        # Check: card is non-empty and mentions name, price ($32) and color (rust).
        "name": "empty wardrobe card complete",
        "query": "corduroy pants under $40",
        "wardrobe": "empty",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems

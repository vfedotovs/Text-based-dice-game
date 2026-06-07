# Issue #4 — Implement the lower-section scoring

> **FEAT: implement lower section score part**
>
> - 3 of a Kind: 3 dice of the same number. Score = sum of all 5 dice.
> - 4 of a Kind: 4 dice of the same number. Score = sum of all 5 dice.
> - Full House: any 3-of-a-kind combined with a pair. Score: 25 points.
> - Small Straight: any 4 consecutive numbers (e.g. 1-2-3-4). Score: 30 points.
> - Large Straight: any 5 consecutive numbers (e.g. 1-2-3-4-5). Score: 40 points.
> - Yahtzee: 5 of a kind. Score: 50 points.
> - Chance: any combination of dice. Score = sum of all 5 dice.

This adds the seven Yahtzee lower-section categories. Unlike the upper section
(which counts a single face), each lower category scores the **whole 5-dice
hand** based on a pattern. This document is the **plan only — no code yet**.

---

## 1. Current state

`src/dice_game/scoring.py` models the game as the upper section only:

- `CATEGORIES` — the six upper categories (`ones`–`sixes`).
- `_FACE_OF` — maps each category to the die face it counts.
- `score_category(category, dice)` — `sum(v for v in dice if v == face)`,
  i.e. it *assumes* every category is a face-count. Lower categories don't fit.
- `new_score_table()` — `dict.fromkeys(CATEGORIES, 0)`; every value is `int`.
- `total_score(table)` — sums the table.

`src/dice_game/cli.py`:

- `prompt_save_category` computes available categories as
  `[c for c in CATEGORIES if table[c] == 0]`.
- `print_score_table` lists every category/value.
- `main` loops **once per category** (today: 6 turns).

Two structural assumptions block the lower section and must be addressed:

1. **Scoring is face-based.** `score_category` only knows how to count a face.
   Lower categories need per-category *pattern* scorers over the full hand.
2. **`0` means "unfilled".** `prompt_save_category` treats `table[c] == 0` as
   "still available". In the lower section a legitimately scored category is
   frequently **0** (e.g. declaring Yahtzee with no five-of-a-kind, or dumping a
   bad roll into Full House). With the current sentinel, a category scored at 0
   would be wrongly offered again, and the game-length loop would break. We need
   to distinguish *unfilled* from *filled-with-0*.

## 2. Interaction with issue #7 (PR #8, not yet merged)

PR #8 (upper-section bonus) adds `upper_section_subtotal` as
`sum(table[c] for c in CATEGORIES)`. **Once lower categories join `CATEGORIES`,
that subtotal would wrongly include them and inflate the bonus.** So this work
must:

- Split categories into `UPPER_CATEGORIES` + `LOWER_CATEGORIES`, with
  `CATEGORIES = UPPER_CATEGORIES + LOWER_CATEGORIES`.
- Change the bonus subtotal to iterate `UPPER_CATEGORIES` only.

**Recommended ordering:** merge PR #8 first, then branch this work off `main`
and adjust `upper_section_subtotal` as part of it. The plan below assumes #8 is
in place; if it isn't yet, the bonus touch-points simply don't exist and can be
skipped.

## 3. Design

### 3.1 Category groups (`scoring.py`)

```python
UPPER_CATEGORIES = ("ones", "twos", "threes", "fours", "fives", "sixes")
LOWER_CATEGORIES = (
    "three_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "small_straight",
    "large_straight",
    "yahtzee",
    "chance",
)
CATEGORIES = UPPER_CATEGORIES + LOWER_CATEGORIES
```

Keep names as `snake_case` identifiers (consistent with the existing lowercase
keys and usable directly at the prompt).

### 3.2 Pattern scorers (`scoring.py`)

Add small pure helpers (use `collections.Counter`). Constants for the fixed
payouts keep magic numbers out of the logic:

```python
FULL_HOUSE_SCORE = 25
SMALL_STRAIGHT_SCORE = 30
LARGE_STRAIGHT_SCORE = 40
YAHTZEE_SCORE = 50


def _max_of_a_kind(dice: list[int]) -> int:
    return max(Counter(dice).values(), default=0)


def score_three_of_a_kind(dice: list[int]) -> int:
    return sum(dice) if _max_of_a_kind(dice) >= 3 else 0


def score_four_of_a_kind(dice: list[int]) -> int:
    return sum(dice) if _max_of_a_kind(dice) >= 4 else 0


def score_full_house(dice: list[int]) -> int:
    return FULL_HOUSE_SCORE if sorted(Counter(dice).values()) == [2, 3] else 0


def score_small_straight(dice: list[int]) -> int:
    runs = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})
    faces = set(dice)
    return SMALL_STRAIGHT_SCORE if any(run <= faces for run in runs) else 0


def score_large_straight(dice: list[int]) -> int:
    return LARGE_STRAIGHT_SCORE if set(dice) in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0


def score_yahtzee(dice: list[int]) -> int:
    return YAHTZEE_SCORE if _max_of_a_kind(dice) >= 5 else 0


def score_chance(dice: list[int]) -> int:
    return sum(dice)
```

### 3.3 Dispatch (`scoring.py`)

Replace the single face-based body of `score_category` with a registry that
keeps the upper section face-based and routes lower categories to their scorer.
Public signature and `KeyError`-on-unknown behaviour are unchanged:

```python
def _face_scorer(face: int) -> Callable[[list[int]], int]:
    return lambda dice: sum(v for v in dice if v == face)


_SCORERS: dict[str, Callable[[list[int]], int]] = {
    name: _face_scorer(face) for name, face in _FACE_OF.items()
}
_SCORERS.update(
    {
        "three_of_a_kind": score_three_of_a_kind,
        "four_of_a_kind": score_four_of_a_kind,
        "full_house": score_full_house,
        "small_straight": score_small_straight,
        "large_straight": score_large_straight,
        "yahtzee": score_yahtzee,
        "chance": score_chance,
    }
)


def score_category(category: str, dice_values: list[int]) -> int:
    return _SCORERS[category](dice_values)   # KeyError if unknown (unchanged)
```

### 3.4 Unfilled vs. zero — use `None` as the "unfilled" sentinel

This is the key model change. Make the score table `dict[str, int | None]`:

- `new_score_table()` → `dict.fromkeys(CATEGORIES, None)`.
- A category is **available** iff its value `is None` (no longer `== 0`).
- A filled category may legitimately hold `0`.

Downstream adjustments:

- `total_score(table)` → `sum(v for v in table.values() if v is not None)`.
- `upper_section_subtotal(table)` (from #7) →
  `sum(table[c] or 0 for c in UPPER_CATEGORIES)` (treat `None` as 0).
- `is_valid_category` is unchanged (membership only).

> **Lighter alternative (not recommended):** keep `0` as the sentinel and forbid
> filling a category with a real 0. That contradicts standard Yahtzee (you must
> sometimes take a 0) and leaves the latent "0 looks unfilled" bug in place.
> Prefer the `None` model.

### 3.5 CLI (`cli.py`)

- `prompt_save_category`: `available = [c for c in scoring.CATEGORIES if table[c] is None]`.
  (Today it filters on `== 0`.) Consider grouping/labelling upper vs lower in the
  prompt for readability with 13 categories.
- `print_score_table`: render `None` as a placeholder (e.g. `-`); keep the
  aligned `ljust` style; the column width must account for the longer lower-section
  names (`three_of_a_kind` is 15 chars). Optionally print upper/lower section
  headers and (with #7) the subtotal/bonus block.
- `main`: the loop already iterates `scoring.CATEGORIES`, so it automatically
  grows from 6 to 13 turns — no structural change, but verify the
  longer game still reads well.

### 3.6 `__init__.py`

Export the new public names: `UPPER_CATEGORIES`, `LOWER_CATEGORIES`, the score
constants, and the per-category scorer functions (add to the import block and
`__all__`).

## 4. Scoring rules — decisions & edge cases

| Category | Rule | Edge case / decision |
| --- | --- | --- |
| 3 of a kind | max face count ≥ 3 → sum of all dice | A four- or five-of-a-kind also qualifies (count ≥ 3). |
| 4 of a kind | max face count ≥ 4 → sum of all dice | Five-of-a-kind also qualifies. |
| Full house | face counts are exactly `{3, 2}` → 25 | **Decision: strict.** Five-of-a-kind (`[5]`) is *not* a full house. Note in a docstring; a variant rule could accept it. |
| Small straight | contains one of `{1234, 2345, 3456}` → 30 | Duplicates are fine (e.g. `1,2,3,4,4`). |
| Large straight | face set is `{1-5}` or `{2-6}` → 40 | — |
| Yahtzee | max face count ≥ 5 → 50 | **Out of scope:** the 100-point *Yahtzee bonus* for extra yahtzees and joker rules — note as future work, don't implement now. |
| Chance | always sum of all dice | Never 0 for real 5-die hands. |

## 5. Tests to add (`tests/test_scoring.py`)

Add a `TestLowerSection` (or per-category classes) covering hits **and** misses,
since "scores 0 when the pattern is absent" is core behaviour:

- 3/4 of a kind: qualifying hand → sum; non-qualifying → 0; five-of-a-kind also
  qualifies for both.
- Full house: `[2,2,3,3,3]` → 25; `[2,2,2,3,4]` → 0; `[5,5,5,5,5]` → 0 (strict).
- Small straight: `[1,2,3,4,6]` → 30; `[1,2,3,4,4]` → 30; `[1,1,2,3,5]` → 0.
- Large straight: `[1,2,3,4,5]` → 40; `[2,3,4,5,6]` → 40; `[1,2,3,4,6]` → 0.
- Yahtzee: `[6,6,6,6,6]` → 50; four-of-a-kind → 0.
- Chance: `[1,2,3,4,5]` → 15.
- `score_category` dispatches to the right scorer for each lower name and still
  raises `KeyError` for unknown categories.
- Table model: `new_score_table()` values are all `None`; `total_score` ignores
  `None`; a category filled with `0` is counted as filled (not "available").
- With #7: `upper_section_subtotal` ignores lower categories (no bonus inflation).

CLI (`tests/test_cli.py`):

- `prompt_save_category` offers a category filled with `0` no longer (uses the
  `None` rule), following the existing `feed_input` pattern.
- `print_score_table` renders unfilled categories and includes lower-section names.
- Update `test_main_plays_full_game` for the 13-category game (more answers).

## 6. Suggested commit / PR

- Branch: `feat/lower-section-scoring`
- Conventional message: `feat(scoring): add lower-section categories`
- Update `CHANGELOG.md` (Unreleased → Added) per `RELEASING.md`.
- Reference `Closes #4` in the PR body.

## 7. Effort estimate

Medium. The scorers themselves are small and pure (~50 lines), but the
`None`-sentinel model change ripples through `scoring`, `cli`, `__init__`, and
several tests, and must stay coordinated with the #7 bonus subtotal. Budget for
a careful pass over the CLI display and the longer game loop. No new runtime
dependencies (`collections.Counter` is stdlib).

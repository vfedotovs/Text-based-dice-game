# Issue #7 — Implement bonus for the upper score section

> **FEAT: implement bonus for upper score section**
> Bonus: If you score 63 or more points in the Upper Section, you earn a 35 bonus.

This is the standard Yahtzee rule: once the six upper-section categories
(`ones`–`sixes`) sum to **63 or more**, the player earns a flat **35-point**
bonus that is added on top of their total.

This document reviews how the bonus fits the current code and proposes an
implementation. **No code is written yet** — this is the plan only.

---

## 1. Current state

The whole game today *is* the upper section, so the score table holds exactly
the six categories:

- `src/dice_game/scoring.py`
  - `CATEGORIES` — the six upper categories.
  - `new_score_table()` — `dict[str, int]`, each category at `0`.
  - `score_category(category, dice_values)` — sum of matching faces.
  - `total_score(table)` — `sum(table.values())`.
- `src/dice_game/cli.py`
  - `print_score_table(table)` — prints each category and value.
  - `print_final_score(table)` — prints `total_score(table)`.
- `src/dice_game/__init__.py` re-exports the scoring API.

Because `total_score` simply sums the table, it has nowhere to express a bonus
that is *derived* from the subtotal rather than stored as a category.

## 2. Design decision: derive the bonus, don't store it

There are two ways to add the bonus:

| Option | How | Verdict |
| --- | --- | --- |
| **A. Store bonus as a table entry** | Add a `"bonus"` key to the score table | ✗ Pollutes the table; `prompt_save_category`, `CATEGORIES` iteration, and tests all assume the table is only real categories. Fragile. |
| **B. Derive bonus from the subtotal** | Keep the table as the six categories; compute the bonus on demand | ✓ Single source of truth, no special-casing in input/loop logic, backward-compatible. |

**Recommendation: Option B.** The bonus is a pure function of the upper
subtotal, so compute it; don't persist it.

## 3. Proposed changes

### 3.1 `scoring.py` — constants and functions

Add module-level constants and three small functions (names mirror the existing
style):

```python
UPPER_SECTION_THRESHOLD = 63
UPPER_SECTION_BONUS = 35


def upper_section_subtotal(table: dict[str, int]) -> int:
    """Return the sum of the six upper-section category scores."""
    return sum(table[category] for category in CATEGORIES)


def upper_section_bonus(table: dict[str, int]) -> int:
    """Return the 35-point bonus if the subtotal reaches the threshold, else 0."""
    if upper_section_subtotal(table) >= UPPER_SECTION_THRESHOLD:
        return UPPER_SECTION_BONUS
    return 0


def total_score(table: dict[str, int]) -> int:
    """Return the upper subtotal plus any earned bonus."""
    return upper_section_subtotal(table) + upper_section_bonus(table)
```

Notes:
- `upper_section_subtotal` iterates `CATEGORIES` rather than `table.values()`
  so it stays correct even if the table ever gains non-category keys.
- `total_score` keeps its existing signature, so `cli.py` needs no change to
  the final-score print. Its meaning is unchanged when no bonus is earned.

### 3.2 `cli.py` — show the bonus to the player

The bonus should be *visible*, otherwise the total looks like it jumped by 35
for no reason. Two touch points:

- `print_score_table` (or `print_final_score`): after the categories, print the
  subtotal, the bonus line, and the total, e.g.:

  ```
  ==== My Score Table ====
    ones   -> 3
    ...
    sixes  -> 18
  ------------------------
    subtotal -> 65
    bonus    -> 35  (63+ earns 35)
    TOTAL    -> 100
  ```

- `print_final_score` already calls `total_score`, which now includes the
  bonus — but consider also printing the bonus line so the result is explained.

Keep the exact formatting consistent with the existing aligned `ljust` style.

### 3.3 `__init__.py` — export the new public API

Add to the `from .scoring import (...)` block and `__all__`:

- `UPPER_SECTION_THRESHOLD`
- `UPPER_SECTION_BONUS`
- `upper_section_subtotal`
- `upper_section_bonus`

## 4. Backward compatibility

The two existing `total_score` tests still pass:

- `test_sums_all_values` — subtotal `21` (`< 63`) → no bonus → `21`. ✓
- `test_empty_game_totals_zero` — subtotal `0` → `0`. ✓

So this is an additive change; no existing test needs editing.

## 5. Tests to add (`tests/test_scoring.py`)

Boundary behaviour is the whole point of this feature, so test around 63:

- `upper_section_subtotal` returns the sum of the six categories.
- `upper_section_bonus`:
  - subtotal `62` → `0` (just below threshold).
  - subtotal `63` → `35` (exactly at threshold — inclusive).
  - subtotal `64`/max → `35` (above threshold).
  - subtotal `0` / empty table → `0`.
- `total_score`:
  - below threshold → equals the subtotal (no bonus added).
  - at/above threshold → subtotal `+ 35`.
- A realistic max case: every category at its max
  (`ones`=5, `twos`=10, `threes`=15, `fours`=20, `fives`=25, `sixes`=30 = 105)
  → `total_score` = `140`.

Building a 63-subtotal table for the boundary test, e.g.: set
`fours=20, fives=25, threes=15, ones=3` → `63`.

Optionally add a CLI test (`tests/test_cli.py`) asserting the bonus line is
printed once a high-scoring game ends, following the existing
`feed_input`/`capsys` pattern.

## 6. Suggested commit / PR

- Branch: `feat/upper-section-bonus`
- Conventional message: `feat(scoring): add upper-section 63+ bonus of 35 points`
- Update `CHANGELOG.md` (Unreleased → Added) per `RELEASING.md`.
- Reference `Closes #7` in the PR body.

## 7. Effort estimate

Small. ~25 lines of logic across `scoring.py` / `cli.py` / `__init__.py`,
plus ~6 focused tests. No new dependencies, no breaking changes.

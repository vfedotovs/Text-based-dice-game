"""Pure scoring logic for the upper and lower sections.

The score table is a plain ``dict[str, int | None]`` created by
:func:`new_score_table` so every game (and every test) gets its own fresh,
independent state instead of sharing a module-level global. A category value of
``None`` means *unfilled*; once played a category holds an ``int`` score, which
may legitimately be ``0`` (e.g. declaring Yahtzee with no five-of-a-kind).
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable

# A score table maps each category to its score, or ``None`` if not yet played.
ScoreTable = dict[str, "int | None"]

# Upper section: index + 1 is the die face each category counts.
UPPER_CATEGORIES: tuple[str, ...] = (
    "ones",
    "twos",
    "threes",
    "fours",
    "fives",
    "sixes",
)

# Lower section: each category scores the whole 5-dice hand by pattern.
LOWER_CATEGORIES: tuple[str, ...] = (
    "three_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "small_straight",
    "large_straight",
    "yahtzee",
    "chance",
)

# All categories, in play order (upper first, then lower).
CATEGORIES: tuple[str, ...] = UPPER_CATEGORIES + LOWER_CATEGORIES

_FACE_OF: dict[str, int] = {
    name: face for face, name in enumerate(UPPER_CATEGORIES, start=1)
}

# Yahtzee upper-section bonus: reaching the threshold earns a flat bonus.
UPPER_SECTION_THRESHOLD = 63
UPPER_SECTION_BONUS = 35

# Fixed payouts for the pattern-based lower-section categories.
FULL_HOUSE_SCORE = 25
SMALL_STRAIGHT_SCORE = 30
LARGE_STRAIGHT_SCORE = 40
YAHTZEE_SCORE = 50


def _max_of_a_kind(dice_values: list[int]) -> int:
    """Return the highest number of identical dice (0 for an empty hand)."""
    return max(Counter(dice_values).values(), default=0)


def score_three_of_a_kind(dice_values: list[int]) -> int:
    """Sum of all dice if at least three share a face, else 0."""
    return sum(dice_values) if _max_of_a_kind(dice_values) >= 3 else 0


def score_four_of_a_kind(dice_values: list[int]) -> int:
    """Sum of all dice if at least four share a face, else 0."""
    return sum(dice_values) if _max_of_a_kind(dice_values) >= 4 else 0


def score_full_house(dice_values: list[int]) -> int:
    """:data:`FULL_HOUSE_SCORE` for an exact 3-and-2 split, else 0.

    A strict full house: a five-of-a-kind does *not* count.
    """
    return FULL_HOUSE_SCORE if sorted(Counter(dice_values).values()) == [2, 3] else 0


def score_small_straight(dice_values: list[int]) -> int:
    """:data:`SMALL_STRAIGHT_SCORE` for any four consecutive faces, else 0."""
    faces = set(dice_values)
    runs = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})
    return SMALL_STRAIGHT_SCORE if any(run <= faces for run in runs) else 0


def score_large_straight(dice_values: list[int]) -> int:
    """:data:`LARGE_STRAIGHT_SCORE` for five consecutive faces, else 0."""
    straights = ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6})
    return LARGE_STRAIGHT_SCORE if set(dice_values) in straights else 0


def score_yahtzee(dice_values: list[int]) -> int:
    """:data:`YAHTZEE_SCORE` for five of a kind, else 0."""
    return YAHTZEE_SCORE if _max_of_a_kind(dice_values) >= 5 else 0


def score_chance(dice_values: list[int]) -> int:
    """Sum of all dice, with no qualifying pattern required."""
    return sum(dice_values)


def _face_scorer(face: int) -> Callable[[list[int]], int]:
    """Return a scorer summing all dice equal to ``face``."""
    return lambda dice_values: sum(v for v in dice_values if v == face)


# Dispatch table: category name -> scorer over the full hand.
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


def new_score_table() -> ScoreTable:
    """Return a fresh score table with every category unfilled (``None``)."""
    return dict.fromkeys(CATEGORIES, None)


def is_valid_category(category: str) -> bool:
    """Return whether ``category`` is a known scoring category."""
    return category in _SCORERS


def score_category(category: str, dice_values: list[int]) -> int:
    """Return the score for ``category`` given ``dice_values``.

    Upper-section categories sum the dice matching their face; lower-section
    categories score the whole hand by pattern (see the ``score_*`` functions).

    Raises:
        KeyError: If ``category`` is not a valid category.
    """
    return _SCORERS[category](dice_values)


def upper_section_subtotal(table: ScoreTable) -> int:
    """Return the sum of the six upper-section category scores (``None`` as 0)."""
    return sum(table[category] or 0 for category in UPPER_CATEGORIES)


def upper_section_bonus(table: ScoreTable) -> int:
    """Return the bonus if the upper subtotal reaches the threshold, else 0."""
    if upper_section_subtotal(table) >= UPPER_SECTION_THRESHOLD:
        return UPPER_SECTION_BONUS
    return 0


def total_score(table: ScoreTable) -> int:
    """Return the sum of all played categories plus any upper-section bonus."""
    played = sum(value for value in table.values() if value is not None)
    return played + upper_section_bonus(table)

"""Pure scoring logic for the upper section (ones through sixes).

The score table is a plain ``dict[str, int]`` created by :func:`new_score_table`
so every game (and every test) gets its own fresh, independent state instead of
sharing a module-level global.
"""

from __future__ import annotations

# Ordered categories; index + 1 is the die face each category counts.
CATEGORIES: tuple[str, ...] = (
    "ones",
    "twos",
    "threes",
    "fours",
    "fives",
    "sixes",
)

_FACE_OF: dict[str, int] = {name: face for face, name in enumerate(CATEGORIES, start=1)}


def new_score_table() -> dict[str, int]:
    """Return a fresh score table with every category initialised to 0."""
    return {category: 0 for category in CATEGORIES}


def is_valid_category(category: str) -> bool:
    """Return whether ``category`` is a known scoring category."""
    return category in _FACE_OF


def score_category(category: str, dice_values: list[int]) -> int:
    """Return the score for ``category`` given ``dice_values``.

    The score is the sum of all dice matching the category's face value, e.g.
    ``score_category("threes", [3, 3, 1, 3, 6])`` -> ``9``.

    Raises:
        KeyError: If ``category`` is not a valid category.
    """
    face = _FACE_OF[category]
    return sum(value for value in dice_values if value == face)


def total_score(table: dict[str, int]) -> int:
    """Return the sum of all category scores in ``table``."""
    return sum(table.values())

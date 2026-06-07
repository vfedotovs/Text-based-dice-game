"""Text-based dice game (single-player, Yahtzee-style upper section).

Public API re-exports the pure logic so callers can do, e.g.::

    from dice_game import roll_dice, score_category, new_score_table
"""

from .dice import (
    DIE_MAX,
    DIE_MIN,
    NUM_DICE,
    is_valid_keep_selection,
    parse_selection,
    reroll,
    roll_dice,
)
from .scoring import (
    CATEGORIES,
    UPPER_SECTION_BONUS,
    UPPER_SECTION_THRESHOLD,
    is_valid_category,
    new_score_table,
    score_category,
    total_score,
    upper_section_bonus,
    upper_section_subtotal,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # dice
    "DIE_MAX",
    "DIE_MIN",
    "NUM_DICE",
    "is_valid_keep_selection",
    "parse_selection",
    "reroll",
    "roll_dice",
    # scoring
    "CATEGORIES",
    "UPPER_SECTION_BONUS",
    "UPPER_SECTION_THRESHOLD",
    "is_valid_category",
    "new_score_table",
    "score_category",
    "total_score",
    "upper_section_bonus",
    "upper_section_subtotal",
]

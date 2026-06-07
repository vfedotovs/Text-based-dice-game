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
    is_valid_category,
    new_score_table,
    score_category,
    total_score,
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
    "is_valid_category",
    "new_score_table",
    "score_category",
    "total_score",
]

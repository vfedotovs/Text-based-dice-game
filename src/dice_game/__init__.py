"""Text-based dice game (single-player, Yahtzee-style upper and lower sections).

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
    FULL_HOUSE_SCORE,
    LARGE_STRAIGHT_SCORE,
    LOWER_CATEGORIES,
    SMALL_STRAIGHT_SCORE,
    UPPER_CATEGORIES,
    UPPER_SECTION_BONUS,
    UPPER_SECTION_THRESHOLD,
    YAHTZEE_SCORE,
    ScoreTable,
    is_valid_category,
    new_score_table,
    score_category,
    score_chance,
    score_four_of_a_kind,
    score_full_house,
    score_large_straight,
    score_small_straight,
    score_three_of_a_kind,
    score_yahtzee,
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
    "FULL_HOUSE_SCORE",
    "LARGE_STRAIGHT_SCORE",
    "LOWER_CATEGORIES",
    "SMALL_STRAIGHT_SCORE",
    "ScoreTable",
    "UPPER_CATEGORIES",
    "UPPER_SECTION_BONUS",
    "UPPER_SECTION_THRESHOLD",
    "YAHTZEE_SCORE",
    "is_valid_category",
    "new_score_table",
    "score_category",
    "score_chance",
    "score_four_of_a_kind",
    "score_full_house",
    "score_large_straight",
    "score_small_straight",
    "score_three_of_a_kind",
    "score_yahtzee",
    "total_score",
    "upper_section_bonus",
    "upper_section_subtotal",
]

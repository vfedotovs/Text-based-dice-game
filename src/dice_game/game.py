"""Turn orchestration.

:func:`play_turn` runs one turn of up to :data:`MAX_THROWS` rolls. It contains
no I/O of its own: it receives a ``prompt_keep`` callable that asks the player
which dice to keep, so the same logic is driven by the real CLI in production and
by simple fakes in tests.
"""

from __future__ import annotations

import random
from typing import Callable

from . import dice

MAX_THROWS = 3

# Given the current dice and the throw number (1-based), return the 1-based
# positions the player wants to keep.
PromptKeep = Callable[[list[int], int], "list[int]"]


def play_turn(prompt_keep: PromptKeep, rng: random.Random | None = None) -> list[int]:
    """Play one turn and return the final dice values.

    The player gets an initial roll plus up to ``MAX_THROWS - 1`` rerolls. After
    each non-final throw ``prompt_keep`` is asked which dice to keep; the kept
    values are preserved (fixing the original bug where they were discarded) and
    the rest are rerolled. Keeping all dice ends the turn early.

    Args:
        prompt_keep: Callable returning valid keep positions for the given dice.
        rng: Optional random source; defaults to the global ``random`` module.

    Returns:
        The final list of :data:`dice.NUM_DICE` dice values.
    """
    current = dice.roll_dice(dice.NUM_DICE, rng)

    # Throws 1..MAX_THROWS-1 each allow a reroll; the final throw cannot.
    for throw in range(1, MAX_THROWS):
        keep = prompt_keep(current, throw)
        if len(set(keep)) >= dice.NUM_DICE:
            break  # Player is happy with everything — stop early.
        current = dice.reroll(current, keep, rng)

    return current

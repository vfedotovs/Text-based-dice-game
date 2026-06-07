"""Pure dice logic: rolling, parsing/validating selections, and rerolling.

No I/O lives here — every function takes its inputs as arguments and returns a
value, which makes the module trivial to unit test. Randomness is injectable via
the ``rng`` parameter so tests can pass a seeded ``random.Random`` instance.
"""

from __future__ import annotations

import random
from collections.abc import Iterable

NUM_DICE = 5
DIE_MIN = 1
DIE_MAX = 6


def roll_dice(count: int, rng: random.Random | None = None) -> list[int]:
    """Roll ``count`` dice, returning their values (each in ``DIE_MIN..DIE_MAX``).

    Args:
        count: Number of dice to roll. ``0`` returns an empty list.
        rng: Optional random source; defaults to the global ``random`` module.

    Returns:
        A list of ``count`` integers, each in the range 1-6.

    Raises:
        ValueError: If ``count`` is negative.
    """
    if count < 0:
        raise ValueError("count must be non-negative")
    source = rng if rng is not None else random
    return [source.randint(DIE_MIN, DIE_MAX) for _ in range(count)]


def parse_selection(text: str) -> list[int]:
    """Parse a raw keep-selection string into a list of integer positions.

    Each character is interpreted as a single digit, e.g. ``"135"`` -> ``[1, 3, 5]``.

    Args:
        text: User-entered string (surrounding whitespace is ignored).

    Returns:
        The digits as a list of ints.

    Raises:
        ValueError: If any character is not a digit.
    """
    return [int(char) for char in text.strip()]


def is_valid_keep_selection(positions: Iterable[int]) -> bool:
    """Return whether ``positions`` is a valid set of dice positions to keep.

    A selection is valid when it is non-empty, has no duplicates, contains at
    most ``NUM_DICE`` entries, and every position is in ``1..NUM_DICE``.
    """
    positions = list(positions)
    if not positions:
        return False
    if len(positions) > NUM_DICE:
        return False
    if len(set(positions)) != len(positions):
        return False
    return all(1 <= position <= NUM_DICE for position in positions)


def reroll(
    dice: list[int],
    keep_positions: Iterable[int],
    rng: random.Random | None = None,
) -> list[int]:
    """Return a new dice list, keeping chosen positions and rerolling the rest.

    Args:
        dice: Current dice values.
        keep_positions: 1-based positions whose values are preserved.
        rng: Optional random source; defaults to the global ``random`` module.

    Returns:
        A new list the same length as ``dice``; kept positions retain their
        value, all others get a fresh roll.
    """
    source = rng if rng is not None else random
    keep = set(keep_positions)
    return [
        value if position in keep else source.randint(DIE_MIN, DIE_MAX)
        for position, value in enumerate(dice, start=1)
    ]

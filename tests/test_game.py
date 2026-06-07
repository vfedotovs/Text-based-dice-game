"""Tests for turn orchestration in :mod:`dice_game.game`."""

from __future__ import annotations

import random

from dice_game import dice, game


def test_keep_all_ends_turn_after_one_prompt() -> None:
    calls: list[int] = []

    def prompt_keep(current: list[int], throw: int) -> list[int]:
        calls.append(throw)
        return list(range(1, dice.NUM_DICE + 1))  # keep everything

    result = game.play_turn(prompt_keep, random.Random(1))

    assert len(result) == dice.NUM_DICE
    assert calls == [1]  # stopped early, no reroll prompts


def test_prompts_until_max_throws_when_rerolling() -> None:
    calls: list[int] = []

    def prompt_keep(current: list[int], throw: int) -> list[int]:
        calls.append(throw)
        return [1]  # keep one, reroll the rest each time

    game.play_turn(prompt_keep, random.Random(2))

    # MAX_THROWS rolls means MAX_THROWS - 1 reroll prompts.
    assert calls == list(range(1, game.MAX_THROWS))


def test_kept_dice_are_preserved_across_rerolls() -> None:
    """Regression for the original bug where kept dice were discarded."""
    seen: list[list[int]] = []

    def prompt_keep(current: list[int], throw: int) -> list[int]:
        seen.append(list(current))
        return [1, 2]  # always keep the first two dice

    game.play_turn(prompt_keep, random.Random(123))

    # The prompt sees the dice before each reroll; positions 1 and 2 the player
    # kept must carry over unchanged into the next throw it sees.
    assert len(seen) >= 2
    for before, after in zip(seen, seen[1:], strict=False):
        assert after[0] == before[0]
        assert after[1] == before[1]


def test_result_length_is_always_five() -> None:
    result = game.play_turn(lambda current, throw: [3], random.Random(5))
    assert len(result) == dice.NUM_DICE

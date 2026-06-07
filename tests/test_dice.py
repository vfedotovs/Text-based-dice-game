"""Tests for the pure dice logic in :mod:`dice_game.dice`."""

from __future__ import annotations

import random

import pytest

from dice_game import dice


class TestRollDice:
    def test_returns_requested_count(self) -> None:
        assert len(dice.roll_dice(5)) == 5

    def test_zero_count_returns_empty(self) -> None:
        assert dice.roll_dice(0) == []

    def test_values_in_range(self) -> None:
        for value in dice.roll_dice(200):
            assert dice.DIE_MIN <= value <= dice.DIE_MAX

    def test_negative_count_raises(self) -> None:
        with pytest.raises(ValueError):
            dice.roll_dice(-1)

    def test_is_deterministic_with_seeded_rng(self) -> None:
        a = dice.roll_dice(5, random.Random(123))
        b = dice.roll_dice(5, random.Random(123))
        assert a == b


class TestParseSelection:
    def test_parses_digits(self) -> None:
        assert dice.parse_selection("135") == [1, 3, 5]

    def test_strips_whitespace(self) -> None:
        assert dice.parse_selection("  24 ") == [2, 4]

    def test_empty_string_returns_empty(self) -> None:
        assert dice.parse_selection("") == []

    def test_non_digit_raises(self) -> None:
        with pytest.raises(ValueError):
            dice.parse_selection("1a3")


class TestIsValidKeepSelection:
    def test_empty_is_invalid(self) -> None:
        assert dice.is_valid_keep_selection([]) is False

    def test_valid_subset(self) -> None:
        assert dice.is_valid_keep_selection([1, 3, 5]) is True

    def test_keep_all_positions_valid(self) -> None:
        assert dice.is_valid_keep_selection([1, 2, 3, 4, 5]) is True

    def test_too_many_is_invalid(self) -> None:
        assert dice.is_valid_keep_selection([1, 2, 3, 4, 5, 1]) is False

    def test_duplicates_invalid(self) -> None:
        assert dice.is_valid_keep_selection([1, 1]) is False

    @pytest.mark.parametrize("bad", [[0], [6], [9], [1, 0]])
    def test_out_of_range_invalid(self, bad: list[int]) -> None:
        assert dice.is_valid_keep_selection(bad) is False

    def test_always_returns_bool(self) -> None:
        # Regression: original returned None on the fall-through path.
        assert isinstance(dice.is_valid_keep_selection([2, 3]), bool)


class TestReroll:
    def test_preserves_kept_positions(self) -> None:
        original = [1, 2, 3, 4, 5]
        result = dice.reroll(original, [1, 2, 3], random.Random(1))
        assert result[:3] == [1, 2, 3]

    def test_length_is_unchanged(self) -> None:
        result = dice.reroll([1, 2, 3, 4, 5], [2, 4], random.Random(0))
        assert len(result) == 5

    def test_keep_none_rerolls_all(self) -> None:
        original = [1, 1, 1, 1, 1]
        # Seed chosen so at least one die changes; mainly assert kept count is 0.
        result = dice.reroll(original, [], random.Random(7))
        assert len(result) == 5
        for value in result:
            assert dice.DIE_MIN <= value <= dice.DIE_MAX

    def test_keep_all_preserves_everything(self) -> None:
        original = [6, 5, 4, 3, 2]
        assert dice.reroll(original, [1, 2, 3, 4, 5], random.Random(9)) == original

    def test_is_deterministic_with_seeded_rng(self) -> None:
        a = dice.reroll([1, 2, 3, 4, 5], [1], random.Random(42))
        b = dice.reroll([1, 2, 3, 4, 5], [1], random.Random(42))
        assert a == b

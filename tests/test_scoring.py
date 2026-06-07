"""Tests for the pure scoring logic in :mod:`dice_game.scoring`."""

from __future__ import annotations

import pytest

from dice_game import scoring


class TestNewScoreTable:
    def test_has_all_categories(self) -> None:
        assert tuple(scoring.new_score_table()) == scoring.CATEGORIES

    def test_all_start_at_zero(self) -> None:
        assert set(scoring.new_score_table().values()) == {0}

    def test_values_are_ints(self) -> None:
        # Regression: original table stored strings ("0").
        for value in scoring.new_score_table().values():
            assert isinstance(value, int)

    def test_instances_are_independent(self) -> None:
        a = scoring.new_score_table()
        a["ones"] = 3
        assert scoring.new_score_table()["ones"] == 0


class TestIsValidCategory:
    def test_known_category(self) -> None:
        assert scoring.is_valid_category("threes") is True

    def test_unknown_category(self) -> None:
        assert scoring.is_valid_category("sevens") is False


class TestScoreCategory:
    def test_sums_matching_faces(self) -> None:
        assert scoring.score_category("threes", [3, 3, 1, 3, 6]) == 9

    def test_no_matches_scores_zero(self) -> None:
        assert scoring.score_category("twos", [1, 3, 4, 5, 6]) == 0

    @pytest.mark.parametrize(
        ("category", "expected"),
        [
            ("ones", 2),
            ("twos", 4),
            ("threes", 3),
            ("fours", 4),
            ("fives", 5),
            ("sixes", 6),
        ],
    )
    def test_each_category_face(self, category: str, expected: int) -> None:
        dice_values = [1, 1, 2, 2, 3, 4, 5, 6]
        assert scoring.score_category(category, dice_values) == expected

    def test_invalid_category_raises(self) -> None:
        with pytest.raises(KeyError):
            scoring.score_category("sevens", [1, 2, 3])


class TestTotalScore:
    def test_sums_all_values(self) -> None:
        table = scoring.new_score_table()
        table["threes"] = 9
        table["sixes"] = 12
        assert scoring.total_score(table) == 21

    def test_empty_game_totals_zero(self) -> None:
        assert scoring.total_score(scoring.new_score_table()) == 0

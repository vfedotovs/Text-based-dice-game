"""Tests for the pure scoring logic in :mod:`dice_game.scoring`."""

from __future__ import annotations

import pytest

from dice_game import scoring


class TestNewScoreTable:
    def test_has_all_categories(self) -> None:
        assert tuple(scoring.new_score_table()) == scoring.CATEGORIES

    def test_includes_upper_and_lower_sections(self) -> None:
        keys = set(scoring.new_score_table())
        assert set(scoring.UPPER_CATEGORIES) <= keys
        assert set(scoring.LOWER_CATEGORIES) <= keys

    def test_all_start_unfilled(self) -> None:
        # ``None`` marks an unplayed category, distinct from a played 0.
        assert set(scoring.new_score_table().values()) == {None}

    def test_instances_are_independent(self) -> None:
        a = scoring.new_score_table()
        a["ones"] = 3
        assert scoring.new_score_table()["ones"] is None


class TestIsValidCategory:
    def test_known_upper_category(self) -> None:
        assert scoring.is_valid_category("threes") is True

    def test_known_lower_category(self) -> None:
        assert scoring.is_valid_category("full_house") is True

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


class TestLowerSectionScorers:
    @pytest.mark.parametrize(
        ("dice", "expected"),
        [
            ([3, 3, 3, 1, 6], 16),  # exactly three of a kind -> sum
            ([4, 4, 4, 4, 2], 18),  # four also qualifies
            ([5, 5, 5, 5, 5], 25),  # five also qualifies
            ([2, 2, 6, 1, 3], 0),  # only a pair -> 0
        ],
    )
    def test_three_of_a_kind(self, dice: list[int], expected: int) -> None:
        assert scoring.score_three_of_a_kind(dice) == expected

    @pytest.mark.parametrize(
        ("dice", "expected"),
        [
            ([4, 4, 4, 4, 2], 18),  # exactly four -> sum
            ([6, 6, 6, 6, 6], 30),  # five also qualifies
            ([3, 3, 3, 1, 6], 0),  # only three -> 0
        ],
    )
    def test_four_of_a_kind(self, dice: list[int], expected: int) -> None:
        assert scoring.score_four_of_a_kind(dice) == expected

    @pytest.mark.parametrize(
        ("dice", "expected"),
        [
            ([2, 2, 3, 3, 3], scoring.FULL_HOUSE_SCORE),
            ([5, 5, 5, 1, 1], scoring.FULL_HOUSE_SCORE),
            ([2, 2, 2, 3, 4], 0),  # trips but no pair
            ([5, 5, 5, 5, 5], 0),  # strict: five-of-a-kind is not a full house
        ],
    )
    def test_full_house(self, dice: list[int], expected: int) -> None:
        assert scoring.score_full_house(dice) == expected

    @pytest.mark.parametrize(
        ("dice", "expected"),
        [
            ([1, 2, 3, 4, 6], scoring.SMALL_STRAIGHT_SCORE),
            ([3, 4, 5, 6, 6], scoring.SMALL_STRAIGHT_SCORE),
            ([1, 2, 3, 4, 4], scoring.SMALL_STRAIGHT_SCORE),  # duplicate is fine
            ([1, 1, 2, 3, 5], 0),  # only three consecutive
        ],
    )
    def test_small_straight(self, dice: list[int], expected: int) -> None:
        assert scoring.score_small_straight(dice) == expected

    @pytest.mark.parametrize(
        ("dice", "expected"),
        [
            ([1, 2, 3, 4, 5], scoring.LARGE_STRAIGHT_SCORE),
            ([2, 3, 4, 5, 6], scoring.LARGE_STRAIGHT_SCORE),
            ([1, 2, 3, 4, 6], 0),  # small straight only
        ],
    )
    def test_large_straight(self, dice: list[int], expected: int) -> None:
        assert scoring.score_large_straight(dice) == expected

    @pytest.mark.parametrize(
        ("dice", "expected"),
        [
            ([6, 6, 6, 6, 6], scoring.YAHTZEE_SCORE),
            ([6, 6, 6, 6, 1], 0),  # four of a kind only
        ],
    )
    def test_yahtzee(self, dice: list[int], expected: int) -> None:
        assert scoring.score_yahtzee(dice) == expected

    def test_chance_is_always_the_sum(self) -> None:
        assert scoring.score_chance([1, 2, 3, 4, 5]) == 15

    def test_score_category_dispatches_to_lower_scorers(self) -> None:
        assert scoring.score_category("yahtzee", [2, 2, 2, 2, 2]) == 50
        assert scoring.score_category("full_house", [2, 2, 3, 3, 3]) == 25
        assert scoring.score_category("chance", [1, 1, 1, 1, 1]) == 5


def _table_with_subtotal_63() -> scoring.ScoreTable:
    """Return a table whose upper-section subtotal is exactly 63."""
    table = scoring.new_score_table()
    table["fours"] = 20
    table["fives"] = 25
    table["threes"] = 15
    table["ones"] = 3
    return table  # 20 + 25 + 15 + 3 == 63


class TestUpperSectionSubtotal:
    def test_sums_the_six_categories(self) -> None:
        table = scoring.new_score_table()
        table["threes"] = 9
        table["sixes"] = 12
        assert scoring.upper_section_subtotal(table) == 21

    def test_empty_table_is_zero(self) -> None:
        assert scoring.upper_section_subtotal(scoring.new_score_table()) == 0


class TestUpperSectionBonus:
    def test_below_threshold_scores_zero(self) -> None:
        table = _table_with_subtotal_63()
        table["ones"] = 2  # subtotal now 62, one short
        assert scoring.upper_section_subtotal(table) == 62
        assert scoring.upper_section_bonus(table) == 0

    def test_exactly_at_threshold_earns_bonus(self) -> None:
        table = _table_with_subtotal_63()
        assert scoring.upper_section_subtotal(table) == 63
        assert scoring.upper_section_bonus(table) == scoring.UPPER_SECTION_BONUS

    def test_above_threshold_earns_bonus(self) -> None:
        table = _table_with_subtotal_63()
        table["ones"] = 5  # subtotal now 65
        assert scoring.upper_section_bonus(table) == scoring.UPPER_SECTION_BONUS

    def test_empty_table_earns_no_bonus(self) -> None:
        assert scoring.upper_section_bonus(scoring.new_score_table()) == 0


class TestTotalScore:
    def test_sums_all_values(self) -> None:
        table = scoring.new_score_table()
        table["threes"] = 9
        table["sixes"] = 12
        assert scoring.total_score(table) == 21

    def test_empty_game_totals_zero(self) -> None:
        assert scoring.total_score(scoring.new_score_table()) == 0

    def test_below_threshold_excludes_bonus(self) -> None:
        table = _table_with_subtotal_63()
        table["ones"] = 2  # subtotal 62
        assert scoring.total_score(table) == 62

    def test_at_threshold_includes_bonus(self) -> None:
        table = _table_with_subtotal_63()  # subtotal 63
        assert scoring.total_score(table) == 63 + scoring.UPPER_SECTION_BONUS

    def test_counts_lower_section(self) -> None:
        table = scoring.new_score_table()
        table["chance"] = 17
        table["yahtzee"] = scoring.YAHTZEE_SCORE
        # No upper points -> no bonus; total is just the lower-section scores.
        assert scoring.total_score(table) == 17 + scoring.YAHTZEE_SCORE

    def test_played_zero_is_distinct_from_unfilled(self) -> None:
        table = scoring.new_score_table()
        table["yahtzee"] = 0  # declared yahtzee with no five-of-a-kind
        assert scoring.total_score(table) == 0

    def test_maximum_upper_game(self) -> None:
        # Every upper category maxed: 5 + 10 + 15 + 20 + 25 + 30 == 105, plus bonus.
        table = scoring.new_score_table()
        for face, category in enumerate(scoring.UPPER_CATEGORIES, start=1):
            table[category] = 5 * face
        assert scoring.upper_section_subtotal(table) == 105
        assert scoring.total_score(table) == 105 + scoring.UPPER_SECTION_BONUS

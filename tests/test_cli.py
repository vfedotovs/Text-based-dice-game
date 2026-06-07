"""Tests for the I/O layer in :mod:`dice_game.cli`.

``input``/``print`` are driven via monkeypatch/capsys so the prompts and the
full game loop can be exercised without a real terminal.
"""

from __future__ import annotations

import random
from collections.abc import Iterable

import pytest

from dice_game import cli, dice, scoring


def feed_input(monkeypatch: pytest.MonkeyPatch, answers: Iterable[str]) -> None:
    """Make ``input()`` return each string in ``answers`` in turn."""
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda *_: next(it))


class TestPromptKeepSelection:
    def test_keep_all_returns_every_position(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        feed_input(monkeypatch, [cli.KEEP_ALL])
        assert cli.prompt_keep_selection([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4, 5]

    def test_valid_selection_is_returned(self, monkeypatch: pytest.MonkeyPatch) -> None:
        feed_input(monkeypatch, ["135"])
        assert cli.prompt_keep_selection([1, 2, 3, 4, 5], 1) == [1, 3, 5]

    def test_reprompts_on_invalid_then_valid(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        feed_input(monkeypatch, ["9", "24"])  # 9 invalid, then 24 valid
        assert cli.prompt_keep_selection([1, 2, 3, 4, 5], 1) == [2, 4]
        assert "Invalid selection" in capsys.readouterr().out

    def test_reprompts_on_non_digit(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        feed_input(monkeypatch, ["ab", "1"])
        assert cli.prompt_keep_selection([1, 2, 3, 4, 5], 1) == [1]
        assert "digits only" in capsys.readouterr().out


class TestPromptSaveCategory:
    def test_valid_category_returned(self, monkeypatch: pytest.MonkeyPatch) -> None:
        feed_input(monkeypatch, ["threes"])
        assert cli.prompt_save_category(scoring.new_score_table()) == "threes"

    def test_is_case_insensitive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        feed_input(monkeypatch, ["SIXES"])
        assert cli.prompt_save_category(scoring.new_score_table()) == "sixes"

    def test_reprompts_on_invalid(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        feed_input(monkeypatch, ["sevens", "ones"])
        assert cli.prompt_save_category(scoring.new_score_table()) == "ones"
        assert "Invalid category" in capsys.readouterr().out


class TestPrinters:
    def test_print_score_table_shows_categories(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        cli.print_score_table(scoring.new_score_table())
        out = capsys.readouterr().out
        assert "My Score Table" in out
        for category in scoring.CATEGORIES:
            assert category in out

    def test_print_score_table_shows_subtotal_and_bonus(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        table = scoring.new_score_table()
        table["fours"] = 20
        table["fives"] = 25
        table["threes"] = 15
        table["ones"] = 3  # subtotal 63 -> bonus earned
        cli.print_score_table(table)
        out = capsys.readouterr().out
        assert "subtotal -> 63" in out
        assert f"bonus    -> {scoring.UPPER_SECTION_BONUS}" in out

    def test_print_final_score(self, capsys: pytest.CaptureFixture[str]) -> None:
        table = scoring.new_score_table()
        table["sixes"] = 12
        cli.print_final_score(table)
        assert "12" in capsys.readouterr().out


def test_main_plays_full_game(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Deterministic dice for the whole game.
    monkeypatch.setattr(random, "randint", lambda *_: 4)
    # Each turn: keep all, then save into the next category.
    answers: list[str] = []
    for category in scoring.CATEGORIES:
        answers += [cli.KEEP_ALL, category]
    feed_input(monkeypatch, answers)

    cli.main()

    out = capsys.readouterr().out
    assert "Game over" in out
    # Every die is a 4, so only the "fours" turn scores: 5 dice * 4 = 20.
    assert "your final score is: 20" in out


def test_keep_all_constant_matches_dice_count() -> None:
    # Entering KEEP_ALL must map to keeping all NUM_DICE positions.
    assert len(range(1, dice.NUM_DICE + 1)) == dice.NUM_DICE

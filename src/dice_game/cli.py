"""Command-line interface: all ``print``/``input`` lives here.

This module is the only place that talks to the terminal. It wires the pure
logic in :mod:`dice_game.dice`, :mod:`dice_game.scoring`, and the orchestration
in :mod:`dice_game.game` together into a playable game.
"""

from __future__ import annotations

from . import dice, game, scoring

KEEP_ALL = "0"


def print_score_table(table: dict[str, int]) -> None:
    """Print the current score table."""
    print("==== My Score Table ====")
    width = max(len(category) for category in table)
    for category, value in table.items():
        print(f"  {category.ljust(width)} -> {value}")


def prompt_keep_selection(dice_values: list[int], throw_number: int) -> list[int]:
    """Ask which dice to keep, looping until the input is valid.

    Returns the 1-based positions to keep. Entering ``0`` keeps every die and
    ends the turn early.
    """
    while True:
        print(f"\nThrow {throw_number} — current dice: {dice_values}")
        raw = input(
            f"Positions to keep (1-{dice.NUM_DICE}), or {KEEP_ALL} to keep all: "
        ).strip()

        if raw == KEEP_ALL:
            return list(range(1, dice.NUM_DICE + 1))

        try:
            positions = dice.parse_selection(raw)
        except ValueError:
            print("Please enter digits only.")
            continue

        if dice.is_valid_keep_selection(positions):
            return positions

        print("Invalid selection, please try again.")


def prompt_save_category(table: dict[str, int]) -> str:
    """Ask the player which category to save points to, looping until valid."""
    available = [c for c in scoring.CATEGORIES if table[c] == 0]
    while True:
        choice = (
            input(f"Save points to which category? ({', '.join(available)}): ")
            .strip()
            .lower()
        )
        if scoring.is_valid_category(choice):
            return choice
        print("Invalid category, please try again.")


def print_final_score(table: dict[str, int]) -> None:
    """Print the end-of-game total."""
    print()
    print(f"Game over — your final score is: {scoring.total_score(table)}")


def main() -> None:
    """Run a full single-player game: one turn per scoring category."""
    table = scoring.new_score_table()

    for _ in scoring.CATEGORIES:
        print_score_table(table)
        final_dice = game.play_turn(prompt_keep_selection)
        print(f"\nFinal dice: {final_dice}")
        category = prompt_save_category(table)
        table[category] = scoring.score_category(category, final_dice)

    print_score_table(table)
    print_final_score(table)


if __name__ == "__main__":
    main()

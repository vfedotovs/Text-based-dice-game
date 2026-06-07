# Functions to Implement Tests For — DONE

The original `main.py` was refactored into the `src/dice_game` package
(see `improve_quality_todo.md` §2). The functions below were renamed/relocated
and now have tests under `tests/` (56 tests, 96% coverage). Every bug noted
during the original review has been fixed.

Mapping from the old `main.py` names to the new package + tests:

| Old `main.py`              | New location                         | Tests              |
|----------------------------|--------------------------------------|--------------------|
| `generate_random_dices`    | `dice.roll_dice`                     | `test_dice.py`     |
| `is_valid_selection`       | `dice.is_valid_keep_selection` (+ `parse_selection`) | `test_dice.py` |
| `get_dice_retrow_selection`| `cli.prompt_keep_selection`          | `test_cli.py`      |
| `single_move`              | `game.play_turn`                     | `test_game.py`     |
| `user_save_input`          | `cli.prompt_save_category`           | `test_cli.py`      |
| `update_score_table`/`calculate_score` | `scoring.score_category` + `scoring.new_score_table` | `test_scoring.py` |
| `print_score_table`        | `cli.print_score_table`              | `test_cli.py`      |
| `game_end_score`           | `scoring.total_score` + `cli.print_final_score` | `test_scoring.py`, `test_cli.py` |

## Functions

- [x] `dice.roll_dice` — length, value range, `count == 0`, negative raises
      `ValueError`, deterministic with seeded rng.
- [x] `dice.parse_selection` — digit parsing, whitespace, empty, non-digit
      raises `ValueError`.
- [x] `dice.is_valid_keep_selection` — empty -> False, valid subset/keep-all,
      length > 5 -> False, duplicates -> False, out-of-range -> False; always
      returns a `bool` (fixed the implicit-`None` bug).
- [x] `dice.reroll` — preserves kept positions (fixes the keep-dice bug),
      length unchanged, keep-none/keep-all, deterministic with seeded rng.
- [x] `scoring.new_score_table` — all categories, all `int` 0 (no more strings),
      independent instances per call.
- [x] `scoring.score_category` — sums matching faces, zero on no match, every
      category face, invalid category raises `KeyError`.
- [x] `scoring.total_score` — sums all values, zero for a fresh table.
- [x] `scoring.is_valid_category` — known/unknown categories.
- [x] `game.play_turn` — keep-all ends early, prompts up to `MAX_THROWS`,
      **kept dice preserved across rerolls** (regression test), result length 5.
- [x] `cli.prompt_keep_selection` — keep-all, valid input, reprompt on invalid
      and on non-digit (mocked `input`/captured stdout).
- [x] `cli.prompt_save_category` — valid, case-insensitive, reprompt on invalid.
- [x] `cli.print_score_table` / `cli.print_final_score` — output assertions.
- [x] `cli.main` — full game played end-to-end with deterministic dice.

## Review Notes (all addressed in §2 refactor)

- [x] Replaced stringly-typed table values ("0") with ints.
- [x] Removed trailing spaces from table keys.
- [x] Deduplicated scoring into a single data-driven `score_category`.
- [x] Removed the dead `calculate_score` function.
- [x] Fixed typos in messages/docstrings ("Raises", etc.).
- [x] Separated I/O from logic so functions are testable without mocking STDIN.

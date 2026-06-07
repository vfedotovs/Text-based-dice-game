# Functions to Implement Tests For

Tracking unit tests for the functions in `main.py`.

## Functions

- [ ] `generate_random_dices(dice_count) -> list`
  - Returns a list of length `dice_count`, each value in range 1-6.
  - Edge cases: `dice_count == 0`, negative input.
  - Note: random output — seed `random` or assert on length/value range.

- [ ] `print_score_table(mydict) -> None`
  - Prints score table; capture stdout to assert formatting.

- [ ] `is_valid_selection(dice_values, user_selection) -> bool`
  - Empty selection -> False.
  - Single `0` (keep all) / `9` (rethrow all) -> True.
  - Length > 5 -> False.
  - Valid digits 1-5 -> True.
  - **Bug:** falls through to `return None` when `count != slen` (no explicit `False`).
  - **Bug:** `slen == 1` branch compares against ints `0`/`9` but input may be str/int depending on caller.

- [ ] `get_dice_retrow_selection() -> list`
  - Reads from STDIN; mock `input()`.
  - Converts each char to int — will raise `ValueError` on non-digit input (untested path).

- [ ] `single_move() -> list`
  - Core loop: 3 throw attempts, keep/rethrow logic.
  - **Bug (commit 7682b8e):** selection of dice to keep does not work — kept dice values are discarded; each throw regenerates fresh dice instead of preserving kept ones.
  - Returns first throw on `0` selection.
  - Hard to test due to STDIN + randomness — mock both.

- [ ] `user_save_input() -> list`
  - Loops until valid option in save_opts; mock `input()`.
  - Note: docstring says returns list, actually returns str.

- [ ] `calculate_score(dest_opt, dice_values, point_value)`
  - **Dead/duplicate code** — superseded by `update_score_table`.
  - **Bug:** `point_value` is a str ("0"), compared/added to ints.
  - Consider deleting rather than testing.

- [ ] `update_score_table(save_input, score) -> None`
  - For each category sums matching dice * face value into table.
  - **Bug (#TODO line 16):** table keys have trailing spaces ("ones  ") — verify keys match.
  - Lots of duplicated branches — candidate for refactor before testing.

- [ ] `game_end_score(mydict)`
  - Sums all table values.
  - **Bug:** table initial values are strings ("0"); `+=` on str raises TypeError unless all updated.

## Review Notes (non-test)

- Replace stringly-typed table values ("0") with ints to avoid type errors.
- Remove trailing spaces from table keys; use clean keys for lookups.
- Deduplicate `update_score_table` into a single data-driven loop.
- Remove dead `calculate_score` function.
- Several typos in messages/docstrings ("Rises" -> "Raises", "Invalit", "piont", "choise", "lenght", "trow").
- Separate I/O from logic so functions are testable without mocking STDIN.

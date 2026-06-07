# Text-based-dice-game

[![CI](https://github.com/vfedotovs/Text-based-dice-game/actions/workflows/ci.yml/badge.svg)](https://github.com/vfedotovs/Text-based-dice-game/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A single-player, text-based, Yahtzee-style dice game for the terminal.

Roll five dice, choose which to keep, reroll the rest, and bank your points into
a scoring category. Play all thirteen categories — the six upper-section faces
plus the seven lower-section combinations — for the highest total.

## Install

From source (until the package is published to PyPI):

```bash
git clone https://github.com/vfedotovs/Text-based-dice-game.git
cd Text-based-dice-game
pip install .
```

For development, install in editable mode with the dev extras:

```bash
pip install -e ".[dev]"
```

## Usage

After installing, start a game with either:

```bash
dice-game
# or
python -m dice_game
```

A turn looks like this:

```
==== My Score Table ====
  -- Upper section --
  ones            -> -
  twos            -> -
  threes          -> -
  fours           -> -
  fives           -> -
  sixes           -> -
  ---------------------
  subtotal        -> 0
  bonus           -> 0  (63+ earns 35)
  -- Lower section --
  three_of_a_kind -> -
  four_of_a_kind  -> -
  full_house      -> -
  small_straight  -> -
  large_straight  -> -
  yahtzee         -> -
  chance          -> -

Throw 1 — current dice: [3, 3, 1, 6, 3]
Positions to keep (1-5), or 0 to keep all: 124
...
Final dice: [3, 3, 3, 5, 3]
Save points to which category? (...): threes
```

Unfilled categories show as `-`; once played a category holds its score (which
may legitimately be `0`).

## Rules

- The game lasts **13 turns** — one per category.
- Each turn you get an initial roll of **5 dice** plus up to **2 rerolls**
  (3 rolls total).
- Before each reroll you choose which dice to **keep** by entering their
  positions (e.g. `135`). Entering `0` keeps every die and ends the turn early.
- After the final roll you pick an unfilled category to **save** your dice into.

### Upper section

The score is the **sum of the dice matching the category's face value** — e.g.
scoring `threes` on `[3, 3, 1, 3, 6]` gives `9`. If the six upper categories
total **63 or more**, you earn a **35-point bonus**.

### Lower section

| Category | Requirement | Score |
| --- | --- | --- |
| `three_of_a_kind` | 3+ dice of the same face | sum of all 5 dice |
| `four_of_a_kind` | 4+ dice of the same face | sum of all 5 dice |
| `full_house` | a three-of-a-kind **and** a pair | 25 |
| `small_straight` | 4 consecutive faces | 30 |
| `large_straight` | 5 consecutive faces | 40 |
| `yahtzee` | 5 of a kind | 50 |
| `chance` | any dice | sum of all 5 dice |

A category that doesn't meet its requirement scores **0**.

- Your final score is the sum of all played categories plus any upper bonus.

## Development

```bash
pip install -e ".[dev]"
pre-commit install        # optional: run hooks on every commit

ruff check .              # lint
ruff format .            # format
mypy                      # static type-check (strict)
pytest                    # run the test suite
pytest --cov=dice_game    # with coverage
```

The project uses a **src layout**:

```
src/dice_game/
  dice.py       # pure dice logic (rolling, selection, reroll)
  scoring.py    # pure scoring logic
  game.py       # turn orchestration
  cli.py        # all input/output + the game loop
tests/          # pytest suite mirroring the package
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and
[RELEASING.md](RELEASING.md) for the release process.

## License

[MIT](LICENSE) © Valentins Fedotovs

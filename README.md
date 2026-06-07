# Text-based-dice-game

[![CI](https://github.com/vfedotovs/Text-based-dice-game/actions/workflows/ci.yml/badge.svg)](https://github.com/vfedotovs/Text-based-dice-game/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A single-player, text-based, Yahtzee-style dice game for the terminal.

Roll five dice, choose which to keep, reroll the rest, and bank your points into
one of six categories. Play all six categories for the highest total.

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
  ones   -> 0
  twos   -> 0
  threes -> 0
  fours  -> 0
  fives  -> 0
  sixes  -> 0

Throw 1 — current dice: [3, 3, 1, 6, 3]
Positions to keep (1-5), or 0 to keep all: 124
...
Final dice: [3, 3, 3, 5, 3]
Save points to which category? (ones, twos, threes, fours, fives, sixes): threes
```

## Rules

- The game lasts **6 turns** — one per category (`ones` … `sixes`).
- Each turn you get an initial roll of **5 dice** plus up to **2 rerolls**
  (3 rolls total).
- Before each reroll you choose which dice to **keep** by entering their
  positions (e.g. `135`). Entering `0` keeps every die and ends the turn early.
- After the final roll you pick a category to **save** your dice into. The score
  for a category is the **sum of the dice matching its face value** — e.g.
  scoring `threes` on `[3, 3, 1, 3, 6]` gives `9`.
- Your final score is the sum of all six categories.

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

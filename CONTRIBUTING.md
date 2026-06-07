# Contributing

Thanks for your interest in improving Text-based-dice-game! This is a small
hobby project, but it follows a few professional conventions to stay tidy.

## Getting set up

```bash
git clone https://github.com/vfedotovs/Text-based-dice-game.git
cd Text-based-dice-game
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Workflow

1. Create a branch off `main` (e.g. `fix/...`, `feat/...`, `docs/...`).
2. Make your change, keeping logic and I/O separated:
   - pure logic in `dice.py` / `scoring.py` / `game.py`,
   - all `print`/`input` in `cli.py`.
3. Add or update tests under `tests/`.
4. Run the full local gate (CI runs the same checks):

   ```bash
   ruff check .
   ruff format --check .
   mypy
   pytest --cov=dice_game
   ```

5. Update `CHANGELOG.md` under the `[Unreleased]` section if your change is
   user-facing.
6. Open a pull request against `main`.

## Conventions

- **Style/formatting:** ruff (line length 88). Run `ruff format .`.
- **Types:** full type hints; `mypy --strict` must pass.
- **Tests:** pytest; keep randomness deterministic by injecting a seeded
  `random.Random` (logic) or monkeypatching `random` / `input` (CLI).
- **Commits:** clear, imperative subject lines.

## Releases

Maintainers: see [RELEASING.md](RELEASING.md).

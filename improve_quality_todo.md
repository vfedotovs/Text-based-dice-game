# Improve Quality TODO — Path to a Professional Python Project

Current state: single `main.py` (~290 lines mixing game logic + I/O), one-line
`README.md`, a `.gitignore`. No package layout, tests, CI, packaging, or docs.

This is a roadmap to take it from a beginner script to a professional,
installable, tested, and documented Python project.

---

## 1. Target Folder Structure

Adopt the modern **src layout** (prevents accidental imports of the local dir
and forces you to test the installed package):

```
Text-based-dice-game/
├── src/
│   └── dice_game/
│       ├── __init__.py        # package version, public API
│       ├── __main__.py        # `python -m dice_game` entry point
│       ├── cli.py             # input/output, the game loop (main())
│       ├── dice.py            # generate_random_dices, selection validation
│       ├── scoring.py         # update_score_table, calculate_score, totals
│       └── game.py            # single_move, turn orchestration
├── tests/
│   ├── __init__.py
│   ├── test_dice.py
│   ├── test_scoring.py
│   └── test_game.py
├── docs/
│   ├── index.md
│   └── rules.md               # how the dice game is played
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore                 # already present
├── pyproject.toml             # build + tooling config (single source of truth)
├── README.md                  # expand (see section 7)
├── LICENSE                    # pick one (MIT is common for hobby projects)
├── CHANGELOG.md               # keep-a-changelog format
└── CONTRIBUTING.md            # optional but professional
```

---

## 2. Refactor `main.py` Into a Package (DONE)

The biggest blocker to professionalism is that logic and I/O are tangled, which
makes testing nearly impossible. Steps:

- [x] Create `src/dice_game/` and move code into the modules above
      (`dice.py`, `scoring.py`, `game.py`, `cli.py`, `__main__.py`, `__init__.py`).
- [x] **Separate pure logic from I/O.** `dice.py` and `scoring.py` are pure
      (args in, values out); `game.play_turn` takes a `prompt_keep` callable so
      it has no I/O of its own.
- [x] Push all `print()`/`input()` into `cli.py`.
- [x] Fix the open bugs: int score table (no more strings), clean keys (no
      trailing spaces), `single_move`→`play_turn` now preserves kept dice across
      rerolls, validation returns explicit `bool`.
- [x] Replace the module-level mutable `table` dict with a factory
      `scoring.new_score_table()` so each game/test gets fresh state.
- [x] Add type hints throughout and a `py.typed` marker file.

> Note: `roll_dice`/`reroll`/`play_turn` accept an injectable `rng` for
> deterministic tests. `main.py` at the repo root is now a thin transitional
> shim (adds `src/` to the path) and should be deleted once §3 packaging lands.

---

## 3. Packaging — `pyproject.toml`

- [ ] Create `pyproject.toml` with a PEP 621 `[project]` table (name, version,
      description, authors, `requires-python`, dependencies).
- [ ] Use a modern build backend (`hatchling` or `setuptools`).
- [ ] Define a console entry point so the game installs as a command:
      ```toml
      [project.scripts]
      dice-game = "dice_game.cli:main"
      ```
- [ ] Add an optional dev dependency group:
      ```toml
      [project.optional-dependencies]
      dev = ["pytest", "pytest-cov", "ruff", "mypy"]
      ```
- [ ] After this, `pip install -e ".[dev]"` sets up a full dev environment.

---

## 4. Tooling / Code Quality

- [ ] **Ruff** for linting + formatting (replaces flake8/black/isort). Configure
      in `pyproject.toml`.
- [ ] **mypy** for static type checking.
- [ ] **pre-commit** (`.pre-commit-config.yaml`) running ruff + mypy on commit.
- [ ] Add an `EditorConfig` (`.editorconfig`) for consistent whitespace.

---

## 5. Tests

- [ ] Use **pytest**. Mirror the package structure under `tests/`.
- [ ] Test pure functions directly (now easy after the I/O split).
- [ ] For randomness: seed `random.seed()` or inject a RNG; assert on
      length/range invariants.
- [ ] For CLI: use `monkeypatch`/`capsys` to mock `input()` and capture stdout.
- [ ] Track coverage with `pytest-cov`; aim for a sensible target (e.g. 80%+).
- [ ] See `todo_inplement_tests.md` for the per-function test checklist.

---

## 6. CI/CD — GitHub Actions

- [ ] `.github/workflows/ci.yml` triggered on push + PR:
      - Matrix over Python versions (e.g. 3.10–3.13).
      - Steps: checkout → setup-python → `pip install -e ".[dev]"` →
        `ruff check` → `ruff format --check` → `mypy` → `pytest --cov`.
      - Upload coverage (optional: Codecov).
- [ ] **Release workflow** (`release.yml`) triggered on a version tag (`v*`):
      - Build with `python -m build`.
      - Publish to PyPI via **trusted publishing** (OIDC, no API token), or
        attach the wheel/sdist to a GitHub Release.
- [ ] Add status badges (CI, coverage, PyPI version) to the README.

---

## 7. Release Process

- [ ] Adopt **Semantic Versioning** (MAJOR.MINOR.PATCH).
- [ ] Single source of version (e.g. `__version__` in `__init__.py` or
      hatch-vcs deriving it from git tags).
- [ ] Maintain `CHANGELOG.md` (keep-a-changelog style).
- [ ] Release checklist: bump version → update changelog → tag `vX.Y.Z` →
      push tag → CI builds & publishes.

---

## 8. Documentation

- [ ] **Rewrite `README.md`** to include:
      - Project description + a short demo (asciinema GIF or sample session).
      - Install instructions (`pip install dice-game` or from source).
      - Usage / how to run (`dice-game` or `python -m dice_game`).
      - Game rules summary.
      - Development setup, running tests, contributing pointer.
      - Badges + license.
- [ ] Add `LICENSE`, `CONTRIBUTING.md`, and a `CHANGELOG.md`.
- [ ] Optional: full docs site with **MkDocs (Material theme)** under `docs/`,
      auto-deployed to GitHub Pages via Actions.
- [ ] Add docstrings (already partially present — fix typos: "Rises"→"Raises").

---

## Suggested Order of Work

1. Refactor into `src/dice_game/` package + split logic/I/O (§2)
2. Add `pyproject.toml` + dev install (§3)
3. Add ruff/mypy/pre-commit (§4)
4. Write tests (§5)
5. Add CI workflow (§6)
6. Expand README + add LICENSE/CHANGELOG (§7, §8)
7. Add release workflow + first tagged release (§6, §7)
8. (Optional) MkDocs site + GitHub Pages (§8)

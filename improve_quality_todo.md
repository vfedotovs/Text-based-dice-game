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

## 3. Packaging — `pyproject.toml` (DONE)

- [x] Create `pyproject.toml` with a PEP 621 `[project]` table (name, version,
      description, authors, `requires-python >=3.10`, classifiers, URLs).
- [x] Use a modern build backend (**hatchling**); version is single-sourced
      from `src/dice_game/__init__.py` via `[tool.hatch.version]`.
- [x] Define a console entry point so the game installs as a command:
      `dice-game = "dice_game.cli:main"`.
- [x] Add an optional dev dependency group
      (`pytest`, `pytest-cov`, `ruff`, `mypy`).
- [x] Verified `pip install -e ".[dev]"` works and `dice-game` runs; verified
      `python -m build` produces a wheel + sdist containing all modules and
      `py.typed`.

> Next: §4 tooling config (ruff/mypy in this same `pyproject.toml`) and §5
> tests. The root `main.py` shim can now be deleted in favour of `dice-game`.

---

## 4. Tooling / Code Quality (DONE)

- [x] **Ruff** for linting + formatting, configured in `pyproject.toml`
      (`E,W,F,I,UP,B,C4,SIM` rule set, line length 88). `ruff check` and
      `ruff format --check` both pass.
- [x] **mypy** in `--strict` mode, configured in `pyproject.toml` — passes with
      no issues across `src`. (Add `tests` to `files` once §5 lands.)
- [x] **pre-commit** (`.pre-commit-config.yaml`) running ruff, ruff-format,
      mypy, and a few hygiene hooks. Enable with `pre-commit install`.
- [x] Added `.editorconfig` for consistent whitespace/indentation.
- [x] Also added `[tool.pytest.ini_options]` (with `pythonpath = ["src"]`) to
      `pyproject.toml` so the §5 test suite runs without an install.

---

## 5. Tests (DONE)

- [x] Use **pytest**, mirroring the package structure under `tests/`
      (`test_dice.py`, `test_scoring.py`, `test_game.py`, `test_cli.py`).
- [x] Test pure functions directly (easy after the I/O split).
- [x] Randomness handled via injected `random.Random(seed)` / monkeypatched
      `random.randint`; assertions on length/range invariants.
- [x] CLI driven with `monkeypatch` (`input`) and `capsys` (stdout), including a
      full `main()` game played end-to-end.
- [x] Coverage via `pytest-cov`: **96%** (only entry-point `__main__`/`__name__`
      guards uncovered). 56 tests passing.
- [x] `tests` added to the mypy `files` list; ruff + mypy clean on tests too.
- [x] Per-function checklist in `todo_inplement_tests.md` all ticked.

---

## 6. CI/CD — GitHub Actions (DONE)

- [x] `.github/workflows/ci.yml` triggered on push + PR to `main`:
      - `lint` job: `ruff check` → `ruff format --check` → `mypy` (on 3.12).
      - `test` job: matrix over Python 3.10–3.13 running `pytest --cov`.
      - Concurrency cancels superseded runs; least-privilege `permissions`.
      - Codecov upload stubbed (commented) pending an account/token.
- [x] **Release workflow** (`release.yml`) triggered on a version tag (`v*`):
      - `build` job: `python -m build` + `twine check`, uploads artifacts.
      - `github-release` job: attaches wheel/sdist to an auto-noted GitHub
        Release.
      - PyPI Trusted Publishing (OIDC) job stubbed (commented) pending a
        configured publisher on PyPI.
- [x] Added a CI status badge to the README (coverage/PyPI badges to follow in
      §8 once Codecov/PyPI are wired up).

> Both workflow files validated as well-formed YAML; the lint/test commands are
> the same ones already passing locally.

---

## 7. Release Process (DONE)

- [x] Adopt **Semantic Versioning** (MAJOR.MINOR.PATCH) — documented in
      `RELEASING.md`.
- [x] Single source of version: `__version__` in `src/dice_game/__init__.py`,
      read by hatchling at build time (set up in §3).
- [x] Maintain `CHANGELOG.md` (keep-a-changelog style) with a `0.1.0` entry.
- [x] Documented release checklist in `RELEASING.md` (bump → changelog → tag
      `vX.Y.Z` → push → `release.yml` builds & attaches dists).
- [x] Cut the first `v0.1.0` tag to exercise `release.yml`.

---

## 8. Documentation (DONE)

- [x] **Rewrote `README.md`**: description, sample session, install (source +
      editable dev), usage (`dice-game` / `python -m dice_game`), rules summary,
      development gate, src-layout overview, badges, license.
- [x] Added `LICENSE` (MIT), `CONTRIBUTING.md` (and `CHANGELOG.md` in §7).
- [x] Docstrings present across the package with typos fixed ("Raises", etc.).
- [ ] ~~Optional MkDocs (Material) site on GitHub Pages~~ — deferred by choice;
      revisit if the project grows. (Needs Pages enabled in repo settings.)

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

# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-07

First packaged release. The original single-file script was rebuilt into a
tested, typed, installable package.

### Added
- `src/dice_game` package with a clean separation of pure logic and I/O:
  `dice`, `scoring`, `game` (logic) and `cli` (I/O).
- `dice-game` console entry point and `python -m dice_game` support.
- `pyproject.toml` packaging (hatchling backend, version single-sourced from
  `dice_game.__version__`, `[dev]` extras).
- Tooling: ruff (lint + format), mypy (`--strict`), pre-commit hooks,
  `.editorconfig`.
- pytest suite (56 tests, 96% coverage) with deterministic randomness.
- GitHub Actions CI (lint + type-check, test matrix over Python 3.10–3.13) and
  a tag-triggered release workflow.

### Fixed
- Kept dice are now preserved across rerolls (previously discarded each throw).
- Score table uses integers with clean keys (was stringly-typed with
  trailing-space keys, which could raise `TypeError` at game end).
- Selection validation always returns a `bool` (was an implicit `None` on one
  path).
- Per-game score state via a factory instead of a shared module-level global.

### Removed
- Dead/duplicate `calculate_score` function.

[Unreleased]: https://github.com/vfedotovs/Text-based-dice-game/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vfedotovs/Text-based-dice-game/releases/tag/v0.1.0

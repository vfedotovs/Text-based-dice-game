# Issue #10 — Wire up Codecov and add coverage/PyPI badges

> FEAT: Wire up Codecov and add coverage/PyPI badges (stubs already in place).

This document proposes a concrete implementation. There are two independent
parts:

1. **Codecov** — actually upload `coverage.xml` from CI and show a coverage
   badge. (Stub already present in `.github/workflows/ci.yml`.)
2. **PyPI badges** — version + supported Python versions. These only render
   once the package is published to PyPI (see issue/§ on PyPI publishing).

---

## Part 1 — Codecov

### 1.1 One-time account setup (manual, outside the repo)

1. Sign in at <https://app.codecov.io> with the GitHub account `vfedotovs` and
   enable the `Text-based-dice-game` repository.
2. Copy the repository's **upload token**.
3. In GitHub: **Settings → Secrets and variables → Actions → New repository
   secret**, name it `CODECOV_TOKEN`, paste the token.

> Public repos *can* upload tokenless, but Codecov now rate-limits tokenless
> uploads and recommends a token even for public projects. Using the secret is
> the reliable choice.

### 1.2 CI change — upload coverage once

The current `test` job runs on a 4-version matrix and already produces
`coverage.xml`. Uploading on every matrix leg would send 4 reports per run;
upload from a single version instead. Replace the commented stub in
`.github/workflows/ci.yml` (lines 64–68) with a real, guarded step:

```yaml
      - name: Run tests with coverage
        run: pytest --cov=dice_game --cov-report=xml --cov-report=term-missing

      - name: Upload coverage to Codecov
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v5
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

Notes:
- `codecov/codecov-action@v5` is the current major (the stub referenced `@v4`).
- `if: matrix.python-version == '3.12'` uploads exactly one report per CI run.
- `fail_ci_if_error: true` surfaces upload problems instead of silently passing.
  If that ever feels too strict, drop it back to the default `false`.

If you prefer to keep coverage reporting fully independent of the version
matrix, an alternative is a dedicated single-version `coverage` job. The guarded
step above is simpler and reuses the existing matrix, so it is the recommended
option.

### 1.3 Optional: `codecov.yml`

Add a small project-root `codecov.yml` to make the bot non-blocking and tidy:

```yaml
coverage:
  status:
    project:
      default:
        target: auto        # compare against the base commit
        threshold: 1%       # allow tiny dips without failing the check
    patch:
      default:
        target: 80%         # new/changed lines should be well covered
comment:
  layout: "reach, diff, files"
  require_changes: true     # only comment on PRs that move coverage
```

### 1.4 Coverage badge

Add to the badge block at the top of `README.md` (after the CI badge):

```markdown
[![codecov](https://codecov.io/gh/vfedotovs/Text-based-dice-game/branch/main/graph/badge.svg)](https://codecov.io/gh/vfedotovs/Text-based-dice-game)
```

The badge becomes live after the first successful upload from `main`.

---

## Part 2 — PyPI badges

The package name in `pyproject.toml` is **`dice-game`**. shields.io reads PyPI
directly, so no extra setup is needed — but the badges 404 / show "not found"
until the package is actually published to PyPI.

### 2.1 Badges

In `README.md`, replace the current static Python badge

```markdown
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
```

with the dynamic PyPI pair (version + the `requires-python` it advertises):

```markdown
[![PyPI](https://img.shields.io/pypi/v/dice-game)](https://pypi.org/project/dice-game/)
[![Python versions](https://img.shields.io/pypi/pyversions/dice-game)](https://pypi.org/project/dice-game/)
```

### 2.2 Sequencing

- If PyPI publishing is **not** done yet, either:
  - keep the static `python-3.10+` badge for now and add the PyPI badges in the
    same PR that enables publishing, **or**
  - add them now and accept a temporary "not found" state until the first
    publish.
- Recommended: land Codecov now (Part 1), and add the PyPI badges as part of
  enabling Trusted Publishing (the commented `pypi-publish` job in
  `release.yml`).

---

## Suggested final README badge block

Once both parts are live:

```markdown
[![CI](https://github.com/vfedotovs/Text-based-dice-game/actions/workflows/ci.yml/badge.svg)](https://github.com/vfedotovs/Text-based-dice-game/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/vfedotovs/Text-based-dice-game/branch/main/graph/badge.svg)](https://codecov.io/gh/vfedotovs/Text-based-dice-game)
[![PyPI](https://img.shields.io/pypi/v/dice-game)](https://pypi.org/project/dice-game/)
[![Python versions](https://img.shields.io/pypi/pyversions/dice-game)](https://pypi.org/project/dice-game/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
```

---

## Implementation checklist

- [ ] Enable the repo on Codecov and add the `CODECOV_TOKEN` GitHub secret.
- [ ] Replace the commented upload stub in `ci.yml` with the guarded
      `codecov/codecov-action@v5` step (single-version upload).
- [ ] (Optional) Add `codecov.yml` with non-blocking thresholds.
- [ ] Add the Codecov badge to `README.md`.
- [ ] Add PyPI version + pyversions badges to `README.md` (with/after the first
      PyPI publish).
- [ ] Open a PR; confirm the CI run uploads coverage and the badge renders.

## Acceptance criteria (from the issue)

- Coverage is uploaded to Codecov from CI on pushes/PRs to `main`.
- The README shows a working **coverage** badge.
- The README shows **PyPI** version (and Python versions) badges (active once
  published).

## Risks / notes

- **Token:** without `CODECOV_TOKEN`, uploads may be rate-limited and flaky.
- **Duplicate uploads:** guarding on a single matrix version avoids 4 uploads
  per run.
- **`fail_ci_if_error`:** makes CI fail on upload errors — intentional, but flip
  to `false` if Codecov outages become annoying.
- **PyPI badge timing:** badges 404 until the package is first published.
- The third-party `codecov/codecov-action` runs on Node 24 at `@v5`, consistent
  with the recent action-version bump (no new deprecation warnings).

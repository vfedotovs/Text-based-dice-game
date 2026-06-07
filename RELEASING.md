# Releasing

This project uses [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`)
and a single source of truth for the version: `__version__` in
`src/dice_game/__init__.py` (read by hatchling at build time).

## Checklist

1. Ensure `main` is green in CI and your working tree is clean.
2. Bump `__version__` in `src/dice_game/__init__.py`.
3. Update `CHANGELOG.md`: move items from `[Unreleased]` into a new
   `[X.Y.Z] - YYYY-MM-DD` section and refresh the compare links at the bottom.
4. Commit: `git commit -am "Release vX.Y.Z"`.
5. Tag and push:
   ```bash
   git tag vX.Y.Z
   git push origin main --tags
   ```
6. The `release.yml` workflow builds the sdist + wheel, runs `twine check`, and
   attaches them to a GitHub Release with auto-generated notes.

## Versioning guide

- **PATCH** — backwards-compatible bug fixes.
- **MINOR** — backwards-compatible new features.
- **MAJOR** — breaking changes.

## PyPI (optional, not yet enabled)

To publish to PyPI, configure a
[Trusted Publisher](https://docs.pypi.org/trusted-publishers/) for this
repository, then uncomment the `pypi-publish` job in `.github/workflows/release.yml`.
No API tokens are needed with OIDC trusted publishing.

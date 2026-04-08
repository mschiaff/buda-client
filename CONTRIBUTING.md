# Contributing to Buda Client

Thanks for your interest in contributing! This project is open to bug reports, feature ideas, documentation improvements, and code contributions of all sizes.

## Reporting Bugs

Found something broken? [Open an issue](https://github.com/mschiaff/buda-client/issues/new) and include:

- A clear description of the problem.
- Steps to reproduce it (minimal code snippet if possible).
- What you expected to happen vs. what actually happened.
- Your Python version and `buda` version (`python --version`, `pip show buda`).

## Suggesting Features

Have an idea? [Open an issue](https://github.com/mschiaff/buda-client/issues/new) describing:

- The problem or use case you're trying to solve.
- How you'd like the API to look (if you have a preference).

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and builds.

```bash
# Clone the repo
git clone https://github.com/mschiaff/buda-client.git
cd buda-client

# Install all dependencies (including dev tools)
uv sync --group dev

# Set up pre-commit hooks (runs ruff automatically on each commit)
uv run pre-commit install
```

### Running Checks

```bash
# Lint and format
uv run ruff check .
uv run ruff format .

# Type checking (strict mode)
uv run pyright

# Tests
uv run pytest

# Tests with coverage report
uv run coverage run --source=src/buda -m pytest
uv run coverage report -m
```

If you installed the pre-commit hooks, ruff will run automatically on each commit. You can also run all hooks manually:

```bash
uv run pre-commit run --all-files
```

Please make sure all checks pass before submitting a pull request.

## Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/). A pre-commit hook validates your commit messages automatically.

Format: `type(scope): description`

| Type       | When to use                        |
|------------|------------------------------------|
| `feat`     | New feature                        |
| `fix`      | Bug fix                            |
| `docs`     | Documentation only                 |
| `style`    | Formatting, no logic change        |
| `refactor` | Code change that neither fixes nor adds |
| `perf`     | Performance improvement            |
| `test`     | Adding or updating tests           |
| `build`    | Build system or dependencies       |
| `ci`       | CI configuration                   |
| `chore`    | Maintenance tasks                  |
| `revert`   | Reverting a previous commit        |

To activate the commit-msg hook:

```bash
uv run pre-commit install --hook-type commit-msg
```

## Code Standards

- **Type hints are required** on all public and private functions. The project uses Pyright in strict mode — your code must pass without errors.
- **Formatting and linting** are handled by [Ruff](https://docs.astral.sh/ruff/). Run `ruff format .` before committing.
- Follow the existing code style. When in doubt, look at how similar things are done elsewhere in the codebase.

## Pull Requests

1. Fork the repository and create a branch from `main`.
2. Make your changes in focused, well-scoped commits.
3. Make sure all checks pass (`ruff check`, `ruff format --check`, `pyright`, `pytest`).
4. Open a pull request against `main` with a clear description of what you changed and why.

## Releasing

Releases are triggered by pushing a `v*` tag to `main`. Two paths are available:

### Option A: Local release (recommended)

Requires [git-cliff](https://git-cliff.org/) (`brew install git-cliff`).

```bash
./scripts/release.sh patch   # 0.1.0 → 0.1.1
./scripts/release.sh minor   # 0.1.0 → 0.2.0
./scripts/release.sh major   # 0.1.0 → 1.0.0
./scripts/release.sh auto    # infer from conventional commits
```

The script will show a summary and ask for confirmation before pushing.

### Option B: GitHub Actions UI

Go to **Actions → Bump Version → Run workflow** and choose the bump type. Use `dry_run: true` to preview.

### What happens after a tag push

The `release.yml` workflow:

1. Runs full CI (lint + tests across Python 3.12/3.13/3.14)
2. Builds the sdist and wheel
3. Creates a GitHub Release with auto-generated changelog
4. Publishes to PyPI via trusted publishers

### Tag convention

Tags follow `v{major}.{minor}.{patch}` — e.g., `v0.1.0`, `v0.2.0`, `v1.0.0`.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers this project.

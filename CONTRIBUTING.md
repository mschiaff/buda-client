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

Please make sure all checks pass before submitting a pull request.

## Code Standards

- **Type hints are required** on all public and private functions. The project uses Pyright in strict mode — your code must pass without errors.
- **Formatting and linting** are handled by [Ruff](https://docs.astral.sh/ruff/). Run `ruff format .` before committing.
- Follow the existing code style. When in doubt, look at how similar things are done elsewhere in the codebase.

## Pull Requests

1. Fork the repository and create a branch from `main`.
2. Make your changes in focused, well-scoped commits.
3. Make sure all checks pass (`ruff check`, `ruff format --check`, `pyright`, `pytest`).
4. Open a pull request against `main` with a clear description of what you changed and why.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers this project.

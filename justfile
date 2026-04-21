[default]
_list:
    @just --list

# Lint Python files with Ruff.
lint:
    uv run ruff check .

# Format Python files with Ruff.
format:
    uv run ruff format

# Type-check Python files with ty.
type:
    uv run ty check .

# Run the test suite.
test:
    uv run pytest -v -s --cov=src tests

# Build and publish the package.
publish:
    uv build --wheel
    uv publish

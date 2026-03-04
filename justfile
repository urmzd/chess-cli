# Format check
fmt:
    uv run ruff format --check .

# Format fix
fmt-fix:
    uv run ruff format .

# Lint
lint:
    uv run ruff check .

# Lint fix
lint-fix:
    uv run ruff check --fix .

# Type-check
typecheck:
    uv run mypy src/chess_cli

# Run tests
test:
    uv run pytest

# Run the game
run:
    uv run python -m chess_cli

# Full CI check
ci: fmt lint typecheck test

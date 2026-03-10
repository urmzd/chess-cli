# AGENTS.md

## Identity

You are an agent working on **chess-cli** — a terminal-based chess game with an AI opponent, built in Python using Textual TUI framework. The AI uses minimax with alpha-beta pruning.

## Architecture

Two packages under `src/` with a clean separation:

| Package | Path | Role |
|---------|------|------|
| `chess_core` | `src/chess_core/` | Pure game logic — no UI dependency |
| `chess_cli` | `src/chess_cli/` | Textual TUI application |

```
src/
├── chess_core/          # Pure game logic
│   ├── models/          # Frozen Pydantic models (Piece, Move, GameState)
│   ├── rules/           # Board ops, move generation, check/checkmate detection
│   └── engine/          # Static evaluation + minimax with alpha-beta pruning
└── chess_cli/           # Textual TUI
    ├── app.py           # ChessApp entry point
    ├── app.tcss         # Terminal stylesheet
    ├── screens/         # GameScreen
    └── widgets/         # ChessBoard, ChessSquare, CommandInput, MoveLog
```

All game state is immutable — every move produces a new `GameState` with no mutation.

## Key Files

- `src/chess_cli/__main__.py` — Entry point (`main()`)
- `src/chess_core/models/` — Frozen Pydantic models
- `src/chess_core/engine/` — Minimax AI with alpha-beta pruning
- `src/chess_core/rules/` — Move generation, check/checkmate
- `src/chess_cli/app.py` — Textual app
- `src/chess_cli/widgets/` — Board, squares, command input, move log
- `tests/` — pytest tests

## Commands

| Task | Command |
|------|---------|
| Run game | `just run` or `uv run chess-cli` |
| Test | `just test` or `uv run pytest` |
| Lint | `just lint` or `uv run ruff check .` |
| Format check | `just fmt` or `uv run ruff format --check .` |
| Format fix | `just fmt-fix` or `uv run ruff format .` |
| Type-check | `just typecheck` or `uv run mypy src/chess_cli` |
| Full CI | `just ci` (fmt + lint + typecheck + test) |

## Code Style

- Python 3.12+, Apache-2.0 license
- `ruff` for formatting and linting (line-length 100)
- `mypy` for type checking
- `pydantic>=2.0` with frozen models for immutable state
- `textual>=1.0` for TUI
- Conventional Commits enforced via pre-commit hook

## Modifying the AI

The AI engine is in `src/chess_core/engine/`. It uses:
- Static board evaluation (piece values, positional bonuses)
- Minimax search with alpha-beta pruning
- Configurable search depth

To improve the AI, modify the evaluation function or increase search depth.

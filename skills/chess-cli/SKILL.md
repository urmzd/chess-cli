---
name: chess-cli
description: Play terminal chess against an AI opponent with minimax alpha-beta pruning. Use when launching, debugging, or developing the chess game.
argument-hint: [command]
disable-model-invocation: true
---

# Chess CLI

Play chess in the terminal.

## Launch

```sh
uv run chess-cli
# or
just run
```

## Gameplay

- **Mouse**: Click a piece to select, click a green-highlighted square to move
- **Keyboard**: Type moves like `e2e4`, promotions like `a7a8q`
- **Commands**: `help`, `new` (new game), `quit`

## Development

```sh
just ci          # Full check (fmt + lint + typecheck + test)
just test        # Run pytest
just typecheck   # Run mypy
just lint        # Run ruff check
```

## Architecture

- `chess_core` — Pure game logic (immutable Pydantic models, move generation, minimax AI)
- `chess_cli` — Textual TUI (board widget, command input, move log)

All state is immutable. Every move produces a new `GameState`.

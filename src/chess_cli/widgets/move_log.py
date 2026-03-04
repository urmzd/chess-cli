from __future__ import annotations

from textual.containers import VerticalScroll
from textual.widgets import Static

from chess_core.models.move import Move
from chess_core.rules.board_ops import move_to_string


class MoveLog(VerticalScroll):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._moves: list[str] = []

    def add_move(self, move: Move) -> None:
        self._moves.append(move_to_string(move))
        self._render_moves()

    def clear_moves(self) -> None:
        self._moves = []
        self._render_moves()

    def compose(self):
        yield Static("", id="move-text")

    def _render_moves(self) -> None:
        lines: list[str] = []
        for i in range(0, len(self._moves), 2):
            num = i // 2 + 1
            white_move = self._moves[i]
            black_move = self._moves[i + 1] if i + 1 < len(self._moves) else ""
            lines.append(f"{num:>3}. {white_move:<8}{black_move}")

        self.query_one("#move-text", Static).update("\n".join(lines))
        self.scroll_end(animate=False)

from __future__ import annotations

from textual.containers import Container
from textual.message import Message

from chess_cli.widgets.square import ChessSquare
from chess_core.models.game import GameState
from chess_core.models.move import Move, Position
from chess_core.rules.constants import PIECE_ICONS
from chess_core.rules.movement import get_legal_moves


class ChessBoard(Container):
    class MoveRequested(Message):
        def __init__(self, move: Move) -> None:
            super().__init__()
            self.move = move

    def __init__(self, state: GameState, **kwargs) -> None:
        super().__init__(**kwargs)
        self.game_state = state
        self.selected_pos: Position | None = None
        self.legal_targets: list[Move] = []

    def compose(self):
        # Render board from rank 8 (top) to rank 1 (bottom)
        for rank in range(7, -1, -1):
            for file in range(8):
                pos = Position(x=file, y=rank)
                is_light = (file + rank) % 2 == 1
                content = self._square_content(file, rank)
                square = ChessSquare(
                    pos,
                    content,
                    is_light=is_light,
                    id=f"sq-{file}-{rank}",
                )
                yield square

    def _square_content(self, x: int, y: int) -> str:
        piece = self.game_state.grid[y][x]
        if piece is None:
            return "\u00b7"
        return PIECE_ICONS.get((piece.team, piece.piece_type), "?")

    def refresh_board(self, state: GameState) -> None:
        self.game_state = state
        self.selected_pos = None
        self.legal_targets = []
        for rank in range(8):
            for file in range(8):
                sq = self.query_one(f"#sq-{file}-{rank}", ChessSquare)
                sq.update(self._square_content(file, rank))
                sq.remove_class("selected", "legal-target", "last-move")

        if state.last_move:
            lm = state.last_move
            self._get_square(lm.from_pos).add_class("last-move")
            self._get_square(lm.to_pos).add_class("last-move")

    def _get_square(self, pos: Position) -> ChessSquare:
        return self.query_one(f"#sq-{pos.x}-{pos.y}", ChessSquare)

    def on_chess_square_clicked(self, event: ChessSquare.Clicked) -> None:
        pos = event.pos
        piece = self.game_state.grid[pos.y][pos.x]

        if self.selected_pos is not None:
            # Check if clicked square is a legal target
            for move in self.legal_targets:
                if move.to_pos == pos:
                    self._clear_highlights()
                    self.post_message(self.MoveRequested(move))
                    return

            # Clicking own piece switches selection
            if piece is not None and piece.team == self.game_state.turn:
                self._clear_highlights()
                self._select(pos)
                return

            # Otherwise deselect
            self._clear_highlights()
            return

        # No selection yet — select if it's current team's piece
        if piece is not None and piece.team == self.game_state.turn:
            self._select(pos)

    def _select(self, pos: Position) -> None:
        self.selected_pos = pos
        self.legal_targets = get_legal_moves(self.game_state, pos)
        self._get_square(pos).add_class("selected")
        for move in self.legal_targets:
            self._get_square(move.to_pos).add_class("legal-target")

    def _clear_highlights(self) -> None:
        if self.selected_pos:
            self._get_square(self.selected_pos).remove_class("selected")
        for move in self.legal_targets:
            self._get_square(move.to_pos).remove_class("legal-target")
        self.selected_pos = None
        self.legal_targets = []

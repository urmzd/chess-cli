from __future__ import annotations

from typing import ClassVar

from textual import work
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from chess_cli.widgets.board import ChessBoard
from chess_cli.widgets.command_input import CommandInput
from chess_cli.widgets.move_log import MoveLog
from chess_core.models.enums import GameStatus, PieceType, Team
from chess_core.models.game import GameState
from chess_core.models.move import Move
from chess_core.rules.board_ops import apply_move, parse_move_string


class GameScreen(Screen):
    BINDINGS: ClassVar[list] = [  # type: ignore[assignment]
        ("q", "quit_game", "Quit"),
        ("n", "new_game", "New Game"),
    ]

    def __init__(
        self,
        state: GameState,
        ai_team: Team | None = None,
        ai_depth: int = 3,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.game_state = state
        self.ai_team = ai_team
        self.ai_depth = ai_depth

    def compose(self):
        yield Header()
        with Horizontal(id="main-area"):
            with Vertical(id="board-panel"):
                yield Static(self._file_labels(), id="top-files", classes="file-labels")
                yield ChessBoard(self.game_state, id="chess-board")
                yield Static(self._file_labels(), id="bottom-files", classes="file-labels")
            with Vertical(id="side-panel"):
                yield Static(self._status_text(), id="status-label")
                yield MoveLog(id="move-log")
        yield CommandInput(id="command-input")
        yield Footer()

    def _file_labels(self) -> str:
        return "    a   b   c   d   e   f   g   h"

    def _status_text(self) -> str:
        s = self.game_state
        turn = "White" if s.turn == Team.WHITE else "Black"
        if s.status == GameStatus.CHECKMATE:
            winner = "Black" if s.turn == Team.WHITE else "White"
            return f"Checkmate! {winner} wins!"
        if s.status == GameStatus.STALEMATE:
            return "Stalemate! Draw."
        if s.status == GameStatus.DRAW:
            return "Draw by 50-move rule."
        if s.status == GameStatus.CHECK:
            return f"{turn}'s Turn (CHECK!)"
        return f"{turn}'s Turn"

    def _apply_and_update(self, move: Move) -> None:
        self.game_state = apply_move(self.game_state, move)
        board = self.query_one("#chess-board", ChessBoard)
        board.refresh_board(self.game_state)
        self.query_one("#move-log", MoveLog).add_move(move)
        self.query_one("#status-label", Static).update(self._status_text())

        if self.game_state.status in (
            GameStatus.CHECKMATE,
            GameStatus.STALEMATE,
            GameStatus.DRAW,
        ):
            return

        # Trigger AI if it's AI's turn
        if self.ai_team is not None and self.game_state.turn == self.ai_team:
            self._run_ai()

    @work(thread=True, exclusive=True)
    def _run_ai(self) -> None:
        from chess_core.engine.minimax import best_move

        status_label = self.query_one("#status-label", Static)
        self.app.call_from_thread(status_label.update, "AI thinking...")

        move = best_move(self.game_state, self.ai_depth)
        if move is not None:
            self.app.call_from_thread(self._apply_and_update, move)

    def on_chess_board_move_requested(self, event: ChessBoard.MoveRequested) -> None:
        if self.game_state.status in (
            GameStatus.CHECKMATE,
            GameStatus.STALEMATE,
            GameStatus.DRAW,
        ):
            return
        # If it's AI's turn, ignore human clicks
        if self.ai_team is not None and self.game_state.turn == self.ai_team:
            return

        move = event.move

        # Handle promotion: if move needs promotion but doesn't have one, default to queen
        piece = self.game_state.grid[move.from_pos.y][move.from_pos.x]
        if piece is not None and piece.piece_type == PieceType.PAWN and move.promotion is None:
            promo_rank = 7 if piece.team == Team.WHITE else 0
            if move.to_pos.y == promo_rank:
                move = move.model_copy(update={"promotion": PieceType.QUEEN})

        self._apply_and_update(move)

    def on_command_input_command_submitted(self, event: CommandInput.CommandSubmitted) -> None:
        cmd = event.value.lower()

        if cmd in ("quit", "q"):
            self.app.exit()
            return

        if cmd in ("new", "n"):
            self.action_new_game()
            return

        if cmd in ("help", "h"):
            status = self.query_one("#status-label", Static)
            status.update("Commands: move (e2e4), quit, new, help")
            return

        if self.game_state.status in (
            GameStatus.CHECKMATE,
            GameStatus.STALEMATE,
            GameStatus.DRAW,
        ):
            return

        if self.ai_team is not None and self.game_state.turn == self.ai_team:
            return

        move = parse_move_string(self.game_state, cmd)
        if move is None:
            status = self.query_one("#status-label", Static)
            status.update(f"Invalid move: {cmd}")
            return

        self._apply_and_update(move)

    def action_quit_game(self) -> None:
        self.app.exit()

    def action_new_game(self) -> None:
        from chess_core.rules.board_ops import initial_state

        self.game_state = initial_state()
        self.query_one("#chess-board", ChessBoard).refresh_board(self.game_state)
        self.query_one("#move-log", MoveLog).clear_moves()
        self.query_one("#status-label", Static).update(self._status_text())

        if self.ai_team == Team.WHITE:
            self._run_ai()

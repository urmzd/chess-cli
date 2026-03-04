import pytest
from pydantic import ValidationError

from chess_core.models.enums import GameStatus, PieceType, Team
from chess_core.models.game import GameState
from chess_core.models.move import Move, Position
from chess_core.models.piece import Piece


class TestPiece:
    def test_create_piece(self):
        p = Piece(piece_type=PieceType.PAWN, team=Team.WHITE)
        assert p.piece_type == PieceType.PAWN
        assert p.team == Team.WHITE
        assert p.has_moved is False

    def test_frozen(self):
        p = Piece(piece_type=PieceType.KING, team=Team.BLACK)
        with pytest.raises(ValidationError):
            p.team = Team.WHITE

    def test_model_copy(self):
        p = Piece(piece_type=PieceType.ROOK, team=Team.WHITE)
        p2 = p.model_copy(update={"has_moved": True})
        assert p.has_moved is False
        assert p2.has_moved is True


class TestPosition:
    def test_valid(self):
        pos = Position(x=0, y=7)
        assert pos.x == 0
        assert pos.y == 7

    def test_out_of_bounds(self):
        with pytest.raises(ValidationError):
            Position(x=-1, y=0)
        with pytest.raises(ValidationError):
            Position(x=0, y=8)


class TestMove:
    def test_basic_move(self):
        m = Move(from_pos=Position(x=4, y=1), to_pos=Position(x=4, y=3))
        assert m.promotion is None
        assert m.is_castling is False
        assert m.is_en_passant is False

    def test_promotion(self):
        m = Move(
            from_pos=Position(x=0, y=6),
            to_pos=Position(x=0, y=7),
            promotion=PieceType.QUEEN,
        )
        assert m.promotion == PieceType.QUEEN


class TestGameState:
    def test_initial_defaults(self):
        grid = tuple(tuple(None for _ in range(8)) for _ in range(8))
        state = GameState(grid=grid, turn=Team.WHITE)
        assert state.last_move is None
        assert state.half_move_clock == 0
        assert state.move_history == ()
        assert state.status == GameStatus.PLAYING

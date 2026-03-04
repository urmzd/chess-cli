from chess_core.models.enums import GameStatus, PieceType, Team
from chess_core.models.game import GameState
from chess_core.models.piece import Piece
from chess_core.rules.check import compute_status, is_checkmate, is_in_check, is_stalemate


def _empty_grid():
    return tuple(tuple(None for _ in range(8)) for _ in range(8))


def _place(grid, x, y, piece):
    grid_list = [list(row) for row in grid]
    grid_list[y][x] = piece
    return tuple(tuple(row) for row in grid_list)


class TestIsInCheck:
    def test_not_in_check_initial(self):
        from chess_core.rules.board_ops import initial_state

        state = initial_state()
        assert is_in_check(state, Team.WHITE) is False
        assert is_in_check(state, Team.BLACK) is False

    def test_in_check_by_rook(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 4, 7, Piece(piece_type=PieceType.ROOK, team=Team.BLACK))
        grid = _place(grid, 0, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        assert is_in_check(state, Team.WHITE) is True


class TestCheckmate:
    def test_back_rank_mate(self):
        grid = _empty_grid()
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 0, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 1, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 7, 0, Piece(piece_type=PieceType.ROOK, team=Team.BLACK))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        assert is_checkmate(state, Team.WHITE) is True


class TestStalemate:
    def test_stalemate(self):
        grid = _empty_grid()
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 2, 1, Piece(piece_type=PieceType.QUEEN, team=Team.BLACK))
        grid = _place(grid, 1, 2, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        assert is_stalemate(state, Team.WHITE) is True
        assert is_checkmate(state, Team.WHITE) is False


class TestComputeStatus:
    def test_playing(self):
        from chess_core.rules.board_ops import initial_state

        state = initial_state()
        assert compute_status(state) == GameStatus.PLAYING

    def test_checkmate_status(self):
        grid = _empty_grid()
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 0, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 1, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 7, 0, Piece(piece_type=PieceType.ROOK, team=Team.BLACK))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        assert compute_status(state) == GameStatus.CHECKMATE

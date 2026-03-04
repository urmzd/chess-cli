from chess_core.engine.minimax import best_move
from chess_core.models.enums import PieceType, Team
from chess_core.models.game import GameState
from chess_core.models.piece import Piece
from chess_core.rules.board_ops import initial_state


def _empty_grid():
    return tuple(tuple(None for _ in range(8)) for _ in range(8))


def _place(grid, x, y, piece):
    grid_list = [list(row) for row in grid]
    grid_list[y][x] = piece
    return tuple(tuple(row) for row in grid_list)


class TestMinimax:
    def test_captures_free_queen(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 3, 3, Piece(piece_type=PieceType.ROOK, team=Team.WHITE))
        grid = _place(grid, 3, 6, Piece(piece_type=PieceType.QUEEN, team=Team.BLACK))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        move = best_move(state, depth=2)
        assert move is not None
        assert move.to_pos.x == 3
        assert move.to_pos.y == 6

    def test_returns_move_from_initial(self):
        state = initial_state()
        move = best_move(state, depth=1)
        assert move is not None

    def test_no_moves_returns_none(self):
        grid = _empty_grid()
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 0, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 1, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 7, 0, Piece(piece_type=PieceType.ROOK, team=Team.BLACK))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        move = best_move(state, depth=2)
        assert move is None

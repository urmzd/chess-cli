from chess_core.engine.evaluation import evaluate
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


class TestEvaluation:
    def test_initial_position_roughly_equal(self):
        state = initial_state()
        score = evaluate(state)
        assert abs(score) < 1.0

    def test_white_queen_advantage(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 3, 3, Piece(piece_type=PieceType.QUEEN, team=Team.WHITE))
        grid = _place(grid, 4, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        score = evaluate(state)
        assert score > 0

    def test_black_material_advantage(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 4, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        grid = _place(grid, 3, 4, Piece(piece_type=PieceType.QUEEN, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        score = evaluate(state)
        assert score < 0

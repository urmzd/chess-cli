from chess_core.models.enums import PieceType, Team
from chess_core.models.game import GameState
from chess_core.models.move import Move, Position
from chess_core.models.piece import Piece
from chess_core.rules.board_ops import initial_state
from chess_core.rules.movement import get_all_legal_moves, get_legal_moves


def _empty_grid():
    return tuple(tuple(None for _ in range(8)) for _ in range(8))


def _place(grid, x, y, piece):
    grid_list = [list(row) for row in grid]
    grid_list[y][x] = piece
    return tuple(tuple(row) for row in grid_list)


class TestPawnMoves:
    def test_initial_pawn_has_two_moves(self):
        state = initial_state()
        moves = get_legal_moves(state, Position(x=4, y=1))
        to_squares = {(m.to_pos.x, m.to_pos.y) for m in moves}
        assert (4, 2) in to_squares
        assert (4, 3) in to_squares

    def test_pawn_blocked(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 1, Piece(piece_type=PieceType.PAWN, team=Team.WHITE))
        grid = _place(grid, 4, 2, Piece(piece_type=PieceType.PAWN, team=Team.BLACK))
        grid = _place(grid, 4, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 4, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        moves = get_legal_moves(state, Position(x=4, y=1))
        assert len(moves) == 0

    def test_pawn_capture(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 4, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 5, 5, Piece(piece_type=PieceType.PAWN, team=Team.BLACK))
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        moves = get_legal_moves(state, Position(x=4, y=4))
        to_squares = {(m.to_pos.x, m.to_pos.y) for m in moves}
        assert (5, 5) in to_squares
        assert (4, 5) in to_squares


class TestKnightMoves:
    def test_center_knight(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 4, Piece(piece_type=PieceType.KNIGHT, team=Team.WHITE))
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        moves = get_legal_moves(state, Position(x=4, y=4))
        assert len(moves) == 8

    def test_corner_knight(self):
        grid = _empty_grid()
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KNIGHT, team=Team.WHITE))
        grid = _place(grid, 4, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        moves = get_legal_moves(state, Position(x=0, y=0))
        assert len(moves) == 2


class TestSlidingPieces:
    def test_rook_open_board(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 4, Piece(piece_type=PieceType.ROOK, team=Team.WHITE))
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        moves = get_legal_moves(state, Position(x=4, y=4))
        assert len(moves) == 14

    def test_bishop_open_board(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 4, Piece(piece_type=PieceType.BISHOP, team=Team.WHITE))
        grid = _place(grid, 0, 2, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 7, 0, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        state = GameState(grid=grid, turn=Team.WHITE)
        moves = get_legal_moves(state, Position(x=4, y=4))
        assert len(moves) == 13


class TestKingMoves:
    def test_initial_king_no_moves(self):
        state = initial_state()
        moves = get_legal_moves(state, Position(x=4, y=0))
        assert len(moves) == 0


class TestAllLegalMoves:
    def test_initial_position_white(self):
        state = initial_state()
        moves = get_all_legal_moves(state, Team.WHITE)
        assert len(moves) == 20  # 16 pawn + 4 knight

    def test_initial_position_black(self):
        state = initial_state()
        moves = get_all_legal_moves(state, Team.BLACK)
        assert len(moves) == 20


class TestEnPassant:
    def test_en_passant(self):
        grid = _empty_grid()
        grid = _place(grid, 4, 4, Piece(piece_type=PieceType.PAWN, team=Team.WHITE, has_moved=True))
        grid = _place(grid, 5, 4, Piece(piece_type=PieceType.PAWN, team=Team.BLACK, has_moved=True))
        grid = _place(grid, 0, 0, Piece(piece_type=PieceType.KING, team=Team.WHITE))
        grid = _place(grid, 7, 7, Piece(piece_type=PieceType.KING, team=Team.BLACK))
        last = Move(from_pos=Position(x=5, y=6), to_pos=Position(x=5, y=4))
        state = GameState(grid=grid, turn=Team.WHITE, last_move=last)
        moves = get_legal_moves(state, Position(x=4, y=4))
        ep_moves = [m for m in moves if m.is_en_passant]
        assert len(ep_moves) == 1
        assert ep_moves[0].to_pos == Position(x=5, y=5)

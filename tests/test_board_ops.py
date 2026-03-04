from chess_core.models.enums import PieceType, Team
from chess_core.models.move import Move, Position
from chess_core.rules.board_ops import apply_move, initial_state, move_to_string, parse_move_string


class TestInitialState:
    def test_grid_dimensions(self):
        state = initial_state()
        assert len(state.grid) == 8
        for row in state.grid:
            assert len(row) == 8

    def test_white_back_rank(self):
        state = initial_state()
        assert state.grid[0][0].piece_type == PieceType.ROOK
        assert state.grid[0][1].piece_type == PieceType.KNIGHT
        assert state.grid[0][2].piece_type == PieceType.BISHOP
        assert state.grid[0][3].piece_type == PieceType.QUEEN
        assert state.grid[0][4].piece_type == PieceType.KING
        for x in range(8):
            assert state.grid[0][x].team == Team.WHITE

    def test_black_back_rank(self):
        state = initial_state()
        assert state.grid[7][4].piece_type == PieceType.KING
        assert state.grid[7][3].piece_type == PieceType.QUEEN
        for x in range(8):
            assert state.grid[7][x].team == Team.BLACK

    def test_pawns(self):
        state = initial_state()
        for x in range(8):
            assert state.grid[1][x].piece_type == PieceType.PAWN
            assert state.grid[1][x].team == Team.WHITE
            assert state.grid[6][x].piece_type == PieceType.PAWN
            assert state.grid[6][x].team == Team.BLACK

    def test_empty_center(self):
        state = initial_state()
        for y in range(2, 6):
            for x in range(8):
                assert state.grid[y][x] is None

    def test_turn(self):
        state = initial_state()
        assert state.turn == Team.WHITE


class TestApplyMove:
    def test_pawn_advance(self):
        state = initial_state()
        move = Move(from_pos=Position(x=4, y=1), to_pos=Position(x=4, y=3))
        new_state = apply_move(state, move)
        assert new_state.grid[1][4] is None
        assert new_state.grid[3][4].piece_type == PieceType.PAWN
        assert new_state.turn == Team.BLACK

    def test_half_move_clock_resets_on_pawn(self):
        state = initial_state()
        move = Move(from_pos=Position(x=4, y=1), to_pos=Position(x=4, y=3))
        new_state = apply_move(state, move)
        assert new_state.half_move_clock == 0

    def test_has_moved_flag(self):
        state = initial_state()
        move = Move(from_pos=Position(x=4, y=1), to_pos=Position(x=4, y=3))
        new_state = apply_move(state, move)
        assert new_state.grid[3][4].has_moved is True

    def test_move_history_grows(self):
        state = initial_state()
        move = Move(from_pos=Position(x=4, y=1), to_pos=Position(x=4, y=3))
        new_state = apply_move(state, move)
        assert len(new_state.move_history) == 1
        assert new_state.move_history[0] == move


class TestParseMoveString:
    def test_valid_opening(self):
        state = initial_state()
        move = parse_move_string(state, "e2e4")
        assert move is not None
        assert move.from_pos == Position(x=4, y=1)
        assert move.to_pos == Position(x=4, y=3)

    def test_invalid_move(self):
        state = initial_state()
        assert parse_move_string(state, "e2e5") is None

    def test_garbage(self):
        state = initial_state()
        assert parse_move_string(state, "xyz") is None
        assert parse_move_string(state, "") is None


class TestMoveToString:
    def test_basic(self):
        move = Move(from_pos=Position(x=4, y=1), to_pos=Position(x=4, y=3))
        assert move_to_string(move) == "e2e4"

    def test_promotion(self):
        move = Move(
            from_pos=Position(x=0, y=6),
            to_pos=Position(x=0, y=7),
            promotion=PieceType.QUEEN,
        )
        assert move_to_string(move) == "a7a8q"

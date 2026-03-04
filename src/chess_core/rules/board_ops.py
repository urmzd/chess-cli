from __future__ import annotations

from chess_core.models.enums import GameStatus, PieceType, Team
from chess_core.models.game import GameState, Grid
from chess_core.models.move import Move, Position
from chess_core.models.piece import Piece
from chess_core.rules.check import compute_status


def initial_state() -> GameState:
    grid_list: list[list[Piece | None]] = [[None] * 8 for _ in range(8)]

    back_rank = [
        PieceType.ROOK,
        PieceType.KNIGHT,
        PieceType.BISHOP,
        PieceType.QUEEN,
        PieceType.KING,
        PieceType.BISHOP,
        PieceType.KNIGHT,
        PieceType.ROOK,
    ]

    # White pieces (rows 0-1)
    for x, pt in enumerate(back_rank):
        grid_list[0][x] = Piece(piece_type=pt, team=Team.WHITE)
    for x in range(8):
        grid_list[1][x] = Piece(piece_type=PieceType.PAWN, team=Team.WHITE)

    # Black pieces (rows 6-7)
    for x in range(8):
        grid_list[6][x] = Piece(piece_type=PieceType.PAWN, team=Team.BLACK)
    for x, pt in enumerate(back_rank):
        grid_list[7][x] = Piece(piece_type=pt, team=Team.BLACK)

    grid: Grid = tuple(tuple(row) for row in grid_list)
    return GameState(grid=grid, turn=Team.WHITE)


def apply_move(state: GameState, move: Move) -> GameState:
    grid_list = [list(row) for row in state.grid]
    piece = grid_list[move.from_pos.y][move.from_pos.x]
    if piece is None:
        return state

    moved_piece = piece.model_copy(update={"has_moved": True})

    # Handle promotion
    if move.promotion is not None:
        moved_piece = Piece(piece_type=move.promotion, team=piece.team, has_moved=True)

    # Determine if capture or pawn move for half-move clock
    is_capture = grid_list[move.to_pos.y][move.to_pos.x] is not None or move.is_en_passant
    is_pawn_move = piece.piece_type == PieceType.PAWN
    new_clock = 0 if (is_capture or is_pawn_move) else state.half_move_clock + 1

    grid_list[move.from_pos.y][move.from_pos.x] = None
    grid_list[move.to_pos.y][move.to_pos.x] = moved_piece

    # En passant capture
    if move.is_en_passant:
        captured_y = move.from_pos.y
        grid_list[captured_y][move.to_pos.x] = None

    # Castling rook movement
    if move.is_castling:
        row = move.from_pos.y
        if move.to_pos.x == 6:  # Kingside
            rook = grid_list[row][7]
            grid_list[row][7] = None
            grid_list[row][5] = rook.model_copy(update={"has_moved": True}) if rook else None
        elif move.to_pos.x == 2:  # Queenside
            rook = grid_list[row][0]
            grid_list[row][0] = None
            grid_list[row][3] = rook.model_copy(update={"has_moved": True}) if rook else None

    new_grid: Grid = tuple(tuple(row) for row in grid_list)
    next_turn = Team.BLACK if state.turn == Team.WHITE else Team.WHITE
    new_history = (*state.move_history, move)

    new_state = GameState(
        grid=new_grid,
        turn=next_turn,
        last_move=move,
        half_move_clock=new_clock,
        move_history=new_history,
        status=GameStatus.PLAYING,
    )

    status = compute_status(new_state)
    return new_state.model_copy(update={"status": status})


def parse_move_string(state: GameState, s: str) -> Move | None:
    s = s.strip().lower()
    if len(s) < 4 or len(s) > 5:
        return None

    try:
        from_x = ord(s[0]) - ord("a")
        from_y = int(s[1]) - 1
        to_x = ord(s[2]) - ord("a")
        to_y = int(s[3]) - 1
    except (ValueError, IndexError):
        return None

    if not (0 <= from_x <= 7 and 0 <= from_y <= 7 and 0 <= to_x <= 7 and 0 <= to_y <= 7):
        return None

    promotion = None
    if len(s) == 5:
        promo_map = {
            "q": PieceType.QUEEN,
            "r": PieceType.ROOK,
            "b": PieceType.BISHOP,
            "n": PieceType.KNIGHT,
        }
        promotion = promo_map.get(s[4])
        if promotion is None:
            return None

    from_pos = Position(x=from_x, y=from_y)
    to_pos = Position(x=to_x, y=to_y)

    # Find the matching legal move
    from chess_core.rules.movement import get_legal_moves

    legal = get_legal_moves(state, from_pos)
    for move in legal:
        if move.to_pos == to_pos:
            if move.promotion is not None:
                if move.promotion == promotion:
                    return move
            elif promotion is None:
                return move
    return None


def move_to_string(move: Move) -> str:
    from_file = chr(move.from_pos.x + ord("a"))
    from_rank = str(move.from_pos.y + 1)
    to_file = chr(move.to_pos.x + ord("a"))
    to_rank = str(move.to_pos.y + 1)
    promo = move.promotion.value if move.promotion else ""
    return f"{from_file}{from_rank}{to_file}{to_rank}{promo}"

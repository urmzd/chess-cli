from __future__ import annotations

from chess_core.models.enums import PieceType, Team
from chess_core.models.game import GameState
from chess_core.models.move import Move, Position
from chess_core.models.piece import Piece
from chess_core.rules.constants import (
    BISHOP_DIRECTIONS,
    KING_DELTAS,
    KNIGHT_DELTAS,
    QUEEN_DIRECTIONS,
    ROOK_DIRECTIONS,
)


def _in_bounds(x: int, y: int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8


def _piece_at(state: GameState, x: int, y: int) -> Piece | None:
    return state.grid[y][x]


def _is_enemy(piece: Piece, team: Team) -> bool:
    return piece.team != team


def _sliding_moves(
    state: GameState,
    pos: Position,
    team: Team,
    directions: list[tuple[int, int]],
) -> list[Move]:
    moves: list[Move] = []
    for dx, dy in directions:
        nx, ny = pos.x + dx, pos.y + dy
        while _in_bounds(nx, ny):
            target = _piece_at(state, nx, ny)
            if target is None:
                moves.append(Move(from_pos=pos, to_pos=Position(x=nx, y=ny)))
            elif _is_enemy(target, team):
                moves.append(Move(from_pos=pos, to_pos=Position(x=nx, y=ny)))
                break
            else:
                break
            nx += dx
            ny += dy
    return moves


def _knight_moves(state: GameState, pos: Position, team: Team) -> list[Move]:
    moves: list[Move] = []
    for dx, dy in KNIGHT_DELTAS:
        nx, ny = pos.x + dx, pos.y + dy
        if not _in_bounds(nx, ny):
            continue
        target = _piece_at(state, nx, ny)
        if target is None or _is_enemy(target, team):
            moves.append(Move(from_pos=pos, to_pos=Position(x=nx, y=ny)))
    return moves


def _pawn_moves(state: GameState, pos: Position, team: Team, piece: Piece) -> list[Move]:
    moves: list[Move] = []
    direction = 1 if team == Team.WHITE else -1
    start_rank = 1 if team == Team.WHITE else 6
    promo_rank = 7 if team == Team.WHITE else 0

    # Forward one
    ny = pos.y + direction
    if _in_bounds(pos.x, ny) and _piece_at(state, pos.x, ny) is None:
        if ny == promo_rank:
            for pt in (PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT):
                moves.append(Move(from_pos=pos, to_pos=Position(x=pos.x, y=ny), promotion=pt))
        else:
            moves.append(Move(from_pos=pos, to_pos=Position(x=pos.x, y=ny)))

        # Forward two (only if forward one was clear)
        ny2 = pos.y + 2 * direction
        if pos.y == start_rank and _in_bounds(pos.x, ny2) and _piece_at(state, pos.x, ny2) is None:
            moves.append(Move(from_pos=pos, to_pos=Position(x=pos.x, y=ny2)))

    # Diagonal captures
    for dx in (-1, 1):
        nx = pos.x + dx
        ny = pos.y + direction
        if not _in_bounds(nx, ny):
            continue
        target = _piece_at(state, nx, ny)
        if target is not None and _is_enemy(target, team):
            if ny == promo_rank:
                for pt in (PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT):
                    moves.append(Move(from_pos=pos, to_pos=Position(x=nx, y=ny), promotion=pt))
            else:
                moves.append(Move(from_pos=pos, to_pos=Position(x=nx, y=ny)))

    # En passant
    if state.last_move is not None:
        lm = state.last_move
        lm_piece = _piece_at(state, lm.to_pos.x, lm.to_pos.y)
        if (
            lm_piece is not None
            and lm_piece.piece_type == PieceType.PAWN
            and abs(lm.to_pos.y - lm.from_pos.y) == 2
            and lm.to_pos.y == pos.y
            and abs(lm.to_pos.x - pos.x) == 1
        ):
            ep_y = pos.y + direction
            moves.append(
                Move(
                    from_pos=pos,
                    to_pos=Position(x=lm.to_pos.x, y=ep_y),
                    is_en_passant=True,
                )
            )

    return moves


def _king_moves(state: GameState, pos: Position, team: Team, piece: Piece) -> list[Move]:
    moves: list[Move] = []
    for dx, dy in KING_DELTAS:
        nx, ny = pos.x + dx, pos.y + dy
        if not _in_bounds(nx, ny):
            continue
        target = _piece_at(state, nx, ny)
        if target is None or _is_enemy(target, team):
            moves.append(Move(from_pos=pos, to_pos=Position(x=nx, y=ny)))

    # Castling
    if not piece.has_moved:
        row = pos.y
        # Kingside (rook at x=7)
        rook_ks = _piece_at(state, 7, row)
        if (
            rook_ks is not None
            and rook_ks.piece_type == PieceType.ROOK
            and not rook_ks.has_moved
            and _piece_at(state, 5, row) is None
            and _piece_at(state, 6, row) is None
        ):
            moves.append(
                Move(
                    from_pos=pos,
                    to_pos=Position(x=6, y=row),
                    is_castling=True,
                )
            )
        # Queenside (rook at x=0)
        rook_qs = _piece_at(state, 0, row)
        if (
            rook_qs is not None
            and rook_qs.piece_type == PieceType.ROOK
            and not rook_qs.has_moved
            and _piece_at(state, 1, row) is None
            and _piece_at(state, 2, row) is None
            and _piece_at(state, 3, row) is None
        ):
            moves.append(
                Move(
                    from_pos=pos,
                    to_pos=Position(x=2, y=row),
                    is_castling=True,
                )
            )

    return moves


def get_pseudo_legal_moves(state: GameState, pos: Position) -> list[Move]:
    piece = _piece_at(state, pos.x, pos.y)
    if piece is None:
        return []

    team = piece.team
    pt = piece.piece_type

    if pt == PieceType.KNIGHT:
        return _knight_moves(state, pos, team)
    elif pt == PieceType.BISHOP:
        return _sliding_moves(state, pos, team, BISHOP_DIRECTIONS)
    elif pt == PieceType.ROOK:
        return _sliding_moves(state, pos, team, ROOK_DIRECTIONS)
    elif pt == PieceType.QUEEN:
        return _sliding_moves(state, pos, team, QUEEN_DIRECTIONS)
    elif pt == PieceType.PAWN:
        return _pawn_moves(state, pos, team, piece)
    elif pt == PieceType.KING:
        return _king_moves(state, pos, team, piece)
    return []


def _apply_move_raw(state: GameState, move: Move) -> GameState:
    """Apply a move without status computation (used for check filtering)."""
    grid_list = [list(row) for row in state.grid]
    piece = grid_list[move.from_pos.y][move.from_pos.x]
    if piece is None:
        return state

    moved_piece = piece.model_copy(update={"has_moved": True})

    # Handle promotion
    if move.promotion is not None:
        moved_piece = Piece(piece_type=move.promotion, team=piece.team, has_moved=True)

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

    new_grid = tuple(tuple(row) for row in grid_list)
    next_turn = Team.BLACK if state.turn == Team.WHITE else Team.WHITE

    return GameState(
        grid=new_grid,
        turn=next_turn,
        last_move=move,
        half_move_clock=state.half_move_clock,
        move_history=state.move_history,
        status=GameStatus.PLAYING,
    )


def _is_square_attacked(state: GameState, x: int, y: int, by_team: Team) -> bool:
    for sy in range(8):
        for sx in range(8):
            p = _piece_at(state, sx, sy)
            if p is None or p.team != by_team:
                continue
            # Use simplified attack check (no recursion into castling)
            pt = p.piece_type
            if pt == PieceType.PAWN:
                direction = 1 if by_team == Team.WHITE else -1
                if sy + direction == y and abs(sx - x) == 1:
                    return True
            elif pt == PieceType.KNIGHT:
                dx, dy_ = abs(sx - x), abs(sy - y)
                if (dx == 1 and dy_ == 2) or (dx == 2 and dy_ == 1):
                    return True
            elif pt == PieceType.KING:
                if abs(sx - x) <= 1 and abs(sy - y) <= 1 and (sx != x or sy != y):
                    return True
            elif pt in (PieceType.BISHOP, PieceType.QUEEN):
                dx, dy_ = x - sx, y - sy
                if abs(dx) == abs(dy_) and dx != 0:
                    step_x = 1 if dx > 0 else -1
                    step_y = 1 if dy_ > 0 else -1
                    cx, cy = sx + step_x, sy + step_y
                    blocked = False
                    while (cx, cy) != (x, y):
                        if _piece_at(state, cx, cy) is not None:
                            blocked = True
                            break
                        cx += step_x
                        cy += step_y
                    if not blocked:
                        return True
            if pt in (PieceType.ROOK, PieceType.QUEEN):
                if sx == x and sy != y:
                    step = 1 if y > sy else -1
                    cy = sy + step
                    blocked = False
                    while cy != y:
                        if _piece_at(state, sx, cy) is not None:
                            blocked = True
                            break
                        cy += step
                    if not blocked:
                        return True
                elif sy == y and sx != x:
                    step = 1 if x > sx else -1
                    cx = sx + step
                    blocked = False
                    while cx != x:
                        if _piece_at(state, cx, sy) is not None:
                            blocked = True
                            break
                        cx += step
                    if not blocked:
                        return True
    return False


def _find_king(state: GameState, team: Team) -> Position | None:
    for y in range(8):
        for x in range(8):
            p = _piece_at(state, x, y)
            if p is not None and p.piece_type == PieceType.KING and p.team == team:
                return Position(x=x, y=y)
    return None


def get_legal_moves(state: GameState, pos: Position) -> list[Move]:
    piece = _piece_at(state, pos.x, pos.y)
    if piece is None:
        return []

    team = piece.team
    enemy = Team.BLACK if team == Team.WHITE else Team.WHITE
    pseudo = get_pseudo_legal_moves(state, pos)
    legal: list[Move] = []

    for move in pseudo:
        new_state = _apply_move_raw(state, move)
        king_pos = _find_king(new_state, team)
        if king_pos is None:
            continue
        if not _is_square_attacked(new_state, king_pos.x, king_pos.y, enemy):
            # Extra castling check: king must not pass through attacked squares
            if move.is_castling:
                if _is_square_attacked(state, pos.x, pos.y, enemy):
                    continue
                mid_x = (pos.x + move.to_pos.x) // 2
                if _is_square_attacked(state, mid_x, pos.y, enemy):
                    continue
            legal.append(move)

    return legal


def get_all_legal_moves(state: GameState, team: Team) -> list[Move]:
    moves: list[Move] = []
    for y in range(8):
        for x in range(8):
            p = _piece_at(state, x, y)
            if p is not None and p.team == team:
                moves.extend(get_legal_moves(state, Position(x=x, y=y)))
    return moves


# Re-export for convenience
from chess_core.models.enums import GameStatus  # noqa: E402

from chess_core.models.enums import GameStatus, Team
from chess_core.models.game import GameState
from chess_core.rules.movement import (
    _find_king,
    _is_square_attacked,
    get_all_legal_moves,
)


def is_in_check(state: GameState, team: Team) -> bool:
    king_pos = _find_king(state, team)
    if king_pos is None:
        return False
    enemy = Team.BLACK if team == Team.WHITE else Team.WHITE
    return _is_square_attacked(state, king_pos.x, king_pos.y, enemy)


def is_checkmate(state: GameState, team: Team) -> bool:
    return is_in_check(state, team) and len(get_all_legal_moves(state, team)) == 0


def is_stalemate(state: GameState, team: Team) -> bool:
    return not is_in_check(state, team) and len(get_all_legal_moves(state, team)) == 0


def compute_status(state: GameState) -> GameStatus:
    team = state.turn
    if is_checkmate(state, team):
        return GameStatus.CHECKMATE
    if is_stalemate(state, team):
        return GameStatus.STALEMATE
    if state.half_move_clock >= 100:
        return GameStatus.DRAW
    if is_in_check(state, team):
        return GameStatus.CHECK
    return GameStatus.PLAYING

from __future__ import annotations

from chess_core.engine.evaluation import evaluate
from chess_core.models.enums import GameStatus, Team
from chess_core.models.game import GameState
from chess_core.models.move import Move
from chess_core.rules.board_ops import apply_move
from chess_core.rules.movement import get_all_legal_moves


def _minimax(
    state: GameState,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
) -> float:
    if depth == 0 or state.status in (GameStatus.CHECKMATE, GameStatus.STALEMATE, GameStatus.DRAW):
        return evaluate(state)

    team = Team.WHITE if maximizing else Team.BLACK
    moves = get_all_legal_moves(state, team)

    if not moves:
        return evaluate(state)

    if maximizing:
        max_eval = -float("inf")
        for move in moves:
            new_state = apply_move(state, move)
            val = _minimax(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in moves:
            new_state = apply_move(state, move)
            val = _minimax(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval


def best_move(state: GameState, depth: int) -> Move | None:
    team = state.turn
    maximizing = team == Team.WHITE
    moves = get_all_legal_moves(state, team)

    if not moves:
        return None

    best: Move | None = None
    if maximizing:
        best_val = -float("inf")
        for move in moves:
            new_state = apply_move(state, move)
            val = _minimax(new_state, depth - 1, -float("inf"), float("inf"), False)
            if val > best_val:
                best_val = val
                best = move
    else:
        best_val = float("inf")
        for move in moves:
            new_state = apply_move(state, move)
            val = _minimax(new_state, depth - 1, -float("inf"), float("inf"), True)
            if val < best_val:
                best_val = val
                best = move

    return best

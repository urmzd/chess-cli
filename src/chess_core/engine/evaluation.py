from chess_core.models.enums import Team
from chess_core.models.game import GameState
from chess_core.rules.constants import PIECE_VALUES, POSITION_VALUES


def evaluate(state: GameState) -> float:
    score = 0.0
    for y in range(8):
        for x in range(8):
            piece = state.grid[y][x]
            if piece is None:
                continue
            material = PIECE_VALUES[piece.piece_type]
            table = POSITION_VALUES[piece.piece_type]
            if piece.team == Team.WHITE:
                score += material + table[y][x]
            else:
                score -= material + table[7 - y][x]
    return score

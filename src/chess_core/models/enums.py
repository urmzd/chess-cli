from enum import Enum


class Team(str, Enum):
    WHITE = "W"
    BLACK = "B"


class PieceType(str, Enum):
    KING = "k"
    QUEEN = "q"
    ROOK = "r"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN = "p"


class GameStatus(str, Enum):
    PLAYING = "playing"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW = "draw"

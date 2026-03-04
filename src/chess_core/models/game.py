from pydantic import BaseModel, ConfigDict

from chess_core.models.enums import GameStatus, Team
from chess_core.models.move import Move
from chess_core.models.piece import Piece

Grid = tuple[tuple[Piece | None, ...], ...]


class GameState(BaseModel):
    model_config = ConfigDict(frozen=True)

    grid: Grid
    turn: Team
    last_move: Move | None = None
    half_move_clock: int = 0
    move_history: tuple[Move, ...] = ()
    status: GameStatus = GameStatus.PLAYING

from pydantic import BaseModel, ConfigDict

from chess_core.models.enums import PieceType, Team


class Piece(BaseModel):
    model_config = ConfigDict(frozen=True)

    piece_type: PieceType
    team: Team
    has_moved: bool = False

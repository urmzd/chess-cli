from pydantic import BaseModel, ConfigDict, Field

from chess_core.models.enums import PieceType


class Position(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int = Field(ge=0, le=7)
    y: int = Field(ge=0, le=7)


class Move(BaseModel):
    model_config = ConfigDict(frozen=True)

    from_pos: Position
    to_pos: Position
    promotion: PieceType | None = None
    is_castling: bool = False
    is_en_passant: bool = False

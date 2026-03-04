from __future__ import annotations

from textual.message import Message
from textual.widgets import Static

from chess_core.models.move import Position


class ChessSquare(Static):
    class Clicked(Message):
        def __init__(self, pos: Position) -> None:
            super().__init__()
            self.pos = pos

    def __init__(
        self,
        pos: Position,
        content: str = "",
        is_light: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(content, **kwargs)
        self.pos = pos
        self.is_light = is_light
        self.add_class("light-square" if is_light else "dark-square")

    def on_click(self) -> None:
        self.post_message(self.Clicked(self.pos))

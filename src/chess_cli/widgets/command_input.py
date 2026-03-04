from __future__ import annotations

from textual.message import Message
from textual.widgets import Input


class CommandInput(Input):
    class CommandSubmitted(Message):
        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    def __init__(self, **kwargs) -> None:
        super().__init__(placeholder="Type move (e.g. e2e4) or command...", **kwargs)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        if value:
            self.post_message(self.CommandSubmitted(value))
            self.value = ""

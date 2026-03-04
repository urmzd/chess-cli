from textual.app import App

from chess_cli.screens.game import GameScreen
from chess_core.models.enums import Team
from chess_core.rules.board_ops import initial_state


class ChessApp(App):
    TITLE = "Chess CLI"
    CSS_PATH = "app.tcss"

    def __init__(self, ai_team: Team | None = Team.BLACK, ai_depth: int = 3, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ai_team = ai_team
        self.ai_depth = ai_depth

    def on_mount(self) -> None:
        state = initial_state()
        self.push_screen(GameScreen(state, ai_team=self.ai_team, ai_depth=self.ai_depth))

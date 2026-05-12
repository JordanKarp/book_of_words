from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText
from src.classes.high_score import HighScore

from src.data.text_strings import RETURN_TO_MENU_TEXT, LINE_BREAK


class HighScoresState(State):
    def __init__(self):
        super().__init__()
        self.scoreboard = None

    def startup(self, persistent=None):
        super().startup(persistent)
        # self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)
        # self.high_score_text = MaskedText("High Scores:", self.user)
        self.scoreboard = persistent.get("scoreboard", None)

    def run(self):
        clear_terminal()
        print("High Scores:")
        self.scoreboard.display()

        print(LINE_BREAK)
        input(RETURN_TO_MENU_TEXT)
        # input(self.return_to_menu_text.render())
        self.next_state = "MAIN_MENU_STATE"

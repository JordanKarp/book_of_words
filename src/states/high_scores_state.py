from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText
from src.classes.high_score import HighScore

from src.data.text_strings import RETURN_TO_MENU_TEXT


class HighScoresState(State):
    def __init__(self):
        super().__init__()
        self.scoreboard = None

    def startup(self, persistent=None):
        super().startup(persistent)
        self.scoreboard = persistent.get("scoreboard", None)

    def run(self):
        clear_terminal()
        print("High Scores:")
        self.scoreboard.display()

        # print("\n" + "-" * 43)
        # input(RETURN_TO_MENU_TEXT + "\n")
        input(RETURN_TO_MENU_TEXT)
        self.next_state = "MAIN_MENU_STATE"

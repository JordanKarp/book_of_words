from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText

from src.data.text_strings import RETURN_TO_MENU_TEXT


class HighScoresState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        # self.lore = MaskedText(LORE_TEXT, self.user)
        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)

    def run(self):
        clear_terminal()
        # TODO: DO SOMETHING WITH HIGH SCORES
        input(self.return_to_menu_text.render() + "\n")
        self.next_state = "GAME_STATE"

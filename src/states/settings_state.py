from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option
from src.utilities.masked_text import MaskedText

from src.data.text_strings import RETURN_TO_MENU_TEXT


class SettingsState(State):
    def __init__(self):
        super().__init__()
        self.settings = None

    def startup(self, persistent=None):
        super().startup(persistent)
        self.settings = persistent.get("settings", None)

    def run(self):
        clear_terminal()
        print("Settings (TODO)")


        input(RETURN_TO_MENU_TEXT)
        self.next_state = None
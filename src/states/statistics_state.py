from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option
from src.utilities.masked_text import MaskedText

from src.data.text_strings import RETURN_TO_MENU_TEXT


class StatisticsState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)

    def run(self):
        clear_terminal()
        # TODO: DO SOMETHING WITH STATISTICS
        for stat in self.user.statistics:
            print(MaskedText(f"{stat}: {self.user.statistics[stat]}", self.user).render())
        input(self.return_to_menu_text.render()+'\n')
        self.next_state = "GAME_STATE"
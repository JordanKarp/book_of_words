from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText

from src.data.text_strings import RETURN_TO_MENU_TEXT
from src.data.starting_words import STARTING_WORDS, STARTING_VALID_WORDS


class NewGameState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.user.learn_words(STARTING_WORDS)

        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)

    def run(self):
        clear_terminal()
        print(
            MaskedText(
                f"New words: {', '.join(STARTING_VALID_WORDS)}", self.user
            ).render()
        )

        input(self.return_to_menu_text.render() + "\n")
        self.next_state = "GAME_STATE"

from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option
from src.utilities.masked_text import MaskedText

from src.data.lore import LORE_TEXT
from src.data.lore import BOOK_OF_LORE
from src.data.text_strings import RETURN_TO_MENU_TEXT, NEXT_PAGE_TEXT


class BookState(State):
    def __init__(self):
        super().__init__()
        self.lore = {}


    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.setup_lore()
        self.next_page_text = MaskedText(NEXT_PAGE_TEXT, self.user)
        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)

    def setup_lore(self):
        for i, entry in enumerate(BOOK_OF_LORE):
            self.lore[i] = MaskedText(entry, self.user)

    def run(self):
        clear_terminal()
        for i, entry in enumerate(self.lore):
            clear_terminal()
            print(self.lore[entry].render())
            print("-"*50)
            if i != len(self.lore)-1:
                input("\n\n"+self.next_page_text.render())
        input(self.return_to_menu_text.render()+'\n')
        self.next_state = "GAME_STATE"
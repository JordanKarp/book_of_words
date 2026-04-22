from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, count_lines
from src.utilities.masked_text import MaskedText

# from src.data.lore import LORE_TEXT
# from src.data.lore import BOOK_OF_LORE
from src.data.book_of_lore import BOOK_OF_WORDS_LORE
from src.data.text_strings import RETURN_TO_MENU_TEXT, NEXT_PAGE_TEXT

LINE_LENGTH = 50
LINE_CHAR = "-"


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
        for entry in BOOK_OF_WORDS_LORE:
            if entry.unlocked:
                self.lore[entry.title] = MaskedText(entry.content, self.user)

    def run(self):
        clear_terminal()
        for i, entry in enumerate(self.lore):
            self.print_page(entry, i)
            if i != len(self.lore) - 1:
                input(self.next_page_text.render())
            else:
                input(self.return_to_menu_text.render())
        self.next_state = "GAME_STATE"

    def print_page(self, lore_entry, page_num):
        clear_terminal()
        text = f"{lore_entry} "
        print(f"{LINE_CHAR} {text.ljust(LINE_LENGTH-4, LINE_CHAR)} {page_num}\n")
        print(self.lore[lore_entry].render())
        print(LINE_CHAR * LINE_LENGTH)
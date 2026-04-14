from pathlib import Path
import pickle

from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option
from src.utilities.masked_text import MaskedText
from src.utilities.word_utilities import load_words

from src.data.text_strings import * 

WORDS_PATH = Path(".") / "src"/ "data"/ "word_list.txt"
SAVES_PATH = Path(".") / "saves"


class GameState(State):
    def __init__(self):
        super().__init__()
        self.user = None
        self.all_words = None

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.all_words = load_words(WORDS_PATH)

        self.title_text = MaskedText(GAME_TITLE_TEXT, self.user)
        self.game_menu_text = MaskedText(PLAY_TEXT, self.user)
        self.book_text = MaskedText(BOOK_TEXT, self.user)
        self.shop_text = MaskedText(SHOP_TEXT, self.user)
        self.user_text = MaskedText(USER_TEXT, self.user)
        self.statistics_text = MaskedText(STATISTICS_TEXT, self.user)
        self.quit_text = MaskedText(QUIT_TEXT, self.user)

    def get_menu_options(self):
        options = [self.game_menu_text.render(), self.book_text.render()]
        if "USER" in self.user.unlocks:
            options.append(self.user_text.render())
        if "SHOP" in self.user.unlocks:
            options.append(self.shop_text.render())
        if "STATS" in self.user.unlocks:
            options.append(self.statistics_text.render())
        options.append(self.quit_text.render())
        return options

    def run(self):
        clear_terminal()
        print(self.title_text.render())
        menu_options = self.get_menu_options()
        choice = get_option("> ", menu_options)    
        
        if choice == self.game_menu_text.render():            
            self.next_state = "ANAGRAM_STATE"
        elif choice == self.book_text.render():
            self.next_state = "BOOK_STATE"
        elif choice == self.shop_text.render():
            self.next_state = "SHOP_STATE"
        elif choice == self.statistics_text.render():
            self.next_state = "STATISTICS_STATE"
        elif choice == self.quit_text.render():
            self.save_game()
            self.next_state = "QUIT"
        

    def save_game(self):
        filename = f"{self.user.name}.dat"
        with open(SAVES_PATH / filename, "wb") as f:
            pickle.dump(self.user, f)
        
        
    def cleanup(self):
        self.persist['user'] = self.user
        self.persist['all_words'] = self.all_words

    
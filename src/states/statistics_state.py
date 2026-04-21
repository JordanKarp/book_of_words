from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText
from src.classes.progress_bar import ProgressBar

from src.data.text_strings import RETURN_TO_MENU_TEXT


class StatisticsState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.all_words = persistent.get("all_words", None)
        self.length_text = MaskedText("Length: ", self.user)
        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)
        self.user_word_count = self.get_word_count_by_length()
        self.total_word_count = self.get_total_word_count_by_length()


    def get_word_count_by_length(self):
        user_word_count = {}
        for word in self.user.words_unlocked:
            length = len(word)
            user_word_count[length] = user_word_count.get(length, 0) + 1
        return user_word_count
    
    def get_total_word_count_by_length(self):
        total_word_count = {}
        for word in self.all_words:
            length = len(word)
            total_word_count[length] = total_word_count.get(length, 0) + 1
        return total_word_count
    
    def run(self):
        clear_terminal()
        # TODO: DO SOMETHING WITH STATISTICS
        # progress with number of words learned by length
        for num in range(2, 8):
            count = self.user_word_count.get(num, 0)
            bar = ProgressBar(total=self.total_word_count.get(num, 10), prefix=f"{num}-letter words: ")
            bar.set(count)
            bar.display()
            print()  # move to next line after each bar

        print('-' * 40)    
        for stat in self.user.statistics:
            print(
                MaskedText(f"{stat}: {self.user.statistics[stat]}", self.user).render()
            )
        input(self.return_to_menu_text.render() + "\n")
        self.next_state = "GAME_STATE"

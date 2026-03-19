from src.utilities.state import State
from src.utilities.masked_text import MaskedText
from src.utilities.terminal_utilities import get_valid_word, clear_terminal

from src.data.text_strings import WORD_PROMPT, WORD_PROMPT_ERROR

class AnagramState(State):
    def __init__(self):
        super().__init__()
        self.anagram = None
        self.user = None
        self.all_words = None

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.all_words = persistent.get("all_words", None)
        self.word_text = MaskedText(WORD_PROMPT, self.user)
        self.error_text = MaskedText(WORD_PROMPT_ERROR, self.user)

    def run(self):
        # clear_terminal()
        self.anagram = get_valid_word(self.word_text.render(), self.all_words, self.error_text.render())
        print(f"You entered: {self.anagram}")
        input()
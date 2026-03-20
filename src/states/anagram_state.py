from src.utilities.state import State
from src.utilities.masked_text import MaskedText
from src.utilities.terminal_utilities import get_valid_word, clear_terminal
from src.utilities.word_utilities import build_index_and_word_set, get_all_anagrams_fast,load_words

from src.data.text_strings import *

class AnagramState(State):
    def __init__(self):
        super().__init__()
        self.anagram = None
        self.user = None
        self.all_words = load_words("src/data/word_list.txt")
        self.all_words_index, self.all_words_set = build_index_and_word_set(self.all_words)

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        # self.all_words_index = persistent.get("all_words_index", None)
        self.word_text = MaskedText(WORD_PROMPT, self.user)
        self.words_found_text = MaskedText(WORDS_FOUND_TEXT, self.user)
        self.error_text = MaskedText(WORD_PROMPT_ERROR, self.user)
        self.return_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)

    def run(self):
        # clear_terminal()
        self.anagram = get_valid_word(self.word_text.render(), self.all_words_set, self.error_text.render())

        anagram_dictionary = get_all_anagrams_fast(self.anagram, self.all_words_index)
   
        round_win = self.play_round(anagram_dictionary)
        if round_win:
            self.user.learn_words(list(anagram_dictionary.keys()))
            print(self.words_found_text.render())
            print(", ".join([w for w, found in anagram_dictionary.items() if found]))
            input("\n\n"+self.return_text.render())
        self.next_state = "GAME_STATE"
    
    def play_round(self, anagram_dictionary):
        playing = True
        while playing:
            # Check win condition
            if all(anagram_dictionary.values()):
                playing = False
                return True
            # 
            clear_terminal()
            print(f"{self.anagram.upper()} - {len([w for w, found in anagram_dictionary.items() if found])}/{len(anagram_dictionary)}")
            # print all found words
            for word, found in anagram_dictionary.items():
                if found:
                    print(word) 
                else:
                    print("-" * len(word))


            guess = get_valid_word(self.word_text.render(), self.all_words_set, self.error_text.render())
            if guess in anagram_dictionary:
                anagram_dictionary[guess] = True
            
    def cleanup(self):
        self.persist['user'] = self.user
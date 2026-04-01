from src.utilities.state import State
from src.utilities.masked_text import MaskedText
from src.utilities.terminal_utilities import get_valid_word, clear_terminal
from src.utilities.word_utilities import build_index_and_word_set, get_all_anagrams_fast,load_words

from src.data.text_strings import *

#TODO add masked text to anagram state and update all text strings to use masked text

class AnagramState(State):
    def __init__(self):
        super().__init__()
        self.anagram = None
        self.user = None
        self.current_message = None
        self.all_words = load_words("src/data/word_list.txt")
        self.all_words_index, self.all_words_set = build_index_and_word_set(self.all_words)

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        # self.all_words_index = persistent.get("all_words_index", None)
        self.current_message = ""

        self.word_text = MaskedText(WORD_PROMPT, self.user)
        self.words_found_text = MaskedText(WORDS_FOUND_TEXT, self.user)
        self.error_text = MaskedText(WORD_PROMPT_ERROR, self.user)
        self.return_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)
        self.game_stats = {STATS_WORDS_GUESSED_TEXT: 0, 
                           STATS_CORRECT_GUESSES_TEXT: 0, 
                           STATS_REPEAT_GUESSES_TEXT: 0, 
                           STATS_INCORRECT_GUESSES_TEXT: 0, 
                           STATS_INELIGIBLE_GUESSES_TEXT: 0}
        self.possible_messages = [MaskedText(msg, self.user) for msg in GAME_MESSAGES]

    def run(self):
        # clear_terminal()
        self.anagram = get_valid_word(self.word_text.render(), self.all_words_set, self.error_text.render())

        anagram_dictionary = get_all_anagrams_fast(self.anagram, self.all_words_index)
   
        round_win = self.play_round(anagram_dictionary)

        self.resolve_round(round_win, anagram_dictionary)
        # self.next_state = "RESULTS_STATE"
        self.next_state = "GAME_STATE"

    def play_round(self, anagram_dictionary):
        guessed_words = set()
        playing = True
        while playing:
            clear_terminal()
            # Display anagram and progress
            print(f"{' '.join(self.anagram.upper())} - {len([w for w, found in anagram_dictionary.items() if found])}/{len(anagram_dictionary)}")
            print("-" * 20)

            # Display stats
            if "STATS" in self.user.unlocks:
                print(MaskedText(STATS_TEXT, self.user).render())
                for stat, value in self.game_stats.items():
                    print(f"{MaskedText(stat, self.user).render()}: {value}")
            
            # Display words and found status
            for word, found in anagram_dictionary.items():
                if found:
                    print(word) 
                else:
                    print("-" * len(word))

           # Check win condition
            if all(anagram_dictionary.values()):
                playing = False
                return True
            
            # Check lose condition 
            # TODO: add lose condition based on number of guesses or time limit
            

            while True:
                # display current message if there is one
                if self.current_message:
                    print(self.current_message)

                # Get user guess
                word = input('> ').strip().lower()
                self.game_stats[STATS_WORDS_GUESSED_TEXT] += 1

                # Repeat guess?
                if word in guessed_words:
                    self.current_message = self.possible_messages[1].render().format(word)
                    self.game_stats[STATS_REPEAT_GUESSES_TEXT] += 1
                    break
                else:
                    guessed_words.add(word)

                # Valid word?
                if word in anagram_dictionary:
                    self.current_message = self.possible_messages[0].render().format(word, self.anagram)
                    anagram_dictionary[word] = True
                    self.game_stats[STATS_CORRECT_GUESSES_TEXT] += 1
                    break

                # What type of invalid guess?
                else:
                    if set(word) - set(self.anagram):
                        self.current_message = self.possible_messages[2].render()
                        self.game_stats[STATS_INELIGIBLE_GUESSES_TEXT] += 1
            
                    else:
                        self.current_message = self.possible_messages[3].render()
                        self.game_stats[STATS_INCORRECT_GUESSES_TEXT] += 1
                    break

    def resolve_round(self, round_win, anagram_dictionary):
        self.user.add_stats(self.game_stats)

        if round_win:
            new_words = self.user.learn_words(list(anagram_dictionary.keys()))
            self.user.add_points(new_words)
            unlocks = self.user.update_unlocks(new_words)
            if unlocks:
                print(MaskedText(f"Unlocked {unlocks}!", self.user).render())

            print(self.words_found_text.render())
            print(", ".join(new_words))
            input("\n\n"+self.return_text.render())
            
    def cleanup(self):
        self.persist['user'] = self.user
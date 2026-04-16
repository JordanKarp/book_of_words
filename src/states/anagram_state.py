from src.utilities.state import State
from src.utilities.masked_text import MaskedText
from src.utilities.terminal_utilities import get_valid_word, clear_terminal
from src.utilities.timer import CountdownTimer
from src.utilities.word_utilities import build_index_and_word_set, get_all_anagrams_fast,load_words

from src.data.text_strings import *

TIME_PER_LETTER = 120
#TODO add masked text to anagram state and update all text strings to use masked text

class AnagramState(State):
    def __init__(self):
        super().__init__()
        self.anagram = None
        self.user = None
        self.current_message = None
        self.timer = None
        self.all_words = load_words("src/data/word_list.txt")
        self.all_words_index, self.all_words_set = build_index_and_word_set(self.all_words)

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        # self.all_words_index = persistent.get("all_words_index", None)
        self.current_message = ""
        self.timer = CountdownTimer(0, label="Guess time")

        self.word_text = MaskedText(WORD_PROMPT, self.user)
        self.words_found_text = MaskedText(WORDS_FOUND_TEXT, self.user)
        self.error_text = MaskedText(WORD_PROMPT_ERROR, self.user)
        self.return_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)
        self.game_stats = {STATS_WORDS_GUESSED_TEXT: 0, 
                           STATS_CORRECT_GUESSES_TEXT: 0, 
                           STATS_REPEAT_GUESSES_TEXT: 0, 
                           STATS_INCORRECT_GUESSES_TEXT: 0, 
                           STATS_INELIGIBLE_GUESSES_TEXT: 0,
                           STATS_FREEBIES_USED_TEXT: 0}
        self.possible_messages = [MaskedText(msg, self.user) for msg in GAME_MESSAGES]

    def run(self):
        # clear_terminal()
        self.anagram = get_valid_word(self.word_text.render(), self.all_words_set, self.error_text.render())
        full_anagram_dictionary = get_all_anagrams_fast(self.anagram, self.all_words_index)
        anagram_dictionary = {word: (word in self.user.words_unlocked) for word in full_anagram_dictionary}
        self.timer.set_duration(len(self.anagram)* TIME_PER_LETTER - 300)
        round_win = self.play_round(anagram_dictionary)

        self.resolve_round(round_win, anagram_dictionary)
        self.next_state = "RESULTS_STATE"
        # self.next_state = "GAME_STATE"

    def play_round(self, anagram_dictionary):
        self.timer.start()
        guessed_words = set(word for word, found in anagram_dictionary.items() if found)
        playing = True
        while playing:
            clear_terminal()
            # Display anagram and progress
            print(f"{' '.join(self.anagram.upper())} - {len([w for w, found in anagram_dictionary.items() if found])}/{len(anagram_dictionary)}")
            print("-" * 20)
            # calculate how many lines will be printed below the timer
            lines_below = 1
            if "STATS" in self.user.unlocks:
                lines_below += 1 + len(self.game_stats)
            lines_below += len(anagram_dictionary)
            if self.current_message:
                lines_below += 1
            # Add 1 so the cursor moves all the way up from the prompt line to the timer line.
            self.timer.place(lines_below=lines_below + 1)
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
                self.timer.stop()
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

                if not self.timer.has_time_left():
                    playing = False
                    return False

                # Is it a special command?
                if word == "q":
                    self.timer.stop()
                    playing = False
                    return False
                elif word == 'f' and self.user.freebies > 0:
                    word = self.get_freebie(anagram_dictionary, guessed_words)
                    if word:
                        self.current_message = self.possible_messages[4].render().format(word)
                        self.game_stats[STATS_FREEBIES_USED_TEXT] += 1
                        anagram_dictionary[word] = True
                        self.user.freebies -= 1
                        break
                elif word == 't':
                    self.timer.add_time(30)
                    self.current_message = "Time added test"
                    break

                self.game_stats[STATS_WORDS_GUESSED_TEXT] += 1
                # self.game_stats[STATS_WORDS_GUESSED_LIST]append(word)

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
        return False

    def resolve_round(self, round_win, anagram_dictionary):
        self.user.add_stats(self.game_stats)

        if round_win:
            new_words = self.user.learn_words(list(anagram_dictionary.keys()))
        else:
            new_words = []

        self.persist['round_win'] = round_win
        self.persist['new_words'] = new_words   

    def get_freebie(self, anagram_dictionary, guessed_words):
        for word, found in anagram_dictionary.items():
            if not found and word not in guessed_words:
                return word
        return None
            
    def cleanup(self):
        self.persist['user'] = self.user
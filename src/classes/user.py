from src.data.starting_words import STARTING_WORDS
from src.data.text_strings import *

class User:
    def __init__(self, name, unlocks=None, words_unlocked=None, points=0):
        self.name = name
        self.points = points
        self.freebies = 3
        self.unlocks = set(unlocks) if unlocks is not None else set()
        self.words_unlocked = set(words_unlocked) if words_unlocked is not None else set()
        self.statistics = {
            TOTAL_WORDS_FOUND_TEXT: len(self.words_unlocked),
            TOTAL_CORRECT_GUESSES_TEXT: 0,
            TOTAL_INCORRECT_GUESSES_TEXT: 0,
            TOTAL_INELIGIBLE_GUESSES_TEXT: 0,
            TOTAL_GUESSES_TEXT: 0,
            TOTAL_FREEBIES_USED_TEXT: 0,
            TOTAL_ANAGRAMS_SOLVED_TEXT: 0,
            TOTAL_ROUNDS_PLAYED_TEXT: 0,
            ROUNDS: {}
        }   
        self._subscribers = []

        self.learn_words(STARTING_WORDS)

    def learn_words(self, words_to_learn):
        words_learned = []
        for word in words_to_learn:
            w = word.lower()
            if w not in self.words_unlocked:
                words_learned.append(w)
                self.words_unlocked.add(w)
                for sub in self._subscribers:
                    sub.reveal_word(w)
        return words_learned

    def add_stats(self, game_round_stats_dict):
        self.statistics[TOTAL_ROUNDS_PLAYED_TEXT] += 1
        # self.statistics[ROUNDS][self.statistics[TOTAL_ROUNDS_PLAYED_TEXT]] = game_round_stats_dict
        self.statistics[TOTAL_WORDS_FOUND_TEXT] += game_round_stats_dict.get(STATS_CORRECT_GUESSES_TEXT, 0)
        self.statistics[TOTAL_CORRECT_GUESSES_TEXT] += game_round_stats_dict.get(STATS_CORRECT_GUESSES_TEXT, 0)
        self.statistics[TOTAL_INCORRECT_GUESSES_TEXT] += game_round_stats_dict.get(STATS_INCORRECT_GUESSES_TEXT, 0)
        self.statistics[TOTAL_INELIGIBLE_GUESSES_TEXT] += game_round_stats_dict.get(STATS_INELIGIBLE_GUESSES_TEXT, 0)
        self.statistics[TOTAL_GUESSES_TEXT] += game_round_stats_dict.get(STATS_WORDS_GUESSED_TEXT, 0)
        self.statistics[TOTAL_FREEBIES_USED_TEXT] += game_round_stats_dict.get(STATS_FREEBIES_USED_TEXT, 0)
        self.statistics[TOTAL_ANAGRAMS_SOLVED_TEXT] += 1 if game_round_stats_dict.get(STATS_CORRECT_GUESSES_TEXT, 0) > 0 else 0

    def add_points(self, words_learned):
        points_earned = sum(len(word) for word in words_learned)
        self.points += points_earned
        return points_earned
    
    def update_unlocks(self, words_learned):
        for word in words_learned:
            if word.upper() == "STATS":
                self.unlocks.add("STATS")
                return "STATS"
            if word.upper() == "SHOP":
                self.unlocks.add("SHOP")
            if word.upper() == "USER":
                self.unlocks.add("USER")
                
            

    def register(self, text_obj):
        self._subscribers.append(text_obj)
    
    # def _print_vocabulary(self):
    #     print("Your Vocabulary:")
    #     for word in sorted(self.words_unlocked):
    #         print(f"- {word}")
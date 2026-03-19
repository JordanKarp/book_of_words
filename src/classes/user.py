from src.data.starting_words import STARTING_WORDS

class User:
    def __init__(self, name, unlocks=None, words_unlocked=None):
        self.name = name
        self.unlocks = set(unlocks) if unlocks is not None else set()
        self.words_unlocked = set(words_unlocked) if words_unlocked is not None else set()
        self.statistics = {
            "total_words_unlocked": len(self.words_unlocked),
            "total_unlocks": len(self.unlocks),
            "freebies_used": 0,
            "anagrams_solved": 0,
        }
        self._subscribers = []

        self.learn_words(STARTING_WORDS)

    def learn_words(self, new_words):
        for word in new_words:
            w = word.lower()
            if w not in self.words_unlocked:
                self.words_unlocked.add(w)
                for sub in self._subscribers:
                    sub.reveal_word(w)

    def register(self, text_obj):
        self._subscribers.append(text_obj)
    
    def print_vocabulary(self):
        print("Your Vocabulary:")
        for word in sorted(self.words_unlocked):
            print(f"- {word}")
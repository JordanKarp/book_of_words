import pickle
import os

class HighScore:
    def __init__(self, filename="highscores.dat"):
        self.filename = filename
        self.scores = []
        self._load()

    def add_score(self, name, score):
        if (name, score) not in self.scores:
            self.scores.append((name, score))
            self.scores.sort(key=lambda x: x[1], reverse=True)
            self._save()

    def top(self, n=5):
        return self.scores[:n]

    def best(self):
        return self.scores[0] if self.scores else None

    def display(self, n=5):
        for i, (name, score) in enumerate(self.top(n), start=1):
            print(f"{i}. {name} - {score}")

    def _save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.scores, f)

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "rb") as f:
                    self.scores = pickle.load(f)
            except Exception:
                self.scores = []  # fallback if file is corrupted
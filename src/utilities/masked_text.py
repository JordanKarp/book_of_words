import re
from collections import defaultdict
from src.classes.user import User

class MaskedText:
    def __init__(self, text: str, user: User):
        self.tokens = re.findall(r"\b[\w']+\b|[^\w']", text)
        self.is_word = [t.isalnum() or "'" in t for t in self.tokens]

        # Map: word -> list of positions in tokens
        self.word_positions = defaultdict(list)

        for i, token in enumerate(self.tokens):
            if self.is_word[i]:
                self.word_positions[token.lower()].append(i)

        # Current visible state
        self.visible = [
            token if not is_word or token.lower() in user.words_unlocked
            else "*" * len(token)
            for token, is_word in zip(self.tokens, self.is_word)
        ]

        # Register with user for updates
        user.register(self)

    def reveal_word(self, word: str):
        """Only update tokens for this word"""
        for idx in self.word_positions.get(word, []):
            self.visible[idx] = self.tokens[idx]

    def render(self) -> str:
        return "".join(self.visible)
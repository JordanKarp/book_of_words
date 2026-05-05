ALL_LETTERS = set("abcdefghijklmnopqrstuvwxyz")
# all_numbers = set("0123456789")
ALL_NUMBERS = {str(i) for i in range(100)}

ALL_SYMBOLS = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~↵")
STARTING_VALID_WORDS = {"new", "book", "of", "words", "word", "play", "quit"}

STARTING_WORDS = (
    STARTING_VALID_WORDS.union(ALL_LETTERS).union(ALL_NUMBERS).union(ALL_SYMBOLS)
)

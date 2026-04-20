all_letters = set("abcdefghijklmnopqrstuvwxyz")
all_numbers = set("0123456789")
symbols = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~↵")
STARTING_VALID_WORDS = {"new", "book", "of", "words", "word", "play", "quit"}

STARTING_WORDS = (
    STARTING_VALID_WORDS.union(all_letters).union(all_numbers).union(symbols)
)

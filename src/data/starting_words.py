all_letters = set("abcdefghijklmnopqrstuvwxyz")
# all_numbers = set("0123456789")
all_numbers = {str(i) for i in range(100)}

symbols = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~↵")
STARTING_VALID_WORDS = {"new", "book", "of", "words", "word", "play", "quit"}

STARTING_WORDS = (
    STARTING_VALID_WORDS.union(all_letters).union(all_numbers).union(symbols)
)

all_letters = set("abcdefghijklmnopqrstuvwxyz")
all_numbers = set("0123456789")
starting_valid_words = set(["book", "of", "words", "word", "play", "quit"])

STARTING_WORDS = starting_valid_words.union(all_letters).union(all_numbers)
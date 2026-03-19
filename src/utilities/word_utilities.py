


def load_words(word_file):
    with open(word_file, "r") as f:
        dictionary = f.read()
    return [x.lower() for x in dictionary.split("\n")]



from collections import Counter
from collections import defaultdict
from itertools import combinations



def load_words(word_file):
    with open(word_file, "r") as f:
        dictionary = f.read()
    return [x.lower() for x in dictionary.split("\n")]

# def get_all_anagrams(word, all_words):
#         MIN_WORD_LENGTH = 2
#         letters = word.lower()
#         count = Counter(letters)

#         all_anagrams = set()
#         for word in all_words:
#             if not set(word) - set(letters):
#                 check_word = {k for k, v in Counter(word).items() if v <= count[k]}
#                 if check_word == set(word):
#                     all_anagrams.add(word)

#         anagram_list = [x for x in all_anagrams if len(x) >= MIN_WORD_LENGTH]
#         sorted_list = sorted(anagram_list, key=lambda x: len(x), reverse=True)

#         return {w: False for w in sorted_list}



def build_index_and_word_set(all_words, min_len=2):
    from collections import defaultdict

    index = defaultdict(list)
    word_set = set()

    for word in all_words:
        w = word.lower()
        if len(w) < min_len:
            continue

        key = ''.join(sorted(w))
        index[key].append(w)
        word_set.add(w)

    return index, word_set

def get_all_anagrams_fast(letters, index, min_len=2):
    letters = letters.lower()
    n = len(letters)

    found = set()

    for r in range(min_len, n + 1):
        for combo in set(combinations(letters, r)):
            key = ''.join(sorted(combo))
            if key in index:
                found.update(index[key])


    # sort by length DESC, then alphabetically ASC
    sorted_words = sorted(found, key=lambda w: (-len(w), w))

    return {w: False for w in sorted_words}

def is_valid_word(word, word_set):
    return word.lower() in word_set
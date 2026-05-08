import os
from src.utilities.word_utilities import is_valid_word

def clear_terminal():
    """Clears the terminal screen depending on the operating system being used."""
    _ = os.system("cls") if os.name == "nt" else os.system("clear")


def _get_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

def get_valid_word(prompt="Word: \n", valid_words=None, error_message="Please enter a valid word (letters only)."):
    while True:
        word = input(prompt).strip()

        if is_valid_word(word, valid_words):
            return word

        print(error_message)

def get_option(prompt, options):
    if not options:
        return None

    while True:
        for num, option in enumerate(options, 1):
            print(f"{num}: {option}")
        choice = _get_number(prompt)
        if 1 <= choice <= len(options):
            return options[choice - 1]
        print("Error: Invalid option. Please try again.")


def clear_terminal():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def get_file_names_in_directory(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []
    
def count_lines(string):
    return string.count("\n") + 1
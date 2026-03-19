import os

def clear_terminal():
    """Clears the terminal screen depending on the operating system being used."""
    _ = os.system("cls") if os.name == "nt" else os.system("clear")


# def input_ranged_int(prompt, min, max):
#     while True:
#         try:
#             value = int(input(prompt))
#             if min <= value <= max:
#                 return value
#             else:
#                 print("Invalid input. Please try again!")
#         except ValueError:
#             print("Invalid input. Please try again!")

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

        if word.isalpha():
            if valid_words is None or word.lower() in valid_words:
                return word.lower()

        print(error_message)

def get_option(prompt, options):
    try:
        for num, option in enumerate(options, 1):
            print(f"{num}: {option}")
        num_options = len(options)
        choice = _get_number(prompt)
        if choice <= num_options:
            return options[choice - 1]
    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")


def clear_terminal():
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For Mac and Linux (posix)
    else:
        _ = os.system("clear")
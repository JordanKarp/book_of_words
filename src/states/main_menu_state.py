import pickle
from pathlib import Path

from src.classes.user import User

from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option

from src.data.text_strings import HEADER_TEXT, MAIN_MENU_OPTIONS, NAME_PROMPT_TEXT, NO_SAVE_FOUND_TEXT, YES_OPTIONS, YES_OR_NO_TEXT


SAVES_PATH = Path(".") / "saves"


class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.persist["saves_path"] = SAVES_PATH

    # def print_header(self):
    #     print('\n')
    #     print("Book of Words")
    #     print("~~~~~~~" * 6)

    def prompt_name(self):
        return input(NAME_PROMPT_TEXT)

    def load_user(self, name):
        while True:
            try:
                filename = f"{name}.dat"
                with open(SAVES_PATH / filename, "rb") as f:
                    user_data = pickle.load(f)
            except FileNotFoundError:
                print(NO_SAVE_FOUND_TEXT)
                play = input(YES_OR_NO_TEXT)
                if play in YES_OPTIONS:
                    return User(name)
                else:
                    name = self.prompt_name()
            else:
                return user_data

    def run(self):
        clear_terminal()
        print(HEADER_TEXT)

        choice = get_option("> ", MAIN_MENU_OPTIONS)
        if choice == "New Game":
            name = self.prompt_name()
            self.persist["user"] = User(name)
            self.next_state = "GAME_STATE"
        elif choice == "Load Game":
            name = self.prompt_name()
            self.persist["user"] = self.load_user(name)
            self.next_state = "GAME_STATE"
        # TODO: Add settings and high scores
        # elif choice == "Settings":
        #     self.next_state = "SETTINGS"
        # elif choice == "High Scores":
        #     self.next_state = "HIGH_SCORE"
        elif choice == "Quit" :
            self.next_state = "QUIT"

    def cleanup(self):
        return super().cleanup()
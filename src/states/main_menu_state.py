import pickle
from pathlib import Path

from src.classes.high_score import HighScore
from src.classes.user import User

from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option, get_file_names_in_directory


from src.data.text_strings import *

SAVES_PATH = Path(".") / "saves"


class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.persist["saves_path"] = SAVES_PATH
        self.scoreboard = HighScore('src/data/highscores.dat')
        self.settings = None

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
        if choice == MAIN_MENU_NEW_GAME_TEXT:
            name = self.prompt_name()
            self.persist["user"] = User(name)
            self.next_state = "NEW_GAME_STATE"
        elif choice == MAIN_MENU_LOAD_GAME_TEXT:
            clear_terminal()
            print(AVAILABLE_SAVES_TEXT)
            saves = get_file_names_in_directory(SAVES_PATH)
            save_names = [s.split(".")[0] for s in saves]
            name = get_option(NAME_PROMPT_TEXT, save_names)
            print(name)
            # name = self.prompt_name()
            self.persist["user"] = self.load_user(name)
            self.next_state = "GAME_STATE"
        elif choice == MAIN_MENU_SETTINGS_TEXT:
            self.next_state = "SETTINGS_STATE"
        elif choice == MAIN_MENU_HIGH_SCORES_TEXT:
            self.next_state = "HIGH_SCORES_STATE"
        elif choice == MAIN_MENU_QUIT_TEXT:
            self.next_state = "QUIT"

    def cleanup(self):
        self.persist["scoreboard"] = self.scoreboard
        self.persist["settings"] = self.settings

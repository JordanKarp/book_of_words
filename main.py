from src.states.states import states_list

from src.utilities.state_manager import StateManager


def run():
    game_manager = StateManager(states_list, "MAIN_MENU")
    game_manager.run()


if __name__ == "__main__":
    run()

from src.states.anagram_state import AnagramState
from src.states.book_state import BookState
from src.states.game_state import GameState
from src.states.main_menu_state import MainMenuState


states_list = {
    "MAIN_MENU": MainMenuState(),
    "GAME_STATE": GameState(),
    "BOOK_STATE": BookState(),
    "ANAGRAM_STATE": AnagramState(),
}
from src.states.anagram_state import AnagramState
from src.states.book_state import BookState
from src.states.high_scores_state import HighScoresState
from src.states.game_state import GameState
from src.states.main_menu_state import MainMenuState
from src.states.new_game_state import NewGameState
from src.states.results_state import ResultsState
from src.states.settings_state import SettingsState
from src.states.shop_state import ShopState
from src.states.statistics_state import StatisticsState

states_list = {
    "MAIN_MENU": MainMenuState(),
    "NEW_GAME_STATE": NewGameState(),
    "GAME_STATE": GameState(),
    "BOOK_STATE": BookState(),
    "ANAGRAM_STATE": AnagramState(),
    "RESULTS_STATE": ResultsState(),
    "SETTINGS_STATE": SettingsState(),
    "SHOP_STATE": ShopState(),
    "STATISTICS_STATE": StatisticsState(),
    "HIGH_SCORES_STATE": HighScoresState(),
}

from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText

from src.data.text_strings import RETURN_TO_MENU_TEXT, RESULTS_LINE_BREAK


class ResultsState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)
        self.round_win = persistent.get("round_win", False)
        self.new_words = persistent.get("new_words", [])
        self.unlocks = None

    def run(self):
        self.process_round(self.round_win, self.new_words)
        self.display_results()

        input(self.return_to_menu_text.render())
        self.next_state = "GAME_STATE"

    def process_round(self, round_win, new_words):
        if round_win:
            self.user.add_points(new_words)
            self.unlocks = self.user.update_unlocks(new_words)


    def print_words_learned(self):
        print(MaskedText("Words Learned: ", self.user).render())
        for word in self.new_words:
            print(
                MaskedText(f"- {f'{word}:'.ljust(12)} {len(word)} ", self.user).render()
            )   

    def print_round_score(self):
        score = sum(len(word) for word in self.new_words)
        print(MaskedText(f"Round Score: {score}", self.user).render())

    def print_unlocks(self):
        print(
                MaskedText(f"Unlocked: {', '.join(self.unlocks)}!", self.user).render()
            )

    def print_statistics(self):
        print(MaskedText("Statistics: ", self.user).render())
        for stat in self.user.statistics:
            # print(f"{stat}: {self.user.statistics[stat]}")
            print(
                MaskedText(f"{stat}: {self.user.statistics[stat]}", self.user).render()
            )

    def display_results(self):
        clear_terminal()
        self.print_words_learned()
        print(RESULTS_LINE_BREAK)
        self.print_round_score()
        print(RESULTS_LINE_BREAK)
        if self.unlocks:
            self.print_unlocks()
            print(RESULTS_LINE_BREAK)
        if "STATS" in self.user.unlocks:
            self.print_statistics()
            print(RESULTS_LINE_BREAK)

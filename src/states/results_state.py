from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal
from src.utilities.masked_text import MaskedText

from src.data.text_strings import RETURN_TO_MENU_TEXT


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

        input(self.return_to_menu_text.render() + "\n")
        self.next_state = "GAME_STATE"

    def process_round(self, round_win, new_words):
        if round_win:
            self.user.add_points(new_words)
            self.unlocks = self.user.update_unlocks(new_words)

        # if round_win:
        #     new_words = self.user.learn_words(list(anagram_dictionary.keys()))
        #     self.persist["new_words"] = new_words
        #     self.user.add_points(new_words)
        #     unlocks = self.user.update_unlocks(new_words)
        #     if unlocks:
        #         print(MaskedText(f"Unlocked {unlocks}!", self.user).render())

        #     print(self.words_found_text.render())
        #     print(", ".join(new_words))
        #     input("\n\n"+self.return_text.render())
        # else:
        #     self.persist["new_words"] = []
        #     print(MaskedText("Better luck next time!", self.user).render())
        #     print(MaskedText("0 words learned.", self.user).render())
        #     input("\n\n"+self.return_text.render())

    def display_results(self):
        clear_terminal()
        print(MaskedText("Words Learned: ", self.user).render())
        for word in self.new_words:
            print(
                MaskedText(f"- {f'{word}:'.ljust(12)} {len(word)} ", self.user).render()
            )

        print("-" * 15)
        print(
            MaskedText(
                f"Round Score: {sum(len(word) for word in self.new_words)}", self.user
            ).render()
        )

        if self.unlocks:
            print("-" * 15)
            print(
                MaskedText(f"Unlocked: {', '.join(self.unlocks)}!", self.user).render()
            )

        # TODO: DO SOMETHING WITH STATISTICS
        print("-" * 15)
        print(MaskedText("Statistics: ", self.user).render())
        for stat in self.user.statistics:
            # print(f"{stat}: {self.user.statistics[stat]}")
            print(
                MaskedText(f"{stat}: {self.user.statistics[stat]}", self.user).render()
            )

        print("-" * 15)

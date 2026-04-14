from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option
from src.utilities.masked_text import MaskedText

FREEBIE_PRICE = 50
EXTRA_TIME_PRICE = 50
EXTRA_LIFE_PRICE = 200

# TODO: update to masked text and add more options to shop
# TODO: fix menu option to shop from game menu
# TODO: fix menu option to shop from game menu


class ShopState(State):
    def __init__(self):
        super().__init__()
        self.user = None

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent
        self.user = self.persist["user"]


    def print_upgrades(self):
        print(f'You have currently have {self.user.points} points.')
        print("~~~~~~~" * 6)
        print(f'1. Buy freebie word\t{FREEBIE_PRICE}')
        print(f'2. Buy 30s extra time\t{EXTRA_TIME_PRICE}')
        print(f'3. Buy extra life\t{EXTRA_LIFE_PRICE}')
        print('4. Back to Game Menu')


    def run(self):
        while True:
            clear_terminal()
            shop_options = self.get_shop_options()
            choice = get_option("> ", shop_options)    

            self.next_state = "GAME_STATE"

    def get_shop_options(self):
        options = [f"Buy freebie word\t{FREEBIE_PRICE}", 
                f"Buy 30s extra time\t{EXTRA_TIME_PRICE}", 
                f"Buy extra life\t{EXTRA_LIFE_PRICE}", 
                "Back to Game Menu"]
        return options
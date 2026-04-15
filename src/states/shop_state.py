from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, get_option
from src.utilities.masked_text import MaskedText

from src.data.text_strings import *

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
        self.shop_text = MaskedText(SHOP_INTRO_TEXT, self.user)
        self.shop_freebie_text = MaskedText(SHOP_OPTION_FREEBIE_TEXT, self.user)
        self.shop_extra_life_text = MaskedText(SHOP_OPTION_EXTRA_LIFE_TEXT, self.user)


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
            print(self.shop_intro_text.render())
            shop_options = self.get_shop_options()
            choice = get_option("> ", shop_options)    
            # if choice == 'Buy freebie word\t{FREEBIE_PRICE}'.format(FREEBIE_PRICE=FREEBIE_PRICE):
            #     if self.user.points >= FREEBIE_PRICE:
            #         self.user.points -= FREEBIE_PRICE
            #         self.user.freebies += 1
            #         print(self.shop_freebie_text.render())
            #     else:
            #         print(self.shop_insufficient_points_text.render())
            self.next_state = "GAME_STATE"

    def get_shop_options(self):
        options = []
        if self.user.unlocks and "FREE" in self.user.unlocks:
            options.append(f"Buy freebie word\t{FREEBIE_PRICE}")
        if self.user.unlocks and "LIFE" in self.user.unlocks:
            options.append(f"Buy extra life\t{EXTRA_LIFE_PRICE}")

        options.append("Back to Game Menu")
        return options
from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal

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
        clear_terminal()
        self.print_upgrades()
        choice = input_ranged_int('> ', 1, 4)
        if choice == 1 and self.user.points >= FREEBIE_PRICE:
            self.user.points -= FREEBIE_PRICE
            self.user.freebies += 1
            print("Freebie purchased!")
        elif choice == 2 and self.user.points >= EXTRA_TIME_PRICE:
            self.user.points -= EXTRA_TIME_PRICE
            self.user.extra_times += 1
            print("Extra Time purchased!")
        elif choice == 3 and self.user.points >= EXTRA_LIFE_PRICE:
            self.user.points -= EXTRA_LIFE_PRICE
            self.user.extra_lives += 1
            print("Extra Life purchased!")
        elif choice == 4:
            self.next_state = "GAME_MENU"
        else:
            print('Insufficient funds.')
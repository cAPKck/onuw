from enum import Enum
from cards import Team, Role, Card, CARDS_DICT
import random

######## NOTE BLOCK ########

# Currently the game is always played with 4 cards on the table. I dunno if this is only usually the case if an alpha is present

# The choices for cards/players etc. are not really limited. That could confuse the resolver later on, but for now its fine to keep it simple

class Player:

    def __init__(self, name):
        self.name = name
        self.starting_card = None
        self.new_cards = list()

    def set_starting_card(self, card):
        self.starting_card = card
        self.new_cards = list()

    def choose_from_table(self, board):
        print(self.name + ', please choose from the table:')


class Table:

    def __init__(self):
        self.top_left: list[Card] = list()
        self.top_middle: list[Card] = list()
        self.top_right: list[Card] = list()
        self.bottom: list[Card] = list()


class Game:

    def __init__(self, player_list: list[str], role_pool: list[Role]):

        self.players: list[Player] = list()
        for p in player_list:
            self.players.append(Player(p))
        self.player_count = len(self.players)

        self.card_pool: list[Card] = list()
        for r in role_pool:
            self.card_pool.append(CARDS_DICT[r]())

        self.table = Table()

        # Check card pool requirements
        # First check the amount of cards (must be player_count + 4)
        if not len(self.card_pool) == self.player_count + 4:
            raise Exception('The pool contains too many werewolves')
        # Then check the amount of werewolves
        wwcount = len(
            list(filter(lambda p: p.team == Team.WEREWOLF, self.card_pool)))
        if wwcount < (self.player_count / 4):
            raise Exception('The pool contains not enough werewolves')
        if wwcount > (self.player_count / 2):
            raise Exception('The pool contains too many werewolves')
        # Then check the pool requirements of each card
        for c in self.card_pool:
            if not c.pool_requirements(self.card_pool, self.player_count):
                raise Exception(
                    'Not all card pool requirements for card ' + str(c.role) + ' were fulfilled.')

    def distribute_cards(self):
        cards_to_distribute = self.card_pool.copy()

        # Check if there is an alpha. If so, put a werewolf card on the bottom Table slot.
        if len(list(filter(lambda c: c.role == Role.ALPHA, cards_to_distribute))) > 0:
            for i in range(len(cards_to_distribute)):
                if cards_to_distribute[i].role == Role.WEREWOLF:
                    self.table.bottom.append(cards_to_distribute.pop(i))
                    break

        # Shuffle rest of the cards
        random.shuffle(cards_to_distribute)

        # Then distribute
        for p in self.players:
            p.set_starting_card(cards_to_distribute.pop(0))
        self.table.top_left.append(cards_to_distribute.pop(0))
        self.table.top_middle.append(cards_to_distribute.pop(0))
        self.table.top_right.append(cards_to_distribute.pop(0))
        if len(self.table.bottom) <= 0:
            self.table.bottom.append(cards_to_distribute.pop(0))
        if len(cards_to_distribute) > 0:
            raise Exception(
                'Something went wrong when distributing the cards.')

    def print_debug_start(self):
        print('Cards on Table: ')
        print('Top left: ' + str(self.table.top_left[0].role))
        print('Top middle: ' + str(self.table.top_middle[0].role))
        print('Top right: ' + str(self.table.top_right[0].role))
        print('Bottom: ' + str(self.table.bottom[0].role))
        print('Player Cards:')
        for p in self.players:
            print(p.name + ' has ' + str(p.starting_card.role))

    def run_round(self):
        for r in Role:
            current_players = list(filter(lambda p: p.starting_card.role == r, self.players))
            for p in current_players:
                print('It is ' + p.name + '\'s (' + str(p.starting_card.role) + ') turn.')

                print(p.name + ' ended their turn.')
        print('The round has ended.')

if __name__ == '__main__':
    DEFAULT_POOL = (Role.COPYCAT, Role.ALPHA, Role.WEREWOLF, Role.MYSTIC, Role.SEER,
                    Role.PARANORMAL, Role.ROBBER, Role.WITCH, Role.GREMLIN, Role.DRUNK, Role.TANNER)
    DEFAULT_PLAYERS = ('Anton', 'Berta', 'Caesar', 'Dora',
                       'Emil', 'Friedrich', 'Gustav')
    GAME = Game(DEFAULT_PLAYERS, DEFAULT_POOL)
    GAME.distribute_cards()
    GAME.print_debug_start()
    GAME.run_round()

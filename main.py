import copy
from enum import Enum
from action import Action, ActionConcatenation, ActionType, Target
from cards import Team, Role, Card, CARDS_DICT
import random

######## NOTE BLOCK ########

# Currently the game is always played with 4 cards on the table. I dunno if this is only usually the case if an alpha is present

# The choices for cards/players etc. are not really limited. That could confuse the resolver later on, but for now its fine to keep it simple

# Currently action handling is limited to two actions with a single concatenator. That is inflexible and not enough for all roles. Change it later.


class Player:

    def __init__(self, name):
        self.name = name
        self.cards = list()

    def set_starting_card(self, card):
        self.cards = list()
        self.cards.append(card)

    def choose_action(self, action1, action2):
        """Choose from two actions. """
        print('Choose from the following two actions:')
        print('1: ' + action1.description)
        print('2: ' + action2.description)
        while True:
            choice = input()
            if choice == '1':
                return action1
            elif choice == '2':
                return action2

    def display_action_description(self, description):
        print(description)

    def display_card(self, card):
        print(card.original_role)

    def choose_card_table(self, table) -> list[Card]:
        print('Choose a table card by entering its position (tl, tm, tr, bot):')
        while True:
            choice = input()
            if choice == 'tl':
                return table.top_left
            if choice == 'tm':
                return table.top_middle
            if choice == 'tr':
                return table.top_right
            if choice == 'bot':
                return table.bottom

    def choose_player(self, players, other=False):
        print('Choose a player from the following list:')
        for p in players:
            if not other or not p == self:
                print(p.name)
        while True:
            choice = input()
            for p in players:
                if not other or not p == self:
                    if p.name == choice:
                        return p


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
            print(p.name + ' has ' + str(p.cards[0].role))

    def print_debug_card_histories(self):
        print('Cards on Table: ')
        print('Top left: ' + ''.join(list(map(lambda c: str(c.role) + '(team:' + str(c.team) + ',original:' + str(c.original_role) + '), ', self.table.top_left))))
        print('Top middle: ' + ''.join(list(map(lambda c: str(c.role) + '(team:' + str(c.team) + ',original:' + str(c.original_role) + '), ', self.table.top_middle))))
        print('Top right: ' + ''.join(list(map(lambda c: str(c.role) + '(team:' + str(c.team) + ',original:' + str(c.original_role) + '), ', self.table.top_right))))
        print('Bottom: ' + ''.join(list(map(lambda c: str(c.role) + '(team:' + str(c.team) + ',original:' + str(c.original_role) + '), ', self.table.bottom))))
        print('Player Cards:')
        for p in self.players:
            print(p.name + ': ' + ''.join(list(map(lambda c: str(c.role) + '(team:' + str(c.team) + ',original:' + str(c.original_role) + '), ', p.cards))))

    def run_round(self):
        for r in Role:
            current_players = list(
                filter(lambda p: p.cards[0].role == r, self.players))
            for p in current_players:
                print('\nIt is ' + p.name + '\'s (' +
                      str(p.cards[0].role) + ') turn.')
                self.resolve_actions(p, p.cards[0])
                print(p.name + ' ended their turn.')
        print('\nThe round has ended.\n')

    def resolve_actions(self, player: Player, card: Card):
        # If there is more than one action, check concatenation
        if card.action is None:
            print('Nothing to do here.')
            return
        first_action = card.action.actions[0]
        second_action = None
        if card.action.concatenation == ActionConcatenation.OR:
            first_action = player.choose_action(
                card.action.actions[0], card.action.actions[1])
        elif card.action.concatenation in [ActionConcatenation.AND, ActionConcatenation.RESULT]:
            second_action = card.action.actions[1]
        result = self.resolve_action_single(player, first_action)
        if card.action.concatenation == ActionConcatenation.AND or (card.action.concatenation == ActionConcatenation.RESULT and not result):
            self.resolve_action_single(player, second_action)

    def resolve_action_single(self, player: Player, action: Action) -> bool:
        # Print action task
        player.display_action_description(action.description)

        # Choose targets
        target_types = [action.target1, action.target2]
        target_cards = [None, None]
        for i in range(len(target_types)):
            t = target_types[i]
            if t == Target.TABLE_CARD_ANY:
                target_cards[i] = player.choose_card_table(self.table)
            if t == Target.TABLE_CARD_BOTTOM:
                target_cards[i] = self.table.bottom
            if t == Target.PLAYER_CARD_ANY:
                target_cards[i] = player.choose_player(self.players).cards
            if t == Target.PLAYER_CARD_OTHER:
                target_cards[i] = player.choose_player(
                    self.players, other=True).cards
            if t == Target.PLAYER_CARD_SELF:
                target_cards[i] = player.cards

        # Apply action to targets
        action_types = [action.type1, action.type2]
        result = False
        for i in range(len(action_types)):
            a = action_types[i]
            if a == ActionType.VIEW:
                player.display_card(target_cards[i][-1])
            elif a == ActionType.SWAP:
                temp = target_cards[0][-1]
                target_cards[0].append(target_cards[1][-1])
                target_cards[1].append(temp)
            elif a == ActionType.ADAPT:
                for t in target_cards:
                    if player.cards[-1].team == Team.VILLAGER:
                        if not t[-1].team == Team.VILLAGER:
                            player.cards[-1].team = t[-1].team
                            result = True
                            break
            elif a == ActionType.COPY:
                copied_card = copy.copy(target_cards[i][-1])
                copied_card.original_role = player.cards[0].role
                player.cards[0] = copied_card
                player.display_card(target_cards[i][-1])
        return result


if __name__ == '__main__':
    DEFAULT_POOL = (Role.COPYCAT, Role.ALPHA, Role.WEREWOLF, Role.MYSTIC, Role.SEER,
                    Role.PARANORMAL, Role.ROBBER, Role.WITCH, Role.GREMLIN, Role.DRUNK, Role.TANNER)
    DEFAULT_PLAYERS = ('Anton', 'Berta', 'Caesar', 'Dora',
                       'Emil', 'Friedrich', 'Gustav')
    GAME = Game(DEFAULT_PLAYERS, DEFAULT_POOL)
    GAME.distribute_cards()
    GAME.print_debug_start()
    GAME.run_round()
    GAME.print_debug_card_histories()

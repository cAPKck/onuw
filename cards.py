from abc import ABC, abstractmethod
from enum import Enum
from action import Action, ActionConcatenation, ActionSequence, ActionType, Target


class Role(Enum):
    COPYCAT = 1,
    DOPPEL = 2,
    WEREWOLF = 3,
    GIANT = 4,
    ALPHA = 5,
    MYSTIC = 6,
    MINION = 7,
    APPTANNER = 8,
    MASON = 9,
    SEER = 10,
    APPSEER = 11,
    PARANORMAL = 12,
    ROBBER = 13,
    WITCH = 14,
    TROUBLE = 15,
    AURA = 16,
    GREMLIN = 17,
    DRUNK = 18,
    INSOMNIAC = 19,
    SQUIRE = 20,
    BEHOLDER = 21,
    REVEALER = 22,
    DREAM = 23,
    VILLAGER = 24,
    TANNER = 25,
    HUNTER = 26,
    BODYGUARD = 27,
    PRINCE = 28,
    CURSED = 29


class Team(Enum):
    VILLAGER = 1,
    WEREWOLF = 2,
    TANNER = 3


class Card(ABC):

    def __init__(self, role: Role, team: Team, max_num: int, actions: list[Action] = list()):
        self.role = role
        self.team = team
        self.max_num = max_num
        self.actions = actions

    def pool_requirements(self, card_pool: list, player_count: int) -> bool:
        """Checks if all cards allowed/disallowed for this card are in the pool. """
        if len(list(filter(lambda c: c.role == self.role, card_pool))) > self.max_num:
            return False
        return True

    def known_facts(self, card_pool):
        """Shows the facts known to that player at the start of the game."""

class Copycat(Card):

    def __init__(self):
        super().__init__(Role.COPYCAT, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.COPY, None,
                                    Target.TABLE_CARD_ANY, None)
                         ]))


class Werewolf(Card):

    def __init__(self):
        super().__init__(Role.WEREWOLF, Team.WEREWOLF, 2)


class Alpha(Card):

    def __init__(self):
        super().__init__(Role.ALPHA, Team.WEREWOLF, 1,
                         ActionSequence([
                             Action(ActionType.SWAP, None,
                                    Target.PLAYER_CARD_OTHER, Target.TABLE_CARD_BOTTOM)
                         ]))

    def pool_requirements(self, card_pool: list, player_count: int) -> bool:
        if len(list(filter(lambda c: c.role == Role.WEREWOLF, card_pool))) < 1:
            return False
        return super().pool_requirements(card_pool, player_count)


class Mystic(Card):

    def __init__(self):
        super().__init__(Role.MYSTIC, Team.WEREWOLF, 1,
                         ActionSequence([
                             Action(ActionType.VIEW, None,
                                    Target.PLAYER_CARD_OTHER, None)
                         ]))


class Seer(Card):

    def __init__(self):
        super().__init__(Role.SEER, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.VIEW, ActionType.VIEW,
                                    Target.TABLE_CARD_ANY, Target.TABLE_CARD_ANY),
                             Action(ActionType.VIEW, None,
                                    Target.PLAYER_CARD_ANY, None)
                         ], [ActionConcatenation.OR]))


class Paranormal(Card):

    def __init__(self):
        super().__init__(Role.PARANORMAL, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.VIEW, ActionType.ADAPT,
                                    Target.PLAYER_CARD_ANY, None, True),
                             Action(ActionType.VIEW, ActionType.ADAPT,
                                    Target.PLAYER_CARD_ANY, None, True)
                         ], [ActionConcatenation.RESULT]))


class Robber(Card):

    def __init__(self):
        super().__init__(Role.ROBBER, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.SWAP, ActionType.VIEW,
                                    Target.PLAYER_CARD_OTHER, Target.PLAYER_CARD_SELF)
                         ], optional=True))


class Witch(Card):

    def __init__(self):
        super().__init__(Role.WITCH, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.VIEW, ActionType.SWAP,
                                    Target.TABLE_CARD_ANY, Target.PLAYER_CARD_ANY)
                         ], optional=True))


class Gremlin(Card):

    def __init__(self):
        super().__init__(Role.GREMLIN, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.SWAP, None,
                                    Target.PLAYER_CARD_ANY, Target.PLAYER_CARD_ANY)
                         ], optional=True))


class Drunk(Card):

    def __init__(self):
        super().__init__(Role.DRUNK, Team.VILLAGER, 1,
                         ActionSequence([
                             Action(ActionType.SWAP, None,
                                    Target.TABLE_CARD_ANY, Target.PLAYER_CARD_SELF)
                         ]))


class Tanner(Card):

    def __init__(self):
        super().__init__(Role.TANNER, Team.TANNER, 1)


CARDS_DICT = dict()
CARDS_DICT[Role.COPYCAT] = Copycat
# CARDS_DICT[Role.DOPPEL] = Copycat
CARDS_DICT[Role.WEREWOLF] = Werewolf
# CARDS_DICT[Role.GIANT] = Copycat
CARDS_DICT[Role.ALPHA] = Alpha
CARDS_DICT[Role.MYSTIC] = Mystic
# CARDS_DICT[Role.MINION] = Copycat
# CARDS_DICT[Role.APPTANNER] = Copycat
# CARDS_DICT[Role.MASON] = Copycat
CARDS_DICT[Role.SEER] = Seer
# CARDS_DICT[Role.APPSEER] = Copycat
CARDS_DICT[Role.PARANORMAL] = Paranormal
CARDS_DICT[Role.ROBBER] = Robber
CARDS_DICT[Role.WITCH] = Witch
# CARDS_DICT[Role.TROUBLE] = Copycat
# CARDS_DICT[Role.AURA] = Copycat
CARDS_DICT[Role.GREMLIN] = Gremlin
CARDS_DICT[Role.DRUNK] = Drunk
# CARDS_DICT[Role.INSOMNIAC] = Copycat
# CARDS_DICT[Role.BEHOLDER] = Copycat
# CARDS_DICT[Role.REVEALER] = Copycat
# CARDS_DICT[Role.DREAM] = Copycat
# CARDS_DICT[Role.VILLAGER] = Copycat
CARDS_DICT[Role.TANNER] = Tanner
# CARDS_DICT[Role.HUNTER] = Copycat
# CARDS_DICT[Role.BODYGUARD] = Copycat
# CARDS_DICT[Role.PRINCE] = Copycat
# CARDS_DICT[Role.CURSED] = Copycat

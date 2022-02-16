from enum import Enum


class ActionType(Enum):
    VIEW = 1,
    SWAP = 2,
    COPY = 3,
    ADAPT = 4,


class Target(Enum):
    TABLE_CARD_ANY = 1,
    TABLE_CARD_BOTTOM = 2,
    PLAYER_CARD_ANY = 3,
    PLAYER_CARD_OTHER = 4,
    PLAYER_CARD_SELF = 5,


class Action():

    def __init__(self, type1: ActionType, type2: ActionType, target1: Target, target2: Target, optional: bool = False):
        self.type1 = type1
        self.type2 = type2
        self.target1 = target1
        self.target2 = target2
        self.optional = optional


class ActionConcatenation(Enum):
    AND = 1,
    OR = 2,
    RESULT = 3,


class ActionSequence():

    def __init__(self, actions: list[Action], concatenation: list[ActionConcatenation] = list(), optional: bool = False):
        self.actions = actions
        self.concatenation = concatenation
        self.optional = optional


"""


Copy Card from Table
Copy Card from Player

View 1 Player Card
View 2 Cards from the Middle

View 1 Cards from the Middle
View 1 then another player card

Swap self with other
Swap Table card with player
Swap two other players
See players taht moved or viewed a card
Swap any two players
Swap self with Table

View own
View Werewolves




"""

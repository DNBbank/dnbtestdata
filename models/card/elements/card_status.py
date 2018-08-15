from enum import Enum
from numpy import random

class CardStatus(Enum):
    ACTIVE = "ACTIVE"
    NOTACTIVE = "NOTACTIVE"
    BLOCKED = "BLOCKED"



    @classmethod
    def get_random(cls):

        choices = [CardStatus.ACTIVE, CardStatus.NOTACTIVE, CardStatus.BLOCKED]
        choice_probabilities = [0.8, 0.15, 0.05]

        return random.choice(choices, p=choice_probabilities)

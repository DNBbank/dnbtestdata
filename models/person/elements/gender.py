import random

from enum import Enum


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

    @classmethod
    def generate_random(cls):
        if random.choice((True, False)):
            return cls.FEMALE
        else:
            return cls.MALE


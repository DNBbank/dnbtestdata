import random
from faker import Faker


class MaskedCardNumber:
    @classmethod

    def generate_random(cls):
        fake = Faker('no_NO')
        number = fake.credit_card_number(card_type="visa16")
        return "************" + number[12:]

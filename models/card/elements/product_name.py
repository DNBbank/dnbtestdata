import random
from faker import Faker
from .card_type import CardType

CREDIT_CARDS_PRODUCT_NAMES = ["MASTERCARD", "DINERS", "MAESTRO", "AMEX CARD"]

class ProductName:
    @classmethod
    def generate_random_by_type(cls, cardType):


        fake = Faker('no_NO')
        number = fake.credit_card_number(card_type="visa16")

        if cardType == CardType.CREDIT:
            return random.choice(CREDIT_CARDS_PRODUCT_NAMES)
        else:
            return "VISA"

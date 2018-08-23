currencyfrom .elements.card_type import CardType
import random
import numpy as np
class CardBalance:
    @classmethod
    def generate_random(cls, card):

        limit = float(random.randint(1, 6) * 10000)
        balance = random.randint(0, limit) - limit

        card_id = card.card_id
        booked_balance = "{:.2f}".format(balance)
        available_balance_without_credit = 0
        currency = "NOK"
        credit_limit = "{:.2f}".format(limit)


        return CardBalance(card_id=card_id, booked_balance=booked_balance,
                           available_balance_without_credit=available_balance_without_credit,
                           currency=currency,
                           credit_limit=credit_limit)

    def __init__(self, card_id,
                 booked_balance, available_balance_without_credit,
                 currency, credit_limit):

        self.card_id = card_id
        self.booked_balance = booked_balance
        self.available_balance_without_credit = available_balance_without_credit
        self.currency = currency
        self.credit_limit = credit_limit

    def to_json(self):
        return {
            'card_id': self.card_id,
            'bookedBalance': self.booked_balance,
            'availableBalanceWithoutCredit': self.available_balance_without_credit,
            'currency': self.currency,
            'creditLimit': self.credit_limit,
        }

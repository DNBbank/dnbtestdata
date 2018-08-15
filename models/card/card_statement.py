import random
import exrex
from faker import Faker
import random
from datetime import date, timedelta
import json

from .elements.masked_card_number import MaskedCardNumber
from .elements.product_name import ProductName
from .elements.card_type import CardType
from .elements.card_status import CardStatus
from .elements.blocking_info import BlockingInfo


class CardStatement:
    @classmethod
    def generate_random(cls, card):

        SECONDS_IN_A_MONTH = 2592000
        randomDays = random.randint(0, 30)
        timestamp = date.today() - timedelta(days=randomDays)

        AMOUNT_PATTERN = "[1-9]\d{1,3}\.\d0"
        STATEMENT_ID_PATTERN = "\d{4}"
        TIMESTAMP_FORMAT = "YYYY-MM-DD"

        statement_id = exrex.getone(STATEMENT_ID_PATTERN)
        account_number =  card.account_number #11 chars
        currency = "NOK"
        opening_balance = exrex.getone(AMOUNT_PATTERN)
        closing_balance = exrex.getone(AMOUNT_PATTERN)
        minimum_due_amount = exrex.getone(AMOUNT_PATTERN)
        billing_date = timestamp.isoformat()
        statement_generated = timestamp.isoformat()
        due_date = timestamp.isoformat()
        current_closing_balance = exrex.getone(AMOUNT_PATTERN)
        instalment_account_balance = exrex.getone(AMOUNT_PATTERN)
        total_outstanding_balance = exrex.getone(AMOUNT_PATTERN)


        return CardStatement(statement_id = statement_id,
                    account_number = account_number,
                    currency = currency,
                    opening_balance = opening_balance,
                    closing_balance = closing_balance,
                    minimum_due_amount = minimum_due_amount,
                    billing_date = billing_date,
                    statement_generated = statement_generated,
                    due_date = due_date,
                    current_closing_balance = current_closing_balance,
                    instalment_account_balance = instalment_account_balance,
                    total_outstanding_balance = total_outstanding_balance)

    def __init__(self, statement_id, account_number, currency, opening_balance,
                closing_balance, minimum_due_amount, billing_date, statement_generated,
                due_date, current_closing_balance, instalment_account_balance,
                total_outstanding_balance):

        self.statement_id = statement_id
        self.account_number = account_number
        self.currency = currency
        self.opening_balance = opening_balance
        self.closing_balance = closing_balance
        self.minimum_due_amount = minimum_due_amount
        self.billing_date = billing_date
        self.statement_generated = statement_generated
        self.due_date = due_date
        self.current_closing_balance = current_closing_balance
        self.instalment_account_balance = instalment_account_balance
        self.total_outstanding_balance = total_outstanding_balance


    def to_json(self):
        return {
            "statementId": self.statement_id,
            "accountNumber": self.account_number,
            "currency": self.currency,
            "openingBalance": self.opening_balance,
            "closingBalance": self.closing_balance,
            "minimumDueAmount": self.minimum_due_amount,
            "billingDate": self.billing_date,
            "statementGenerated": self.statement_generated,
            "dueDate": self.due_date,
            "currentClosingBalance": self.current_closing_balance,
            "instalmentAccountBalance": self.instalment_account_balance,
            "totalOutstandingBalance": self.total_outstanding_balance

        }

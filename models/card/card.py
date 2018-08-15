import random
from faker import Faker
import exrex

from .elements.masked_card_number import MaskedCardNumber
from .elements.product_name import ProductName
from .elements.card_type import CardType
from .elements.card_status import CardStatus
from .elements.blocking_info import BlockingInfo

CARD_ID_PATTERN = "[A-Z]{4}\d{8}[A-Z]\d{2}[A-Z]"
CUSTOMER_ID_PATTERN = "[A-Z]{2}\d{14}[A-Z]"

class Card:
    @classmethod
    def generate_random(cls, account, card_type):
        fake = Faker('no_NO')
        card_id = exrex.getone(CARD_ID_PATTERN) #16 chars
        customer_id = exrex.getone(CUSTOMER_ID_PATTERN) # 18 chars
        customer_public_id = account["accountOwnerPublicId"]
        country_of_public_id = account["countryOfAccountOwnerPublicId"]

        #11 chars
        # Only debit cards are connected to an account number
        account_number = account["accountNumber"] if card_type == CardType.DEBIT else ""
        masked_card_number = MaskedCardNumber.generate_random() #11 * + 4 nums
        card_holder_name = account["accountOwnerName"] #from Account
        source_product_name = ProductName.generate_random_by_type(card_type)
        card_status = CardStatus.get_random()

        primary_card = str(random.choice(["true", "false"]))

        blocking_info = BlockingInfo.generate_random(card_status)




        return Card(card_id=card_id,
                    customer_id=customer_id,
                    customer_public_id=customer_public_id,
                    country_of_public_id=country_of_public_id,
                    account_number=account_number,
                    masked_card_number=masked_card_number,
                    card_holder_name=card_holder_name,
                    source_product_name=source_product_name,
                    card_status=card_status,
                    card_type=card_type,
                    primary_card=primary_card,
                    blocking_info=blocking_info)

    def __init__(self,
                 card_id, customer_id,
                 customer_public_id, country_of_public_id,
                 account_number, masked_card_number, card_holder_name,
                 source_product_name, card_status, card_type, primary_card,
                 blocking_info):

        self.card_id = card_id
        self.customer_id = customer_id
        self.customer_public_id = customer_public_id
        self.country_of_public_id = country_of_public_id
        self.account_number = account_number
        self.masked_card_number = masked_card_number
        self.card_holder_name = card_holder_name
        self.source_product_name = source_product_name
        self.card_status = card_status
        self.card_type = card_type
        self.primary_card = primary_card
        self.blocking_info = blocking_info


    def to_json(self):
        return {
            'cardId': self.card_id,
            'customerId': self.customer_id,
            'customerPublicId': self.customer_public_id,
            'countryOfPublicId': self.country_of_public_id,
            'accountNumber': self.account_number,
            'maskedCardNumber': self.masked_card_number,
            'cardHolderName': self.card_holder_name,
            'sourceProductName': self.source_product_name,
            'cardStatus': self.card_status.name,
            'cardType': self.card_type.name,
            'primary_card': self.primary_card,
            'blockingInfo': self.blocking_info
        }

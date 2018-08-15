#!/usr/bin/env python3
import argparse
import json
import numpy as np

from utils.file_util import FileUtil
from models.card.card import Card
from models.card.elements.card_type import CardType
from models.card.card_balance import CardBalance

CREDIT_CARD_PROBABILITY = [0.60, 0.40]
PRODUCTS_WITH_CARDS = ["BRUKSKONTO", "BRUKSKONTO TILLEGG", "STUDENT BRUKSKONTO"]

def create_cards(accounts):
    cards = list()
    for account in accounts:
        product_name = account["productName"]
        if product_name in PRODUCTS_WITH_CARDS:
            card = Card.generate_random(account, CardType.DEBIT)
            cards.append(card)

        should_add_credit_card = np.random.choice([True, False], p=CREDIT_CARD_PROBABILITY)
        if should_add_credit_card:
            credit_card = Card.generate_random(account, CardType.CREDIT)
            cards.append(credit_card)

    return cards

def create_card_balances(cards):
    balances = list()
    for card in cards:
        #Only generate balance for credit cards
        if card.card_type == CardType.CREDIT:
            balances.append(CardBalance.generate_random(card))
    return balances


# Handle CLI arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('accounts',
        help='A json file containing accounts to generate cards for. This file is typically output by the create_accounts.py script')
args = parser.parse_args()

# Business time
accounts_file = json.load(open(args.accounts))
cards = create_cards(accounts_file)
balances = create_card_balances(cards)
cards_json = list(map(lambda c: c.to_json(), cards))
balances_json = list(map(lambda s: s.to_json(), balances))

FileUtil.json_to_json_file(cards_json, 'generated-cards')
FileUtil.json_to_json_file(balances_json, 'generated-card-balances')

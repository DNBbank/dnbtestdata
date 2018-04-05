#!/usr/bin/env python3
""" Generate fake card credentials, given a list of people.

Uses Faker: https://github.com/joke2k/faker
"""

import argparse
import json
import random
from faker import Faker

def create_cards(persons):
    fake = Faker('no_NO')

    cards = list()
    for person in persons:
        # Between zero and three cards inclusive
        for i in range(0, random.randint(0, 3)):
            number = fake.credit_card_number()
            expiry_date = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
            cvc = fake.credit_card_security_code()

            # API: https://dnbdeveloper.restlet.io/#type_card
            card = {
                'owner': person['ssn'],
                'number': number,
                'expiry_date': expiry_date,
                'cvc': cvc,
            }

            cards.append(card)

    print(json.dumps(cards, indent=2))

# Handle CLI arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('people',
        help='A json file containing people to generate accounts for. This file is typically output by the create_people.py script')
args = parser.parse_args()

# Business time
create_cards(json.load(open(args.people)))

#!/usr/bin/env python3
""" Generate fake accounts, given a list of people.
"""

import argparse
import json
import operator
import random

_weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)

# See: https://no.wikipedia.org/wiki/Kontonummer
def _create_random_bban():
    while True:
        # 10 random digits
        digits = [random.randint(0, 9) for i in range(10)]

        # Modulo 11
        r = sum(map(operator.mul, digits, _weights)) % 11

        if r == 0:
            c = 0
        elif r == 1:
            # The control digit 10 is not allowed. We need to create a new
            # random account number
            continue
        else:
            c = 11 - r

        digits.append(c)
        return ''.join(str(x) for x in digits)


def _iban_from_bban(bban):
    check_digits = "42" # TODO: Calculate the check digits properly
    return "NO" + check_digits + bban

def create_accounts(persons):
    accounts = list()
    for person in persons:
        # Between one and five accounts inclusive
        for i in range(0, random.randint(1, 5)):
            bban = _create_random_bban()
            iban = _iban_from_bban(bban)

            # API: https://dnbdeveloper.restlet.io/#type_account
            account = {
                'owner': person['ssn'],
                'bban': bban,
                'iban': iban,
            }

            accounts.append(account)

    print(json.dumps(accounts, indent=2))

# Handle CLI arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('people',
        help='A json file containing people to generate accounts for. This file is typically output by the create_people.py script')
args = parser.parse_args()

# Business time
create_accounts(json.load(open(args.people)))

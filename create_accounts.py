#!/usr/bin/env python3
""" Generate fake accounts, given a list of people.
"""

import argparse
import json
import random

def _iban_from_bban(bban):
    check_digits = "42" # TODO: Calculate the check digits properly
    return "NO" + check_digits + bban

def create_accounts(persons):
    accounts = list()
    for person in persons:
        # Between one and five accounts inclusive
        for i in range(0, random.randint(1, 5)):
            bban = str(random.randint(0,99999999999)).zfill(11) # 11 random digits.
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

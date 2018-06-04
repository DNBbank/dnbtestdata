#!/usr/bin/env python3

# To test, run with persons.json as argument
''' Generate fake accounts, given a list of people.

TODO:
- logikk for BSU og student
- fikse epost-adresser så det gir mening i forhold til navn
- fikse æøå

'''

import argparse
import codecs
import operator
import json
import random
from datetime import date

today = date.today()
_weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)

# See: https://no.wikipedia.org/wiki/Kontonummer
def _create_random_bban():
    while True:
        # every digit starts with 120 and then 10 random digits
        digits = [random.randint(0, 9) for i in range(7)]

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

        digits.insert(0, 120)
        digits.append(c)
        return ''.join(str(x) for x in digits)

def make_account(person, account_type):
    #setting defaults
    debetCardExists = 'false'
    inDefaultStatus = 'false'
    accountCategory = 'DEPOSIT'
    standingOrderExists = 'false'
    productName = account_type
    withdrawalAllowed = 'true'
    transferToAllowed = 'true'
    paymentFromAllowed = 'true'
    accountAlias = ""
    transferFromAllowed = 'true'
    accountNumber = _create_random_bban()

    # setting specifics
    if account_type == 'LÅN':
        accountAlias = "Lån"
        accountCategory = 'LOAN'
        productName = random.choice(('RAMMELÅN', 'BOLIGLÅN'))
        withdrawalAllowed = 'false'
        transferFromAllowed = 'false'
        transferToAllowed = 'false'

    elif account_type == 'BRUKSKONTO' or account_type == 'BRUKSKONTO TILLEGG' or account_type == 'STUDENT BRUKSKONTO':
        debitCardExists = 'true'
        accountAlias = account_type.lower()
        randomNumber = random.randint(0,10)
        if randomNumber > 2:
            standingOrderExists = 'true'

    elif account_type == 'BSU' or account_type == 'SUPERSPAR' or account_type == 'AKSJESPAREKONTO':
        withdrawalAllowed: 'false'

    account = {
        'debetCardExists':      debetCardExists,
        'accountAlias':         accountAlias,
        'accountOwnerPublicId': person['ssn'],
        'inDefaultStatus':      'false',
        'accountCategory':      accountCategory,
        'accountCurrency':      'NOK',
        'withdrawalAllowed':    withdrawalAllowed,
        'accountNumber':        accountNumber,
        'productName':          productName,
        'transferToAllowed':    transferToAllowed,
        'paymentFromAllowed':   paymentFromAllowed,
        'transferFromAllowed':  transferFromAllowed,
        'standingOrderExists':  standingOrderExists,
        'countryOfAccountOwnerPublicId': 'NO',
        'accountOwnerName':     person['firstName'] + ' ' + person['lastName'],
    }

    return account

def calcuate_age(person):
    #def calculate_age(born):
    birthYear = int(person['dateOfBirth'][0:4])
    birthMonth = int(person['dateOfBirth'][5:7])
    birthDay = int(person['dateOfBirth'][8:11])
    return today.year - birthYear - ((today.month, today.day) < (birthMonth, birthDay))

def create_accounts(persons):
    accounts = list()
    # Guessed probability of having an specific account:
    account_types = {
        'BRUKSKONTO': 100,
        'SPAREKONTO': 65,
        'LÅN': 55,
        'BSU': 50,                  # should also be under the age of 34
        'BRUKSKONTO TILLEGG': 25,
        'AKSJESPAREKONTO': 25,
        'STUDENT BRUKSKONTO': 30,   # should be between 19 & 25
        'SUPERSPAR': 20,
    }

    for person in persons:
        age = calcuate_age(person)
        print(str(age))
        # A person has between one and six accounts
        number_of_accounts = random.randint(1,6)
        account_count = 0
        bsu_count = 0
        while account_count <= number_of_accounts:
            for account in account_types:
                # a person can not have more than 1 BSU account
                if account == 'BSU':
                    if age > 33:
                        break
                    elif bsu_count < 1:
                        bsu_count += 1
                    else:
                        break
                elif account == 'STUDENT BRUKSKONTO':
                    if age > 25 or age < 19:
                        break
                randomInt = random.randint(0,100)
                if randomInt <= account_types.get(account):
                    new_account = make_account(person, account)
                    accounts.append(new_account)
                    account_count += 1


    print(json.dumps(accounts, indent=2, ensure_ascii=False))
    with codecs.open('accounts.json', 'w', encoding='utf-8') as outfile:
        json.dump(accounts, outfile, ensure_ascii=False)


# Handle CLI arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('people',
        help='A json file containing people to generate accounts for. This file is typically output by the create_people.py script')
args = parser.parse_args()

# Business time
create_accounts(json.load(open(args.people)))

#!/usr/bin/env python3

# To test, run with accounts.json as argument

'''
Generate fake details of an account, given a list of accounts.
Code looks quite messy at the moment, as final outputs are still to be decided.

'''

import argparse
import json
import random
import codecs
from datetime import date, timedelta

today = date.today()

def get_balance_and_interestdetails(account, interestrate):
    interestDetails = list()
    ratioOfYear = today.month/12
    creditInterestPreviousYear = 0
    debitInterestThisYear = 0
    debitInterestPreviousYear = 0


    if account['accountCategory'] == 'LOAN':
        balance = round(random.randint(-5000000,0),2)
        debitInterestThisYear = 0
        debitInterestPreviousYear = 0
        creditInterestPreviousYear = balance * interestrate - random.uniform(0.0, 1.0) * balance * interestrate
    else:
        if account['productName'] == 'BSU':
            balance = random.randint(0,300000)
            savedThisYear = random.randint(0,balance)
            # Can max save 25000 in BSU per year
            if savedThisYear > 25000:
                savedThisYear = 25000
        elif account['productName'] == 'BRUKSKONTO' or  account['productName'] == 'BRUKSKONTO TILLEGG':
            balance = random.randint(0,40000)
        elif account['productName'] == 'SPAREKONTO' or  account['productName'] == 'SUPERSPAR':
            balance = random.randint(0,100000)
        else:
            balance = random.randint(0,200000)
        savedThisYear = random.randint(0,balance)
        debitInterestThisYear = savedThisYear * interestrate * ratioOfYear
        debitInterestPreviousYear = (balance * interestrate) - debitInterestThisYear
    interestDetails.extend((balance, debitInterestThisYear, debitInterestPreviousYear, creditInterestPreviousYear))
    return interestDetails

def get_last_transaction():
    # currently just returns yesterday's date
    # after transactions has been implemented, it should fetch from ther
    yesterday = today - timedelta(1)
    return (str(yesterday.year)+'-'+str(yesterday.month)+'-'+str(yesterday.day))

def get_opening_date(account):
    birthYear = account['accountOwnerPublicId'][4:6]
    thisYear = str(today.year)[2:4]
    if(int(birthYear) > int(thisYear)):
        fullBirthYear = '19' + birthYear
    else:
        fullBirthYear = '20' + birthYear.zfill(2)

    thisYearLong = int('20'+str(thisYear))
    birthYearLong = int(fullBirthYear)
    random_year = random.randint(birthYearLong, thisYearLong)
    random_month = random.randrange(13)
    random_day = random.randrange(29)
    openingDate = str(random_year) + '-' + str(random_month).zfill(2) + '-' + str(random_day).zfill(2)
    return openingDate

def create_account_details(accounts):
    account_details_list = list()
    account_balances = list()

    interest_rates = {
        'BRUKSKONTO': 0.1,
        'SPAREKONTO': 0.5,
        'RAMMELÅN': 2.5,
        'BOLIGLÅN': 2.65,       # varies a lot
        'BSU': 3.2,
        'BRUKSKONTO TILLEGG': 0.1,
        'AKSJESPAREKONTO': 0,
        'STUDENT BRUKSKONTO': 0.1,   # should be between 19 & 25
        'SUPERSPAR': 1.2,
    }

    for account in accounts:
        accountNumber               = account['accountNumber']
        interestRate                = interest_rates.get(account['productName'])
        returnlist                  = get_balance_and_interestdetails(account, interestRate)
        balance                     = returnlist[0]
        debitInterestThisYear       = returnlist[1]
        debitInterestPreviousYear   = returnlist[2]
        creditInterestPreviousYear  = returnlist[3]

        lastTransactionDate = get_last_transaction()
        iban = 'NO' + str(random.randint(0,99)).zfill(2) + accountNumber
        openingDate = get_opening_date(account)
        account_details = {
            'accountUserRoles': [
                {
                    'roleOwnerName': account['accountOwnerName'],
                    'roleType':      'OWNER'
                }
            ],
            'accountCurrency': 'NOK',
            'accountNumber':   accountNumber,
            'accumulators': [
                {
                    'debitInterestPreviousYear':   debitInterestPreviousYear,
                    'feesThisYear':                0.00,       # don't know about fee strucutre for accounts
                    'debitInterestThisYear':       debitInterestThisYear,
                    'creditInterestPreviousYear':  creditInterestPreviousYear,
                }
            ],
            'depositInterestRates': [
                {
                    'depositThreshold':     0,                          # 25k for bsu?
                    'depositRate':          interestRate
                }
             ],
             'interestCalculationMethod':   'BALANCE',              # what's this
             'lastTransactionDate':         lastTransactionDate,
             'iban':                        iban,
             'overdraftInterestRate':       0,
             'bic':                         'DNBANOKKXXX',
             'openingDate':                 openingDate
             }

        account_details_list.append(account_details)

        account_balance = {
            'bookedBalance': balance,
            'availableBalanceWithoutCredit': balance,
            'availableBalanceWithoutCredit': balance,
            'accountCurrency': 'NOK',
            'creditLimit': 0,
            'accountNumber': accountNumber
        }
        account_balances.append(account_balance)


    print(json.dumps(account_details_list, indent=2, ensure_ascii=False))
    with codecs.open('account_details.json', 'w', encoding='UTF-8') as outfile:
        json.dump(account_details_list, outfile, ensure_ascii=False)

    print(json.dumps(account_balances, indent=2, ensure_ascii=False))
    with codecs.open('account_balances.json', 'w', encoding='UTF-8') as outfile:
        json.dump(account_balances, outfile, ensure_ascii=False)


# Handle CLI arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('accounts',
        help='A json file containing accounts to generate account details for. This file is typically output by the create_accounts.py script')
args = parser.parse_args()

# Business time
create_account_details(json.load(open(args.accounts)))

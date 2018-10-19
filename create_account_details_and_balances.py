#!/usr/bin/env python3
import argparse
import json
import random
from datetime import date

from models.account.account_balance import AccountBalance
from models.account.account_details import AccountDetails
from models.account.elements.account_type import interest_rates
from utils.file_util import FileUtil


def get_balance_and_interest_details(account, interest_rate):
    interest_details = list()
    ratio_of_year = date.today().month / 12
    credit_interest_previous_year = 0
    debit_interest_this_year = 0
    debit_interest_previous_year = 0

    if account['accountCategory'] == 'LOAN':
        balance = round(random.randint(-5000000, 0), 2)
        debit_interest_this_year = 0
        debit_interest_previous_year = 0
        credit_interest_previous_year = balance * interest_rate - random.uniform(0.0, 1.0) * balance * interest_rate
    else:
        if account['productName'] == 'BSU':
            balance = random.randint(0, 300000)
            saved_this_year = random.randint(0, balance)
            # Can max save 25000 in BSU per year
            if saved_this_year > 25000:
                saved_this_year = 25000
        elif account['productName'] == 'BRUKSKONTO' or account['productName'] == 'BRUKSKONTO TILLEGG':
            balance = random.randint(0, 40000)
        elif account['productName'] == 'SPAREKONTO' or account['productName'] == 'SUPERSPAR':
            balance = random.randint(0, 100000)
        else:
            balance = random.randint(0, 200000)
        saved_this_year = random.randint(0, balance)
        debit_interest_this_year = saved_this_year * interest_rate * ratio_of_year
        debit_interest_previous_year = (balance * interest_rate) - debit_interest_this_year
    interest_details.extend(
        (balance, debit_interest_this_year, debit_interest_previous_year, credit_interest_previous_year))
    return interest_details


def create_list_of_account_detail_json(accounts):
    account_details = list()

    for account in accounts:
        account_detail = AccountDetails.generate_random_account_detail_json(account)
        account_details.append(account_detail)
    return account_details


def create_list_of_account_balance_json(accounts):
    account_balances = list()

    for account in accounts:
        account_balance = AccountBalance.generate_random_account_balance_json(account)
        account_balances.append(account_balance)
    return account_balances


def create_account_detail_and_account_balance_files(accounts):
    account_details = list()
    account_balances = list()

    for account in accounts:
        account_number = account['accountNumber']
        interest_rate = interest_rates.get(account['productName'])
        return_list = get_balance_and_interest_details(account, interest_rate)
        balance = return_list[0]

        account_detail = AccountDetails.generate_random_account_detail_json(account, return_list)
        account_balance = AccountBalance.generate_random_account_balance_json(account_number, balance)

        account_details.append(account_detail)
        account_balances.append(account_balance)

    FileUtil.json_to_json_file(account_details, 'generated-account-details')
    FileUtil.json_to_json_file(account_balances, 'generated-account-balances')


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('accounts',
                    help='A json file containing accounts to generate account details for. '
                         'This file is typically output by the create_accounts.py script')
args = parser.parse_args()

with open(args.accounts, encoding='utf-8') as fh:
    create_account_detail_and_account_balance_files(json.load(fh))

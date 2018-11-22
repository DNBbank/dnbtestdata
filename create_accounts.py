#!/usr/bin/env python3
import argparse
import json
import random

from models.account.account import Account
from models.account.elements.account_type import account_types_with_probability
from models.person.elements.date_of_birth import DateOfBirth
from utils.file_util import FileUtil


def create_list_of_account_json(persons):
    accounts = list()

    for person in persons:
        age = DateOfBirth.from_string(person["dateOfBirth"]).calculate_age()

        # A person has between one and six accounts
        number_of_accounts = random.randint(1, 6)
        account_count = 0
        bsu_count = 0
        while account_count <= number_of_accounts:
            for account_type in account_types_with_probability:
                # a person can not have more than 1 BSU account
                if account_type == 'BSU':
                    if age > 33:
                        break
                    elif bsu_count < 1:
                        bsu_count += 1
                    else:
                        break
                elif account_type == 'STUDENT BRUKSKONTO':
                    if age > 25 or age < 19:
                        break
                random_int = random.randint(0, 100)
                if random_int <= account_types_with_probability.get(account_type):
                    new_account = Account.generate_random_account_json(person, account_type)
                    accounts.append(new_account)
                    account_count += 1
    return accounts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('people',
                        help='A json file containing people to generate accounts for. '
                             'This file is typically output by the create_people.py script')
    args = parser.parse_args()

    with open(args.people, encoding='utf-8') as fh:
        FileUtil.json_to_json_file(create_list_of_account_json(json.load(fh)), 'generated-accounts')

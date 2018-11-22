import argparse

from utils.file_util import FileUtil

from create_people import create_list_of_people_json
from create_accounts import create_list_of_account_json
from create_account_details_and_balances import create_account_detail_and_account_balance_files
from create_payments import create_payments
from create_payments import save_payments_to_json
from create_cards_and_card_balances import create_cards
from create_cards_and_card_balances import create_card_balances


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate people along with associated account data.")
    parser.add_argument('-n', type=int, default=10, help='The number of people to create')
    args = parser.parse_args()

    # Create a list of people to use
    # 'generated-people' json file created
    people = create_list_of_people_json(args.n)
    print('\nCreated people\n')
    FileUtil.json_to_json_file(people, 'generated-people')

    # Create between 1 and 6 accounts for each person
    # 'generated-accounts' json file created
    accounts = create_list_of_account_json(people)
    print('\nCreated accounts\n')
    FileUtil.json_to_json_file(accounts, 'generated-accounts')

    # Create details for each of the accounts
    # 'generated-account-details' and 'generated-account-balances' json files created
    balances = create_account_detail_and_account_balance_files(accounts)
    print('\nCreated account details\n')
    FileUtil.json_to_json_file(balances, 'generated-card-balances')

    # Add fake payments for each of the accounts
    # 'generated-booked-transactions', 'generated-due-payments' and 'generated-reserved-transactions' json files created
    print('Generating payments for each account...')
    payments = list()
    for data in accounts:
        ret = create_payments(data)
        payments.append(ret)
    save_payments_to_json(payments)
    print('\nCreated payments\n')

    # Create cards for each of the accounts
    # 'generated-cards' json file created
    cards = create_cards(accounts)
    cards_json = list(map(lambda c: c.to_json(), cards))
    FileUtil.json_to_json_file(cards_json, 'generated-cards')
    print('\nCreated cards\n')

    # Create balances for each of the cards
    # 'generated-card-balances' json file created
    balances = create_card_balances(cards)
    balances_json = list(map(lambda s: s.to_json(), balances))
    FileUtil.json_to_json_file(balances_json, 'generated-card-balances')
    print('\nCreated balances\n')

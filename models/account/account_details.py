import random

from models.account.elements.account_type import interest_rates
from models.account.elements.last_transaction import get_last_transaction
from models.account.elements.opening_date import get_opening_date


class AccountDetails:
    @classmethod
    def generate_random_account_detail_json(cls, account, return_list):
        account_number = account['accountNumber']
        interest_rate = interest_rates.get(account['productName'])
        debit_interest_this_year = return_list[1]
        debit_interest_previous_year = return_list[2]
        credit_interest_previous_year = return_list[3]

        last_transaction_date = get_last_transaction()
        iban = 'NO' + str(random.randint(0,99)).zfill(2) + account_number
        opening_date = get_opening_date(account)
        account_details = {
            'accountUserRoles': [
                {
                    'roleOwnerName': account['accountOwnerName'],
                    'roleType':      'OWNER'
                }
            ],
            'accountCurrency': 'NOK',
            'accountNumber':   account_number,
            'accumulators': [
                {
                    'debitInterestPreviousYear':   debit_interest_previous_year,
                    'feesThisYear':                0.00,       # don't know about fee strucutre for accounts
                    'debitInterestThisYear':       debit_interest_this_year,
                    'creditInterestPreviousYear':  credit_interest_previous_year,
                }
            ],
            'depositInterestRates': [
                {
                    'depositThreshold':     0,                          # 25k for bsu?
                    'depositRate':          interest_rate
                }
            ],
            'interestCalculationMethod':   'BALANCE',              # what's this
            'lastTransactionDate':         last_transaction_date,
            'iban':                        iban,
            'overdraftInterestRate':       0,
            'bic':                         'DNBANOKKXXX',
            'openingDate':                 opening_date,
            'salesProductId':              '104466',
            'salesProductName':            'AKSJESPAREKONTO OVER INTERNETT',
            'transactionRestrictions': [
                {
                    'blockingRestriction':          '',
                    'restrictedWithdrawalAmount':   0,
                    'freeWithdrawals':              0,
                    'remainingFreeWithdrawals':     0
                },
            ],
        }

        return account_details

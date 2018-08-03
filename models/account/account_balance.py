class AccountBalance:
    @classmethod
    def generate_random_account_balance_json(cls, account_number, balance):
        account_balance = {
            'bookedBalance': balance,
            'availableBalanceWithoutCredit': balance,
            'accountCurrency': 'NOK',
            'creditLimit': 0,
            'accountNumber': account_number
        }

        return account_balance

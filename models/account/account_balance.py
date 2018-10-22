class AccountBalance:
    @classmethod
    def generate_random_account_balance_json(cls, account_number, balance):
        account_balance = {
            'availableBalanceWithCredit': balance,
            'availableBalanceWithoutCredit': balance,
            'bookedBalance': balance,
            'accountNumber': account_number,
            'accountCurrency': 'NOK',
            'creditLimit': 0
        }

        return account_balance

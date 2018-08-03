import random

from .elements.bban import Bban


class Account:
    @classmethod
    def generate_random_account_json(cls, person, account_type):
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
        accountNumber = Bban.generate_random_bban()

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
            withdrawalAllowed = 'false'

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


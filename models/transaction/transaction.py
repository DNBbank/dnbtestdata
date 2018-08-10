class Transaction:

    def __init__(self, transaction_id, account_number, transaction_date, description, amount, external_reference, payment_type):
        self.transactionId = transaction_id
        self.accountNumber = account_number
        self.bookingDate = transaction_date
        self.transactionDate = transaction_date
        self.description = description
        self.valueDate = transaction_date
        self.amount = amount
        self.externalReference = external_reference
        sefl.textlines = {
            'Item':     payment_type
         }
         self.details = {
            'textCode': '0023'
         }

#!/usr/bin/env python3

'''
A script to create payments and transactions on an accounts
To test, run with a list of accounts (.json) as an argument

        # due payments - no impact on balance
        # booked transactions - already done
        # reserved_transaction - impact on balance

TODO:
- Dates should be changed to datetime formats

FIXME: performance, for 100 generated people this script will run for 5 minutes
'''

import argparse
import codecs
import operator
import json
import random
from faker import Faker
from datetime import date, timedelta, datetime
import pandas as pd
from models.transaction.checking_account import CheckingAccount

today = date.today()
fake = Faker('no_NO')
weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
filename_payments = 'generated-due-payments-' + str(today.day).zfill(2) + '-' + str(today.month).zfill(2) + '-' + str(today.year) + '.json'
filename_booked_transactions = 'generated-booked-transactions-' + str(today.day).zfill(2) + '-' + str(today.month).zfill(2) + '-' + str(today.year) + '.json'
filename_reserved_transactions = 'generated-reserved-transactions-' + str(today.day).zfill(2) + '-' + str(today.month).zfill(2) + '-' + str(today.year) + '.json'

def create_bban():
    while True:
        digits = [random.randint(0, 9) for i in range(10)]
        # Modulo 11
        r = sum(map(operator.mul, digits, weights)) % 11
        if r == 0:
            c = 0
        elif r == 1:
            # The control digit 10 is not allowed. We need to create a new
            # random account number
            continue
        else:
            c = 11 - r
        digits.append(c)
        return ''.join(str(x) for x in digits)

def message_or_kid():
    randomNumber = random.getrandbits(1)
    if(randomNumber):
        message =   fake.sentence(nb_words=4, variable_nb_words=True, ext_word_list=None)
        kid =       ''
    else:
        message = ''
        kid_length = random.randint(5,25)
        kid_list = [random.randint(0, 9) for i in range(kid_length)]
        kid     = ''.join(str(x) for x in kid_list)
    return (message, kid)

def get_date(type, day):
    if type=='future':
        #due payments are in the future
        random_number = random.randint(0,30)
        date = today + timedelta(random_number)
    elif type=='previous':
        #already happended transactions:
        date = today - timedelta(day)
    elif type=='valuedate':
        # the date a reserved transaction was set
        how_many_days_back = random.randint(30,60)
        date = today - timedelta(how_many_days_back)
    return (str(date.year)+'-'+str(date.month).zfill(2)+'-'+str(date.day).zfill(2))

def get_amount(type):
    random_number = random.randint(1,10)
    treshold = 7
    # Assign a negative weight if the transactions are a type of payment
    if type in ['payment','Varekjøp','Avtalegiro','Fast Oppdrag']:
        weight = "-"
    else:
        # is the transaction a debit or credit
        if random_number < treshold:
            weight = "-"
        else:
            weight = ""
    if random_number < treshold:
        # most payments are of lower amounts
        amount = random.randint(0,1500)
    else:
        amount = random.randint(0,10000)
    return weight + str(amount) + '.00'

def get_paymentId():
    digits = [random.randint(0, 9) for i in range(7)]
    return ''.join(str(x) for x in digits)

def get_transaction_description(payment_type, transaction_date):
    if payment_type=='Varekjøp':
        store_list = ['Kiwi', 'Rema 1000', 'Meny', 'Joker', 'Vinmonopolet', fake.company()]
        store = random.choice(store_list) + ' '
        city_list = ['Oslo', 'Trondheim', 'Bergen', fake.city()]
        city = random.choice(city_list) + ' '
        date = str(transaction_date[-2:]).zfill(2) + '.' + str(transaction_date[5:7]).zfill(2) + ' '
        hour = str(random.randint(1,24)).zfill(2)
        minute = str(random.randint(1,60)).zfill(2)
        time = 'kl. ' + hour + '.' + minute
        description = payment_type + ' ' + store + city + 'Dato ' + date + time
    elif payment_type=='Overføring':
        name = fake.first_name() + ' ' + fake.last_name() + ' '
        number_in_description = str(random.randint(1000000000,9999999999)) + ' '
        description = payment_type + ' ' + number_in_description + name
    else:
        number_in_description = str(random.randint(100,999))
        description = payment_type + ' ' + number_in_description
    return description

def get_payment_type():
    x = random.randint(0,10)
    # Kun negativ: Avtalegiro, Varekjøp, Visa
    payment_types = ['Mobiloverføring', 'Avtalegiro', 'Overføring', 'Fast Oppdrag', 'Varekjøp', 'Visa', 'Kontoregulering']
    if x < 4:
        payment_type = 'Varekjøp'
    else:
        payment_type = random.choice(payment_types)
    return payment_type


def create_payments(accounts):
    due_payments = list()
    booked_transactions = list()
    reserved_transactions = list()
    done_accounts = 0

    # generating for all the different accounts
    for account in accounts:
        # only generating for current accounts
        if account['productName'] in ['BRUKSKONTO','BRUKSKONTO TILLEGG','STUDENT BRUKSKONTO']:
            no_of_due_payments = random.randint(1,7) # must generate
            no_of_reserved_transactions = random.randint(1,3) # must generate
            account_number = account['accountNumber']
            account_owner_ssn = account['accountOwnerPublicId']
            # generating with some transactions each day
            for day in range(1, 30):
                trans_count = random.randint(0,2)
                resv_trans_count = 0
                no_of_transactions = 0

                while resv_trans_count < no_of_reserved_transactions:
                    # random_number = random.randint(0,5)
                    transaction_id   =  str(random.randint(100000, 9999999))
                    transaction_date =  get_date('previous', day)
                    payment_type = get_payment_type()
                    amount =            get_amount(payment_type)
                    external_reference = random.randint(100000, 9999999)
                    description = get_transaction_description(payment_type, transaction_date)

                    # if resv_trans_count < no_of_reserved_transactions and random_number<3:
                    value_date = get_date('valuedate', day)
                    reserved_transaction = {
                            'ssn':              account_owner_ssn, # Only used for grouping
                            'transactionId':    transaction_id,
                            'accountNumber':    account_number,
                            'reservationDate':  transaction_date,
                            'transactionDate':  transaction_date,
                            'description':      description,
                            'valueDate':        value_date,
                            'amount':           amount,
                            'externalReference': external_reference,
                            'textlines':{
                                'Item': payment_type
                                },
                            'details':{
                                'textCode':'0023'
                            }
                    }
                    reserved_transactions.append(reserved_transaction)
                    resv_trans_count += 1

                    # else:
                    #     booked_transaction = {
                    #         'transactionId':    transaction_id,
                    #         'accountNumber':    account_number,
                    #         'bookingDate':      transaction_date,
                    #         'transactionDate':  transaction_date,
                    #          'description':     description,
                    #          'valueDate':       transaction_date,
                    #          'amount':          amount,
                    #          'externalReference':   external_reference,
                    #          'textlines':{
                    #             'Item':     payment_type
                    #          },
                    #          'details':{
                    #             'textCode': '0023'
                    #          }
                    #     }
                    #     booked_transactions.append(booked_transaction)
                    #     no_of_transactions += 1

            # Generating Booked Payments (transactions) for a checking account (BRUKSKONTO)
            booked_transactions.extend(CheckingAccount(account_number, account_owner_ssn).transactions)
            done_accounts += 1
            print('Finished account nr.', done_accounts)


            # Generating due payments
            count = 0
            while count < no_of_due_payments:
                payment_type = get_payment_type
                creditAccountNumber =   create_bban()
                message, kid =  message_or_kid()
                amount =        get_amount('payment')
                paymentId  =    get_paymentId()

                due_payment = {
                     'debitAccountNumber':  account_number,
                     'creditAccountNumber': creditAccountNumber,
                     'message':             message,
                     'kid':                 kid,
                     'requestedExecutionDate': get_date('future', 1),
                     'country':             'NO',
                     'currency':            'NOK',
                     'amount':              amount,
                     'paymentId':           paymentId,
                     'immediatePayment':    'false'
                }
                due_payments.append(due_payment)
                count += 1


    # Due Payments
    #print(json.dumps(due_payments, indent=2, ensure_ascii=False))
    with codecs.open(filename_payments, 'w', encoding='utf-8') as outfile:
        json.dump(due_payments, outfile, ensure_ascii=False)

    # Booked trasactions
    #print(json.dumps(booked_transactions, indent=2, ensure_ascii=False))
    with codecs.open(filename_booked_transactions, 'w', encoding='utf-8') as outfile:
        json.dump(booked_transactions, outfile, ensure_ascii=False)

    # Reserved trasactions
    #print(json.dumps(reserved_transactions, indent=2, ensure_ascii=False))
    with codecs.open(filename_reserved_transactions, 'w', encoding='utf-8') as outfile:
        json.dump(reserved_transactions, outfile, ensure_ascii=False)


# Handle CLI arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('accounts',
        help='A json file containing accounts to generate account details for. This file is typically output by the create_accounts.py script')
args = parser.parse_args()

# Business time
create_payments(json.load(open(args.accounts)))

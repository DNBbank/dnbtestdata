#!/usr/local/bin/python3
""" Quick hack to generate fake people and some data.

Uses Faker quite a bit: https://github.com/joke2k/faker

TODO:
- Valid Norwegian SSNs: https://github.com/joke2k/faker/issues/714
- Bank accounts: One or more per person: https://github.com/joke2k/faker/pull/726
- Debit cards: One or more per person
- Transactions (this is the interesting part):
    - Salary
    - Mortgage (for some)
    - Insurance (for some)
    - Utilities (electricity, public fees, etc)
    - Car related expenses (for some)
    - Food, transport, other everyday transactions
    - Various other purchases
    - Ideally: In segments/groups, with patterns, etc (endless possibilities to make it "realistic")
"""

__author__ = "Christian Løverås"
__contact__ = "cl@dnb.no"
__copyright__ = "Copyright 2018, DNB Open Banking"
__license__ = "GPLv3"
__status__ = "Hack"
__version__ = "0.0.2"

import requests
import json
import random
import datetime
from random import randrange
from random import choice
from faker import Faker

def get_random_birthdate(max_age = 100):
    this_year = datetime.datetime.now().year
    random_year = randrange(this_year - max_age, this_year)
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random_year), '%j %Y')
    # Leap year? Try again.
    except ValueError:
        get_random_date(random_year)

def create_people (number_of_people):
    fake = Faker('no_NO')

    # Files to create, or append to
    customerFileTxt = open('customers-generated.txt', 'a')
    customerFileJson = open('customers-generated.json', 'a')

    # People of the world!
    for i in range(number_of_people):

        # Birth date
        random_date = get_random_birthdate(100)
        year, month, day = [random_date.year, random_date.month, random_date.day]
        date_of_birth = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)

        # SSN: Faking it until Faker supports Norwegian SSNs: https://github.com/joke2k/faker/issues/714
        pnr = str(randrange(10000,99999)).zfill(6)
        ssn = str(day).zfill(2) + str(month).zfill(2) + str(year)[-2] + pnr

        # Name and gender
        if random.choice((True,False)):
            gender = 'Female'
            first_name = fake.first_name_female()
        else:
            gender = 'Male'
            first_name = fake.first_name_male()
        last_name = fake.last_name()

        # Contact information
        street = fake.street_name() + ' ' + fake.building_number()
        postal_code = fake.postcode()
        city = fake.city()
        phone = fake.phone_number()
        email = fake.safe_email()
        id_type = random.choice(('passport', 'driverslicense', 'nationalidcard'))

        # Bank account and credit card
        bank_account_bban = str(randrange(0,99999999999)).zfill(11) # 11 random digits. Not the same as IBAN below
        bank_account_iban = fake.iban() # No provider for no_NO in Faker (yet)

        # Maybe a credit card. Let's assume 95 % has one
        if randrange(0,100) > 5:
            credit_card_no = fake.credit_card_number()
            credit_card_expiry_date = fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y")
            credit_card_cvc = fake.credit_card_security_code()
        else:
            credit_card_no = ''
            credit_card_expiry_date = ''
            credit_card_cvc = ''

        # JSON
        # API: https://dnbdeveloper.restlet.io/#type_customer
        person = {
            'personal_number': ssn,
            'firstName': first_name,
            'lastName': last_name,
            'dateOfBirth': date_of_birth,
            'gender': gender,
            'nationality': 'Norwegian',
            'address': {
                'street': street,
                'postalCode': postal_code,
                'city': city,
                'country': 'NO',
            },
            'phoneNumber': phone,
            'email': email,
            'idType': id_type,
            'bank_account_iban': bank_account_iban,
            'credit_card_no': credit_card_no,
            'credit_card_expiry_date': credit_card_expiry_date,
            'credit_card_cvc': credit_card_cvc
        }
        data = json.dumps(person)

        # Write to files in JSON and text format
        customerFileJson.write(data + '\n\n')

        # The person's data in a string
        person_data = str('%r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r' %
                          (ssn, first_name, last_name, gender, street, postal_code, city, phone, email, id_type,
                           bank_account_bban, bank_account_iban, credit_card_no, credit_card_expiry_date, credit_card_cvc))

        # Write to file
        customerFileTxt.write(person_data + '\n')
        # Be chatty
        print(person_data + '\n')

# Business time
create_people(10)

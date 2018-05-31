#!/usr/bin/env python3
""" Quick hack to generate fake people and some data.

Uses Faker quite a bit: https://github.com/joke2k/faker

TODO:
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

import argparse
import datetime
import json
import random
from random import randrange

from faker import Faker

def get_random_birthdate(max_age = 100):
    this_year = datetime.datetime.now().year
    random_year = randrange(this_year - max_age, this_year)
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random_year), '%j %Y')
    # Leap year? Try again.
    except ValueError:
        get_random_date(random_year)


def create_people(number_of_people):
    fake = Faker('no_NO')

    persons = list()
    for i in range(number_of_people):
        # Birth date
        random_date = get_random_birthdate(100)
        year, month, day = [random_date.year, random_date.month, random_date.day]
        date_of_birth = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)

        # Name and gender
        if random.choice((True,False)):
            gender = 'Female'
            gender_indicator = random.choice(('0','2','4','6','8'))
            first_name = fake.first_name_female()
        else:
            gender = 'Male'
            first_name = fake.first_name_male()
            gender_indicator = random.choice(('1','3','5','7','9'))
        last_name = fake.last_name()

        # SSN: Faking it until Faker supports Norwegian SSNs: https://github.com/joke2k/faker/issues/714
        pnr = str(random.randint(0,99)).zfill(2) + gender_indicator + str(random.randint(0,99)).zfill(2)
        ssn = str(day).zfill(2) + str(month).zfill(2) + str(year)[-2:] + pnr

        # Contact information
        street = fake.street_name() + ' ' + fake.building_number()
        postal_code = fake.postcode()
        city = fake.city()
        phone = fake.phone_number()
        email = fake.safe_email()
        id_type = random.choice(('passport', 'driverslicense', 'nationalidcard'))
        nationality = 'Norwegian'
        country = 'NO'

        # API: https://dnbdeveloper.restlet.io/#type_customer
        person = {
            'ssn': ssn,
            'firstName': first_name,
            'lastName': last_name,
            'dateOfBirth': date_of_birth,
            'gender': gender,
            'nationality': nationality,
            'address': {
                'street': street,
                'postalCode': postal_code,
                'city': city,
                'country': country,
            },
            'phoneNumber': phone,
            'email': email,
            'idType': id_type,
        }

        persons.append(person)

    print(json.dumps(persons, indent=2))

# Handle CLI arguments
parser = argparse.ArgumentParser(description="Quick hack to generate fake people and some data.")
parser.add_argument('-n', type=int, default=10, help='The number of people to create')
args = parser.parse_args()

# Business time
create_people(args.n)

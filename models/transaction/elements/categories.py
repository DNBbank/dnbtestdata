import datetime
import math
import random
from datetime import timedelta, date

import pprint
import json

# Import packages
import numpy as np
import pandas as pd
from faker import Faker

nr_cat = 16  # Number of predefined categories
nr_freq = 3  # Number of predefined frequencies
fake = Faker('no_NO')

# Generate a Date range for year
year = 2018
start_date = date(year, 1, 1)
end_date = date(year, 12, 31)
year_range = []
for n in range(365):
    d = start_date + timedelta(n)
    year_range.append(d.strftime("%Y-%m-%d"))

# Categories with some mean amounts, recurrency indicator etc.
# Can be expanded to include customer segments, with different mean amounts
categories = pd.DataFrame([['Loans&Rent', 1, 1, 'Out', 10000, 0],
                           ['Utilities', 2, 1, 'Out', 2000, 0],
                           ['Home', 3, 0, 'Out', 1000, 30],
                           ['Transport', 4, 2, 'Out', 1000, 10],
                           ['Groceries', 5, 0, 'Out', 500, 100],
                           ['Health', 6, 0, 'Out', 500, 10],
                           ['Culture&Activities', 7, 2, 'Out', 200, 30],
                           ['Travel', 8, 0, 'Out', 5000, 20],
                           ['Restaurants&Nightlife', 9, 0, 'Out', 200, 50],
                           ['Shopping', 10, 0, 'Out', 400, 30],
                           ['Savings', 11, 1, 'Out', 3000, 0],
                           ['Salary', 12, 1, 'In', 30000, 0],
                           ['Various In', 13, 0, 'In', 200, 40],
                           ['Various Out', 14, 0, 'Out', 200, 60],
                           ['Subscriptions', 15, 1, 'Out', 150, 0],
                           ['Insurance', 16, 1, 'Out', 150, 0]],
                          columns=['CategoryName', 'CategoryLabel', 'RegularInd', 'InOut', 'Mean', 'MaxTrans'])

store_list_by_category = {
                        'Loans&Rent': ['Rentebetalinger'],
                        'Utilities': ['Clas Ohlson', 'Biltema', 'Kondomeriet', 'Bohus', 'Byggmaker', 'Mekonomen', 'Elkjøp'],
                        'Home': ['HM Home', 'Kid', 'Ikea', 'Princess', 'Zara Home', 'Jysk', 'Nille', 'Skeidar', 'Bohus'],
                        'Transport': ['Ruter', 'NSB', 'Bysykkel', 'Fjordline','Oslo Taxi'],
                        'Groceries': ['Kiwi','Rema 1000','Bunnpris','Coop','Spar', 'Meny', 'Vinmonopolet'],
                        'Health': ['Boots', 'Apotek1', 'Vita', 'Proteinfabrikken', 'Life'],
                        'Culture&Activities': ['Den norske opera'],
                        'Travel': ['SAS', 'Norwegian', 'Wideroe', 'Polskibuss', 'Flixbuss', 'Ryan Air'],
                        'Restaurants&Nightlife': ['Olivia',"Dit pepper'n gror",'Big Horn Steak House','McDonalds','Stratos','Syng','Max','Heidis', 'Kulturhuset', 'Blå'],
                        'Shopping': ['H&M', 'Gucci', 'Burberry', 'Hermes', 'Zara', 'Carlings', 'BikBok'],
                        'Savings': ['Overføring til sparekonto'],
                        'Salary': ['LØNN DNB'],
                        'Various In': ['Vipps fra'], # Remove?
                        'Various Out': ['Vipps til'], # Remove?
                        'Subscriptions': ['Spotify', 'Tinder Gold', 'Netflix', 'HBO Nordic'],
                        'Insurance': ['Betaling til DNB Liv', 'Avtalegiro Gjensidige']
                        }

payment_categories = ['Utilities','Home','Groceries','Health','Restaurants&Nightlife','Shopping']
visa_categories = ['Subscriptions']
# Frequency dataframe for recurrent payments
frequencies = pd.DataFrame([['Monthly', 1, 30],
                            ['Quarterly', 2, 183],
                            ['Yearly', 3, 365]], columns=['FreqName', 'FreqLabel', 'Duration'])

# Probabilites for each category
cat_prob = [0.100,  # Loans&Rent
            0.075,  # Utilities
            0.050,  # Home
            0.050,  # Transport
            0.115,  # Groceries
            0.020,  # Health
            0.065,  # Culture&Activities
            0.040,  # Travel
            0.065,  # Restaurants&Nightlife
            0.055,  # Shopping
            0.050,  # Savings
            0.145,  # Salary
            0.015,  # Various In
            0.015,  # Various Out
            0.075,  # Subscriptions
            0.065]  # Insurance

# Custom time delta to handle recurrent payments
def custom_delta(start, freq, from_m, end):
    if freq == 1:
        if from_m in [1, 3, 5, 7, 8, 10]:
            return start + timedelta(days=31)
        elif from_m in [2]:
            return start + timedelta(days=28)
        elif from_m in [4, 6, 9, 11]:
            return start + timedelta(days=30)
        else:
            return end
    elif freq == 2:
        if from_m in [1]:
            return start + timedelta(days=90)
        elif from_m in [2]:
            return start + timedelta(days=89)
        elif from_m in [3, 4, 6, 9]:
            return start + timedelta(days=91)
        elif from_m in [5, 6, 7, 8]:
            return start + timedelta(days=92)
        else:
            return end
    else:
        return end

# Get random date in specified year
def get_random_date(year):
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')
    # Leap year? Try again.
    except ValueError:
        get_random_date(random_year)

def get_transaction_description(payment_category, transaction_date):
    if payment_category in payment_categories:
        store_list = store_list_by_category[payment_category]
        store = random.choice(store_list) + ' '
        # TODO: Here it is possible to use the API from Gulesider http://api.eniro.com/
        # to get an actual store based on a category in the same city as the customer
        city_list = ['Oslo', 'Trondheim', 'Bergen', fake.city()]
        city = random.choice(city_list) + ' '
        date = pd.to_datetime(str(transaction_date)).strftime('%d.%m') + ' '#str(transaction_date[-2:]).zfill(2) + '.' + str(transaction_date[5:7]).zfill(2) + ' '
        hour = str(random.randint(7,22)).zfill(2)
        minute = str(random.randint(1,60)).zfill(2)
        time = 'kl. ' + hour + '.' + minute
        description = 'Varekjøp' + ' ' + store + city + 'Dato ' + date + time
    elif payment_category in ['Travel','Transport','Subscriptions', 'Culture&Activities']:
        store_list = store_list_by_category[payment_category]
        store = random.choice(store_list) + ' '
        number_in_description = str(random.randint(100,999))
        description = 'Visa ' + store + ' ' + number_in_description
    elif payment_category in ['Various Out','Various In']:
        payment_types = ['Mobiloverføring', 'Overføring Innland', 'Fast Oppdrag']
        name = fake.first_name() + ' ' + fake.last_name() + ' '
        number_in_description = str(random.randint(1000000000,9999999999)) + ' '
        description = random.choice(payment_types) + ' ' + number_in_description + name
    else:
        number_in_description = str(random.randint(100,999))
        description = random.choice(store_list_by_category[payment_category]) + ' ' + number_in_description
    return description

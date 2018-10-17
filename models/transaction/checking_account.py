'''
Creates transactions for a checking account (BRUKSKONTO)

Based on the transaction (trx_test_data_generator.py) script written by Severin Sjømark
'''
import datetime
import calendar
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


year = 2018

end_date = date.today()
start_date = end_date - timedelta(days=365)

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

# This Dictionary is used in get_transaction_description to generate the description based on the categories above
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
def get_random_date():
    days_since = random.randint(0,365)
    return date.today() - timedelta(days=days_since)


def get_transaction_description(payment_category, transaction_date):
    if payment_category in ['Utilities','Home','Groceries','Health','Restaurants&Nightlife','Shopping']:
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


def sample(length, lowerLimit, upperLimit):

    # Sampling without replacement method

    arr = []
    randPool = {}
    for _ in range(length):
        randInt = np.random.randint(lowerLimit, upperLimit)
        x = randPool.get(randInt, randInt)
        randPool[randInt] = randPool.get(lowerLimit, lowerLimit)
        lowerLimit += 1
        arr.append(x)
    return arr
    
class CheckingAccount:
    def __init__(self,accountNumber, accountOwnerSsn):
        self.accountNumber = accountNumber
        self.accountOwnerSsn = accountOwnerSsn
        self.transactions = self.generate_transactions()

    def generate_transactions(self):
        # Initialize empty dataframe
        SynthData = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
        i = self.accountNumber
        # Initialize account metadata
        # minimum trx on account, minimum deficit on account and maximum surplus
        min_nr_trx = np.random.choice(np.arange(1, 365))  # Minimum number of trx on acct, lower bond has to be 1, if 0 the code can crash
        min_acct_sum = np.random.choice(np.arange(-100000, 0))  # Minimum deficit end of year on acct
        max_acct_sum = np.random.choice(np.arange(0, 100000))  # Maximum surplus end of year on acct
        count = 0  # Initialize trx counter for cust

        # While acct criteria are not fulfilled: sample categories and generate trx
        while ((count < min_nr_trx) or SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) < min_acct_sum or
               SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) > max_acct_sum):
            cat = np.random.choice(np.arange(1, nr_cat + 1), p=cat_prob)  # Sample category
            done = np.zeros(16)  # Register if category has been sampled before on acct

            # While category has been sampled and acct critera not fulfilled: sample new category
            while done[cat - 1] == 1 or (SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) < min_acct_sum and
                                         categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0] == 'Out') or (
                    SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) > max_acct_sum and
                    categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0] == 'In'):
                cat = np.random.choice(np.arange(1, nr_cat + 1), p=cat_prob)

            if categories.loc[categories['CategoryLabel'] == cat, 'RegularInd'].iloc[0] > 0:  # Recurrent Category
                # Initialize temporary dataframe
                tmp_df = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])

                # Sample recurrent trx data
                mean = categories.loc[categories['CategoryLabel'] == cat, 'Mean'].iloc[0]
                std = mean / 4
                amt = math.ceil(np.random.normal(mean, std) / 100) * 100  # round up to nearest 100
                innOut = categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0]
                if innOut == 'Out':
                    amt = -amt
                freq = np.random.choice(np.arange(1, nr_freq + 1), p=[0.75, 0.15, 0.1])

                start = get_random_date()
                day = start.day
                start_month = start.month
                year = start.year

                if freq == 3:
                    end = start
                elif freq == 2:
                    end_month = 12
                    (first_weekday, days_in_month) = calendar.monthrange(year, end_month)
                    end = date(year, end_month, days_in_month)
                elif freq == 1:
                    end = date(year, 12, day)
                date_ = date(year, start_month, day)

                # Generate recurrent trx series
                while date_ < end:
                    tmp_df = pd.concat([tmp_df, pd.DataFrame(
                        [[i, date_, categories.loc[categories['CategoryLabel'] == cat, 'CategoryName'].iloc[0], amt]],
                        columns=['AccountID', 'Date', 'Category', 'Amount'])])
                    date_ = custom_delta(date_, freq, date_.month, end)
                # Update counter
                count = count + len(tmp_df.index)
                if cat == 12:  # Salary
                    done[cat - 1] = 1

            elif categories.loc[categories['CategoryLabel'] == cat, 'RegularInd'].iloc[
                0] == 2:  # If Category is both recurrent and non-recurrent
                # Initialize temporary dataframe
                tmp_df = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])

                # Sample trx data
                mean = categories.loc[categories['CategoryLabel'] == cat, 'Mean'].iloc[0]
                std = mean / 4
                max_trx_cat = categories.loc[categories['CategoryLabel'] == cat, 'MaxTrans'].iloc[0]
                nr_trx_cat = random.randint(5, max_trx_cat)
                amt = np.round(np.random.normal(mean, std, size=nr_trx_cat))
                innOut = categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0]
                if innOut == 'Out':
                    amt = [-i for i in amt]
                dates = np.random.choice(year_range, nr_trx_cat, replace=True)

                # Generate trx data
                for j, date_ in enumerate(dates):
                    tmp_df = pd.concat([tmp_df, pd.DataFrame(
                        [[i, date_, categories.loc[categories['CategoryLabel'] == cat, 'CategoryName'].iloc[0], amt[j]]],
                        columns=['AccountID', 'Date', 'Category', 'Amount'])])
                    count = count + 1
                done[cat - 1] = 1
            else:  # Non-recurrent Category
                # Initialize temporary dataframe
                tmp_df = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])

                # Sample trx data
                mean = categories.loc[categories['CategoryLabel'] == cat, 'Mean'].iloc[0]
                std = mean / 4
                max_trx_cat = categories.loc[categories['CategoryLabel'] == cat, 'MaxTrans'].iloc[0]
                nr_trx_cat = random.randint(5, max_trx_cat)
                amt = np.round(np.random.normal(mean, std, size=nr_trx_cat))
                innOut = categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0]
                if innOut == 'Out':
                    amt = [-i for i in amt]
                dates = np.random.choice(year_range, nr_trx_cat, replace=True)

                # Generate trx data
                for j, date_ in enumerate(dates):
                    tmp_df = pd.concat([tmp_df, pd.DataFrame(
                        [[i, date_, categories.loc[categories['CategoryLabel'] == cat, 'CategoryName'].iloc[0], amt[j]]],
                        columns=['AccountID', 'Date', 'Category', 'Amount'])])
                    count = count + 1
                done[cat - 1] = 1
            # Add temporary dataframe to full dataframe
            SynthData = pd.concat([SynthData, tmp_df])

        SynthData['description'] = SynthData.apply(lambda row: get_transaction_description(row['Category'],row['Date']), axis=1) # FIXME: this line crashes when running many times

        # Reformat date column
        SynthData['Date'] = pd.to_datetime(SynthData['Date'], dayfirst=True, format='%Y-%m-%d')
        SynthData = SynthData.sort_values(by=['Date'])
        
        # Generate random trx ID
        upperLimit=9999999
        lowerLimit=1000000
        TRX_ID = sample(len(SynthData.index),lowerLimit, upperLimit)
        TRX_ID = np.sort(TRX_ID)
        SynthData['transactionId'] = TRX_ID
        assert len(TRX_ID)==len(set(TRX_ID)), "Collision in transaction IDs"

        # Sort by accountId and date
        SynthData = SynthData.sort_values(by=['AccountID', 'Date'])
        SynthData = SynthData[['transactionId', 'AccountID', 'Date', 'Category', 'Amount', 'description']]

        # Adding missing fields
        SynthData['details'] = SynthData.apply(lambda row:{ 'textCode' : '0023' },axis=1)
        SynthData['textlines'] = SynthData.apply(lambda row:{ 'Item' : row['description'].split()[0] },axis=1) #Probability not the best way to do it!!
        SynthData['valueDate'] = SynthData['Date']
        SynthData['bookingDate'] = SynthData['Date']
        SynthData['externalReference'] = np.random.randint(100000, 9999999, SynthData.shape[0])

        #Add SSN for grouping
        SynthData['ssn'] = self.accountOwnerSsn

        # Rename the columns
        SynthData.rename(columns={'Date':'transactionDate','AccountID':'accountNumber','Amount':'amount',}, inplace=True)

        # Dropping the Category column
        SynthData = SynthData.drop(columns=['Category'])

        # Return
        return json.loads(SynthData.to_json(orient='records',date_format='iso', force_ascii=False).replace('T00:00:00.000Z',''))



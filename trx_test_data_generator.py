# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:15:25 2018

@author: ab22764, Severin Sjømark (Deepinsight)

A toy script to generate trx data.
Generates:
    - Fictional Trx ID
    - Fictional Acct ID
    - Random Category
    - Random Amount
    - Random Date in year
Some Categories are recurrent, i.e. occur frequently with the same amount, and on the same day of the month.

THe process for generation is a random sampling process.
We first randomly sample Nr of accounts, minimum trx on account, minimum deficit on account and maximum surplus
For each account we then sample a new category, and generate trx within this category, given mean amount within category,
max nr of trx within category, whether the category can be recurrent etc.

Fictional Trx ID is generated to be increasing with time.

Write to file; ordered by AcctID and date.

Proposed further work:
    - Category metadata for Customer segments (i.e. more specification)
    - More frequencies (weekly, bi-weekly,...)
    - Add dimension of Recipient/Merchant within each category (manual job)

"""

import csv
import datetime
import math
import random
from datetime import timedelta, date

# Import packages
import numpy as np
import pandas as pd

# Initialize account metadata
# Nr of accounts, minimum trx on account, minimum deficit on account and maximum surplus
nr_cust = 10  # Number of Customers to generate trx for
min_nr_trx = np.random.choice(365, nr_cust, replace=True)  # Minimum number of trx on acct
min_acct_sum = np.random.choice(np.arange(-100000, 0), nr_cust, replace=True)  # Minimum deficit end of year on acct
max_acct_sum = np.random.choice(np.arange(0, 100000), nr_cust, replace=True)  # Maximum surplus end of year on acct
nr_cat = 16  # Number of predefined categories
nr_freq = 3  # Number of predefined frequencies

# Generate a Date range for year
year = 2017
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


# Reads customerId (AccountID) from file creqted by create_people.py
def read_customers_from_csv(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='\'')
        customer_id = []
        for row in reader:
            customer_id.append(row[0]);
    return customer_id



# Initialize empty dataframe
SynthData = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
for i in range(nr_cust):  # Iterate over the customer
    nr_trx_i = min_nr_trx[i]  # Get minimum nr of trx for cust
    max_acct_sum_i = max_acct_sum[i]  # Get max acct surplus for cust
    min_acct_sum_i = min_acct_sum[i]  # Get min acct deficit for cust
    count = 0  # Initialize trx counter for cust

    # While acct criteria are not fulfilled: sample categories and generate trx
    while ((count < nr_trx_i) or SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) < min_acct_sum_i or
           SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) > max_acct_sum_i):
        cat = np.random.choice(np.arange(1, nr_cat + 1), p=cat_prob)  # Sample category
        done = np.zeros(16)  # Register if category has been sampled before on acct

        # While category has been sampled and acct critera not fulfilled: sample new category
        while done[cat - 1] == 1 or (SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) < min_acct_sum_i and
                                     categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0] == 'Out') or (
                SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) > max_acct_sum_i and
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
            # Find random date
            # TODO: Because of the "day + 1" below, this sometimes/often fails.
            random_date = get_random_date(year)
            day = random_date.day if random_date.day < 31 else 1 # HACK: Fix the todo above
            start_month = random_date.month
            start = date(year, start_month, day)
            if freq == 3:
                end = start
            elif freq == 2:
                end_month = start_month + 3 * int((12 - start_month) / 3)
                end = date(year, end_month, day + 1)
            elif freq == 1:
                end = date(year, 12, day + 1)
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
    print(i)  # Print current Acct


# Print number of trx and total sum on account
SynthData.groupby(['AccountID'])['Amount'].agg(['count', 'sum'])

# Reformat date column
SynthData['Date'] = pd.to_datetime(SynthData['Date'], dayfirst=True, format='%Y-%m-%d')
SynthData = SynthData.sort_values(by=['Date'])

# Generate random trx ID
TRX_ID = np.random.choice(np.arange(1000000, 9999999), len(SynthData.index), replace=False)
TRX_ID = np.sort(TRX_ID)
SynthData['TrxID'] = TRX_ID

# Generate "random" account ID
SynthData['AccountID'] = 100000 + 3 * SynthData['AccountID']

# Sort by accountId and date
SynthData = SynthData.sort_values(by=['AccountID', 'Date'])
SynthData = SynthData[['TrxID', 'AccountID', 'Date', 'Category', 'Amount']]

# Write to file
SynthData.to_csv('test.csv', sep=';', index=False)

#  -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:15:25 2018

@author: ab22764 (Severin Sjømark)
"""

import datetime
import random
from datetime import timedelta, date

import numpy as np
import pandas as pd

# Initialize account metadata
# Nr of accounts, minimum trx on account, minimum deficit on account and maximum surplus
nr_cust = 3
min_nr_trx = np.random.choice(365, nr_cust, replace=True)
min_acct_sum = np.random.choice(np.arange(-10000, 0), nr_cust, replace=True)
max_acct_sum = np.random.choice(np.arange(0, 75000), nr_cust, replace=True)
nr_cat = 16
nr_freq = 3

# Date range
year = 2017
start_date = date(year, 1, 1)
end_date = date(year, 12, 31)
year_range = []
for n in range(365):
    d = start_date + timedelta(n)
    year_range.append(d.strftime("%Y-%m-%d"))

# Categories with some mean amounts, recurrency indicator etc.
# Can be expanded to include customer segments, with different mean amounts
categories = pd.DataFrame([['Loans&Rent', 1, 1, 'Out', 12000, 0],
                           ['Utilities', 2, 1, 'Out', 2000, 0],
                           ['Home', 3, 0, 'Out', 1500, 30],
                           ['Transport', 4, 2, 'Out', 1000, 10],
                           ['Groceries', 5, 0, 'Out', 1500, 150],
                           ['Health', 6, 0, 'Out', 500, 10],
                           ['Culture&Activities', 7, 2, 'Out', 200, 40],
                           ['Travel', 8, 0, 'Out', 5000, 20],
                           ['Restaurants&Nightlife', 9, 0, 'Out', 500, 50],
                           ['Shopping', 10, 0, 'Out', 1000, 30],
                           ['Savings', 11, 1, 'Out', 5000, 0],
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
cat_prob = [0.1,  # Loans&Rent
            0.075,  # Utilities
            0.05,  # Home
            0.05,  # Transport
            0.115,  # Groceries
            0.02,  # Health
            0.065,  # Culture&Activities
            0.04,  # Travel
            0.065,  # Restaurants&Nightlife
            0.055,  # Shopping
            0.05,  # Savings
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


def get_random_date(year):
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y')
    # Leap year? Try again.
    except ValueError:
        get_random_date(random_year)



SynthData = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
for i in range(nr_cust):
    nr_trx_i = min_nr_trx[i]
    max_acct_sum_i = max_acct_sum[i]
    min_acct_sum_i = min_acct_sum[i]
    count = 0
    while ((count < nr_trx_i) or
           SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) < min_acct_sum_i or
           SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) > max_acct_sum_i):
        cat = np.random.choice(np.arange(1, nr_cat + 1), p=cat_prob)
        done = np.zeros(16)
        while done[cat - 1] == 1 or (SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) < min_acct_sum_i and
                                     categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0] == 'Out') or (
                SynthData.loc[SynthData['AccountID'] == i, 'Amount'].agg(sum) > max_acct_sum_i and
                categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0] == 'In'):
            cat = np.random.choice(np.arange(1, nr_cat + 1), p=cat_prob)
        if categories.loc[categories['CategoryLabel'] == cat, 'RegularInd'].iloc[0] > 0:
            tmp_df = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
            mean = categories.loc[categories['CategoryLabel'] == cat, 'Mean'].iloc[0]
            std = mean / 4
            # amt = math.ceil(np.random.normal(mean, std) / 100) * 100  # round up to nearest 100
            amt = round(np.random.normal(mean, std), 2)
            innOut = categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0]
            if innOut == 'Out':
                amt = -amt
            freq = np.random.choice(np.arange(1, nr_freq + 1), p=[0.75, 0.15, 0.1])
            # day = random.randint(1, 28)
            # start_month = random.randint(1, 12)
            random_date = get_random_date(year)
            day = random_date.day
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
            while date_ < end:
                tmp_df = pd.concat([tmp_df, pd.DataFrame(
                    [[i, date_, categories.loc[categories['CategoryLabel'] == cat, 'CategoryName'].iloc[0], amt]],
                    columns=['AccountID', 'Date', 'Category', 'Amount'])])
                date_ = custom_delta(date_, freq, date_.month, end)
            count = count + len(tmp_df.index)
            if cat == 12:  # Salary
                done[cat - 1] = 1
        elif categories.loc[categories['CategoryLabel'] == cat, 'RegularInd'].iloc[0] == 2:
            tmp_df = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
            mean = categories.loc[categories['CategoryLabel'] == cat, 'Mean'].iloc[0]
            std = mean / 4
            max_trx_cat = categories.loc[categories['CategoryLabel'] == cat, 'MaxTrans'].iloc[0]
            nr_trx_cat = random.randint(5, max_trx_cat)
            amt = np.round(np.random.normal(mean, std, size=nr_trx_cat))
            innOut = categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0]
            if innOut == 'Out':
                amt = [-i for i in amt]
            dates = np.random.choice(year_range, nr_trx_cat, replace=True)
            for j, date_ in enumerate(dates):
                tmp_df = pd.concat([tmp_df, pd.DataFrame(
                    [[i, date_, categories.loc[categories['CategoryLabel'] == cat, 'CategoryName'].iloc[0], amt[j]]],
                    columns=['AccountID', 'Date', 'Category', 'Amount'])])
                count = count + 1
            done[cat - 1] = 1
        else:
            tmp_df = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
            mean = categories.loc[categories['CategoryLabel'] == cat, 'Mean'].iloc[0]
            std = mean / 4
            max_trx_cat = categories.loc[categories['CategoryLabel'] == cat, 'MaxTrans'].iloc[0]
            nr_trx_cat = random.randint(5, max_trx_cat)
            amt = np.round(np.random.normal(mean, std, size=nr_trx_cat))
            innOut = categories.loc[categories['CategoryLabel'] == cat, 'InOut'].iloc[0]
            if innOut == 'Out':
                amt = [-i for i in amt]
            dates = np.random.choice(year_range, nr_trx_cat, replace=True)
            for j, date_ in enumerate(dates):
                tmp_df = pd.concat([tmp_df, pd.DataFrame(
                    [[i, date_, categories.loc[categories['CategoryLabel'] == cat, 'CategoryName'].iloc[0], amt[j]]],
                    columns=['AccountID', 'Date', 'Category', 'Amount'])])
                count = count + 1
            done[cat - 1] = 1
        SynthData = pd.concat([SynthData, tmp_df])
    print(i)

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

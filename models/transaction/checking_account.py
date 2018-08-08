'''
Creates transactions for a checking account (BRUKSKONTO)

Based on the transaction (trx_test_data_generator.py) script written by Severin Sjømark
'''
from .elements.categories import *

class CheckingAccount:
    def __init__(self,accountNumber):
        self.accountNumber = accountNumber
        self.transactions = self.generate_transactions()

    def generate_transactions(self):
        # Initialize empty dataframe
        SynthData = pd.DataFrame(columns=['AccountID', 'Date', 'Category', 'Amount'])
        i = self.accountNumber
        # Initialize account metadata
        # minimum trx on account, minimum deficit on account and maximum surplus
        min_nr_trx = np.random.choice(np.arange(1, 365))  # Minimum number of trx on acct
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
                # Find random date
                # TODO: Because of the "day + 1" below, this sometimes/often fails.
                random_date = get_random_date(year)
                day = random_date.day if random_date.day < 28 else 1 # HACK: Fix the todo above
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

        SynthData['description'] = SynthData.apply(lambda row: get_transaction_description(row['Category'],row['Date']), axis=1) # FIXME: this line crashes when running many times

        # Print number of trx and total sum on account
        #print(SynthData.groupby(['AccountID'])['Amount'].agg(['count', 'sum']))

        # Reformat date column
        SynthData['Date'] = pd.to_datetime(SynthData['Date'], dayfirst=True, format='%Y-%m-%d')
        SynthData = SynthData.sort_values(by=['Date'])

        # Generate random trx ID
        TRX_ID = np.random.choice(np.arange(1000000, 9999999), len(SynthData.index), replace=False)
        TRX_ID = np.sort(TRX_ID)
        SynthData['transactionId'] = TRX_ID

        # Sort by accountId and date
        SynthData = SynthData.sort_values(by=['AccountID', 'Date'])
        SynthData = SynthData[['transactionId', 'AccountID', 'Date', 'Category', 'Amount', 'description']]

        # Adding missing fields
        SynthData['details'] = SynthData.apply(lambda row:{ 'textCode' : '0023' },axis=1)
        SynthData['textlines'] = SynthData.apply(lambda row:{ 'Item' : row['description'].split()[0] },axis=1) #Probability not the best way to do it!!
        SynthData['valueDate'] = SynthData['Date']
        SynthData['bookingDate'] = SynthData['Date']
        SynthData['externalReference'] = np.random.randint(100000, 9999999, SynthData.shape[0])

        # Rename the columns
        SynthData.rename(columns={'Date':'transactionDate','AccountID':'accountNumber','Amount':'amount',}, inplace=True)

        # Return
        return json.loads(SynthData.to_json(orient='records',date_format='iso', force_ascii=False).replace('T00:00:00.000Z',''))

# acc = CheckingAccount(1000)
# import pprint
# pprint.pprint(acc.transactions)

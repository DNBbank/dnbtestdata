# Test data for DNB

Code to generate synthetic data for DNB Developer APIs: https://dnbdeveloper.restlet.io

# DNB data

Branches, ATMs, etc are avilable in the links below. Please note that the .csv suffix is incorrect: The files are not proper comma-separated files.

* https://www.dnb.no/portalfront/datafiles/offices/branch.csv
* https://www.dnb.no/portalfront/datafiles/offices/postal.csv
* https://www.dnb.no/portalfront/datafiles/offices/atm.csv
* https://www.dnb.no/portalfront/datafiles/offices/realestate.csv

# People

- Fake people with valid SSNs and realistic-ish data
- Real companies (from brreg.no)
- Bank accounts
    - One or more per person: https://github.com/joke2k/faker/pull/726
- Debit cards
    - One or more per person
- Credit cards
    - Most people (95 %?) should have at least one.

# Transactions

The following are must-have patterns. Some are broad in terms of the data range, while some are a bit more specific.

As I said yesterday I recommend patterns in terms of bigger categories, and not MCCs or similar. I also highly recommend drawing amounts from normal distributions given a good guess on mean, and day of month of recurrent payments etc. from random distributions. When it comes to frequencies, monthly frequency is most represented, but you could throw in some quarterly or yearly frequencies as well. The next installment of a recurrent payment must respect the frequency, so I suggest fixing the day of month from one installment to the next, taking special care of the last day of the month (28 for February).

 
1. The average net salary in Norway is 30.000 NOK/month. Basically the entire population has an “Income”-post (salary, student loan, pension). The distribution has a large variance, but is of course bounded below at 0. The most represented frequency is monthly, and I think it would be wise to simplify so all income is monthly.
1. Almost everyone rents or has a mortgage. I would guess an average of 10.000 NOK/month on “Loans & Rent” with a large variance bounded below at 0. Monthly frequency.
1. Let’s say that 50% has recurrent “Transport” expenses, in the range 500-1000 NOK fixed each month. Another 30% has variable transport expenses (fuel, car maintenance, various irregular public transport).
1. Most people pay “Insurance”, in the range 150-2500/month. Most pay this monthly, but some pay this quarterly or yearly.
1. Most people have “Various” expenses and incomes, which could be e.g. Vipps, with an average amont of 45NOK/payment, with a high variance
1. 80% of “Restaurants, Bars and Pubs” occur on Thursday, Friday and Saturday.
1. 80% of users buy “Groceries” 3 times a week. The variance in amount is overall large.
1. 70% of users have recurrent “Utilities” payments. There can be several individual plans (one for power, one for internet, one for phone etc). Monthly and quarterly frequencies.
1. 70% of users have “Savings” payments to a savings account. This can be both regular and irregular, with a large variance in savings amount.
1. Users spend more in physical stores than on internet shopping.
1. 10% of people “Travel” regularly (i.e. many times a year). 90% of people travel around the holidays (christmas, easter, summer).

## The suggested categories (if you are to use these) are:

1. Loans&Rent
2. Utilities
3. Home
4. Transport
5. Groceries
6. Health
7. Culture&Activities
8. Travel
9. Restaurants&Nightlife
10. Shopping
11. Savings
12. Income
13. Various in
14. Various out
15. Subscriptions
16. Insurance

Categories 1,2,4,5,8,9,11,12,13,14 and 16 should have been mentioned above. The rest can have various amount of instances per account, with highly variable amounts. If it is possible in the seeding process I also recommend implementing some limits to the overall surplus or deficit on an account, for realism. If it is possible, the likelihood of the categories being represented on a current account is also variable, i.e. 1,2,5 and 12 are highly likely (sort of must-haves), while the rest are less likely. “

 
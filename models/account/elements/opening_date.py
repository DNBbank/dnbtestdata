import random
from datetime import date


def get_opening_date(account):
    birth_year = account['accountOwnerPublicId'][4:6]
    this_year = str(date.today().year)[2:4]
    if int(birth_year) > int(this_year):
        full_birth_year = '19' + birth_year
    else:
        full_birth_year = '20' + birth_year.zfill(2)

    this_year_long = int('20' + str(this_year))
    birth_year_long = int(full_birth_year)
    random_year = random.randint(birth_year_long, this_year_long)
    random_month = random.randrange(13)
    random_day = random.randrange(29)
    opening_date = str(random_year) + '-' + str(random_month).zfill(2) + '-' + str(random_day).zfill(2)
    return opening_date

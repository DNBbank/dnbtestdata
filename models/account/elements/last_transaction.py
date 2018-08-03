from datetime import timedelta, date


def get_last_transaction():
    # currently just returns yesterday's date
    # after transactions has been implemented, it should fetch from there.
    yesterday = date.today() - timedelta(1)
    return str(yesterday.year) + '-' + str(yesterday.month) + '-' + str(yesterday.day)

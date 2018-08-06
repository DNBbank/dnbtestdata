import datetime
import random


class DateUtil:
    @classmethod
    def date_string(cls, date):
        return str(date.day).zfill(2) + '-' + str(date.month).zfill(2) + '-' + str(date.year)

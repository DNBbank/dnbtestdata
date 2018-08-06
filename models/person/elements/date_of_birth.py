import datetime
import random


class DateOfBirth:
    @classmethod
    def generate_random(cls, max_age):
        this_year = datetime.datetime.now().year
        random_year = random.randrange(this_year - max_age, this_year - 14)
        random_date = datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random_year), '%j %Y')
        year, month, day = [random_date.year, random_date.month, random_date.day]
        return DateOfBirth(day, month, year)

    @classmethod
    def from_string(cls, date_string):
        return DateOfBirth(int(date_string[8:11]), int(date_string[5:7]), int(date_string[0:4]))

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def calculate_age(self):
        today = datetime.date.today()
        return today.year - self.year - ((today.month, today.day) < (self.month, self.day))

    def to_string(self):
        return str(self.year) + '-' + str(self.month).zfill(2) + '-' + str(self.day).zfill(2)

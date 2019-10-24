import random

from faker import Faker

fake = Faker('no_NO')

class Ssn:
    @classmethod
    def generate_random_ssn(cls, gender, date_of_birth):
        return fake.ssn(date_of_birth.to_string().replace('-', ''), gender.value[0])

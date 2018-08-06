from faker import Faker


class Address:
    @classmethod
    def generate_norwegian_random(cls):
        return _NorwegianAddress.generate_random()

    def __init__(self, street, postal_code, city, country):
        self.street = street
        self.postal_code = postal_code
        self.city = city
        self.country = country


class _NorwegianAddress:
    fake = Faker('no_NO')

    @classmethod
    def generate_random(cls):
        street = cls.fake.street_name() + ' ' + cls.fake.building_number()
        postal_code = cls.fake.postcode()
        city = cls.fake.city()
        country = 'NO'

        return Address(street, postal_code, city, country)

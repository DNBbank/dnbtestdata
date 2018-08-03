import random

from .elements.address import Address
from .elements.date_of_birth import DateOfBirth
from .elements.gender import Gender
from .elements.name import Name
from .elements.ssn import Ssn
from faker import Faker


class Person:
    @classmethod
    def generate_random(cls):
        fake = Faker('no_NO')

        gender = Gender.generate_random()
        name = Name.generate_norwegian_name(gender)
        date_of_birth = DateOfBirth.generate_random(100)
        ssn = Ssn.generate_random_ssn(gender, date_of_birth)
        nationality = "Norwegian"
        address = Address.generate_norwegian_random()
        phone_number = fake.phone_number()
        email = random.choice(
            (name.first_name,
             name.last_name + str(date_of_birth.year),
             name.first_name + name.last_name)
        ).lower() + '@example.com'

        id_type = random.choice(('passport', 'driverslicense', 'nationalidcard'))

        return Person(ssn,
                      name.first_name,
                      name.last_name,
                      date_of_birth,
                      gender,
                      nationality,
                      address,
                      phone_number,
                      email,
                      id_type
                      )

    def __init__(self, ssn, first_name, last_name, date_of_birth, gender,
                 nationality, address, phone_number, email, id_type):
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.nationality = nationality
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.id_type = id_type

    def to_json(self):
        return {
            'ssn': self.ssn,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'dateOfBirth': self.date_of_birth.to_string(),
            'gender': self.gender.value,
            'nationality': self.nationality,
            'address': {
                'street': self.address.street,
                'postalCode': self.address.postal_code,
                'city': self.address.city,
                'country': self.address.country,
            },
            'phoneNumber': self.phone_number,
            'email': self.email,
            'idType': self.id_type,
        }

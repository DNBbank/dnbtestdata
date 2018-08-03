from faker import Faker


class Name:
    @classmethod
    def generate_norwegian_name(cls, gender):
        return Name(_NorwegianName.generate_random_first_name(gender),
                    _NorwegianName.generate_random_last_name())

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class _NorwegianName:
    fake = Faker('no_NO')

    @classmethod
    def generate_random_first_name(cls, gender):
        if gender.MALE:
            return cls.fake.first_name_male()
        elif gender.FEMALE:
            return cls.fake.first_name_female()
        else:
            raise Exception()

    @classmethod
    def generate_random_last_name(cls):
        return cls.fake.last_name()

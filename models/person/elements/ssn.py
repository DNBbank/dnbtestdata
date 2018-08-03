import random


class Ssn:
    @classmethod
    def generate_random_ssn(cls, gender, date_of_birth):
        # TODO: SSN: Faking it until Faker supports Norwegian SSNs, and it is plossible to:
        # ssn = fake.ssn('19991231',gender[:1])
        # https://github.com/joke2k/faker/pull/716
        # https://github.com/joke2k/faker/issues/714
        gender_indicator = cls._generate_random_gender_indicator(gender)
        pnr = cls._generate_pnr(gender_indicator)
        ssn = str(date_of_birth.day).zfill(2) \
              + str(date_of_birth.month).zfill(2) \
              + str(date_of_birth.year)[-2:] \
              + pnr
        return ssn

    @staticmethod
    def _generate_pnr(gender_indicator):
        return str(random.randint(0, 99)).zfill(2) \
               + gender_indicator \
               + str(random.randint(0, 99)).zfill(2)

    @staticmethod
    def _generate_random_gender_indicator(gender):
        if gender.MALE:
            return random.choice(('1', '3', '5', '7', '9'))
        elif gender.FEMALE:
            return random.choice(('0', '2', '4', '6', '8'))

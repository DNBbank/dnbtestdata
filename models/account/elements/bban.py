import operator
import random


class Bban:
    # See: https://no.wikipedia.org/wiki/Kontonummer
    _weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)

    @classmethod
    def generate_random_bban(cls):
        while True:
            # every digit starts with 120 and then 10 random digits
            digits = [random.randint(0, 9) for i in range(7)]

            # Modulo 11
            r = sum(map(operator.mul, digits, cls._weights)) % 11

            if r == 0:
                c = 0
            elif r == 1:
                # The control digit 10 is not allowed. We need to create a new
                # random account number
                continue
            else:
                c = 11 - r

            digits.insert(0, 120)
            digits.append(c)
            return ''.join(str(x) for x in digits)
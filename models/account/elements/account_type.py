# Guessed probability of having an specific account:
account_types_with_probability = {
    'BRUKSKONTO': 100,
    'SPAREKONTO': 65,
    'LÅN': 55,
    'BSU': 50,                  # should also be under the age of 34
    'BRUKSKONTO TILLEGG': 25,
    'AKSJESPAREKONTO': 25,
    'STUDENT BRUKSKONTO': 30,   # should be between 19 & 25
    'SUPERSPAR': 20,
}

interest_rates = {
    'BRUKSKONTO': 0.1,
    'SPAREKONTO': 0.5,
    'RAMMELÅN': 2.5,
    'BOLIGLÅN': 2.65,       # varies a lot
    'BSU': 3.2,
    'BRUKSKONTO TILLEGG': 0.1,
    'AKSJESPAREKONTO': 0,
    'STUDENT BRUKSKONTO': 0.1,   # should be between 19 & 25
    'SUPERSPAR': 1.2,
}
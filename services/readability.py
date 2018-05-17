from random import random


def round_number_intelligently(number):
    """This will round a number based on its closeness to the next number. So (1.4) has a 40% chance to be rounded to a (2).
    It returns an integer."""
    new_amount = int(number) + (random() < number - int(number))
    return new_amount

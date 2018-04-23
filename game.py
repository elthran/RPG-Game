# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
# Author: Elthran B, Jimmy Zhang                                              #
# Email : jimmy.gnahz@gmail.com                                               #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

"""Objects used in the database and the game.

Suggestion: change name to game_objects.py
"""

from random import random


class Game(object):
    def __init__(self, hero=None):
        self.hero = hero
        self.has_enemy = False
        self.global_chat_user_list = {}
        self.global_chat = []  # I am not sure if this should goin database? Just very temporary chat log that all users can see

    def set_hero(self, hero):
        self.hero = hero


class Notification(object):
    def send_notification(title="Attention!", content="Something interesting has happened.", url="/home"):
        return None

def round_number_intelligently(number):
    """This will round a number based on its closeness to the next number. So (1.4) has a 40% chance to be rounded to a (2).
    It returns an integer."""
    new_amount = int(number) + (random() < number - int(number))
    return new_amount


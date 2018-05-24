# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
#  Author: Elthran B, Jimmy Zhang                                             #
#  Email : jimmy.gnahz@gmail.com                                              #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

from hero import Hero # THIS MIGHT BE USED. CHECK THE GENERATE_MONSTER FUNCTION
from random import choice

def generate_monster(hero, monsters):
    #monsters = database.get_all_monsters(hero)    THIS SHOULD RUN AND "MONSTERS" SHOULDN'T BE PASSED IN AS A PARAMETER
    return choice(monsters)


class NPC(object):
    def __init__(self, id_, name, race, age):
        self.id = id_
        self.name = name
        self.race = race
        self.age = age

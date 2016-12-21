#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

""" this is basically the init file that sets up some things"""


import math
from flask import request
from items import *
from bestiary import *
from abilities import *

# function used in '/level_up'
def convert_input(x):
    try:
        x = int(x)
    except:
        x = 0
    return x

class Game(object):
    def __init__(self, hero):
        self.hero = hero
        self.has_enemy = False

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.has_enemy = True

class Hero(object):
    def __init__(self, user_id=0):
        """Make a new Hero object.

        NOTE: user_id of zero is nobody ever. The minimum user_id is 1. :)
        """
        self.user_id = user_id
        self.character_name = "Admin"
        self.age = 7
        self.character_class = "None"
        self.specialization = "None"
        self.house = "None"
        self.current_exp = 0
        self.max_exp = 10
        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        self.basic_ability_points = 0
        self.class_ability_points = 0
        self.specialization_ability_points = 0
        self.pantheonic_ability_points = 0

        self.attribute_points = 0
        self.strength = 1
        self.resilience = 1
        self.vitality = 1
        self.fortitude = 1
        self.reflexes = 1
        self.agility = 1
        self.perception = 1
        self.wisdom = 1
        self.divinity = 1
        self.charisma = 1
        self.survivalism = 1
        self.fortuity = 1

        self.current_sanctity = 0
        self.current_health = 0
        self.current_endurance = 0
        self.current_carrying_capacity = 0

        self.equipped_items = []
        self.inventory = []
        self.abilities = []
        self.chest_equipped = []

        self.errands = []
        self.current_quests = []
        self.completed_quests = []
        self.completed_achievements = []
        self.kill_quests = {}
        self.bestiary = []

        self.known_locations = []
        self.current_world = None
        self.current_city = None

        self.wolf_kills = 0

    # Sets damage
    def update_secondary_attributes(self):
        self.min_damage = self.strength
        self.max_damage = self.strength + self.agility
        self.attack_speed = 2 * self.agility + self.reflexes
        self.attack_accuracy = 3 * self.agility         # A percentage
        self.first_strike = 3 * self.agility + self.reflexes         # A percentage
        self.critical_hit = 5 * self.agility         # A percentage
        self.defence_modifier = 3 * self.resilience         # A percentage
        self.evade_chance = 4 * self.reflexes + self.agility         # A percentage
        self.parry_chance = 3 * self.reflexes + 2 * self.agility + self.perception         # A percentage
        self.block_chance = 2 * self.reflexes + self.agility        # A percentage
        self.block_reduction = self.strength # + shield type/size         # A percentage
        self.poisin_resistance = 5 * self.resilience         # A percentage
        self.spiritual_resistance = 2 * self.resilience + 2 * self.divinity         # A percentage
        self.stealth_skill = self.agility + self.reflexes + self.perception        # A percentage
        self.faith = self.divinity
        self.max_health = 5 * self.vitality + self.resilience
        self.max_sanctity = 5 * self.divinity
        self.max_endurance = 5 * self.fortitude
        self.max_carrying_capacity = 3 * self.strength + 2 * self.fortitude
        self.barter = 5 * self.charisma
        self.oration = 4 * self.charisma + self.wisdom
        self.luck = 5 * self.fortuity                  # A percentage

        # Hidden attributes
        self.experience_gain_modifier = 1
        self.gold_gain_modifier = 1

        for ability in self.abilities:
            ability.update_stats()
        for item in self.equipped_items:
            item.update_stats()

        self.current_sanctity = self.max_sanctity - 70 # TEMP WHILE TESTING POTIONS
        self.current_health = self.max_health - 70 # TEMP WHILE TESTING POTIONS
        self.current_endurance = self.max_endurance
        self.current_carrying_capacity = self.max_carrying_capacity

    def refresh_character(self):
        # used to fully heal
        pass

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return False
        self.current_exp -= self.max_exp
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.age += 1
        self.update_secondary_attributes()
        return True

    def consume_item(self, item_name):
        for my_item in self.inventory:
            if my_item.name == item_name:
                my_item.apply_effect()
                self.inventory.remove(my_item)
                break

    def __str__(self):
        """Return python representation of Hero opject
        """
        # for e in dir(self):
            # print(e, self.e) #Where e is each element of self ... some kind of compile/execute ...?
        data = """Character belonging to user: '{}'.

The character has attributes: ...""".format(self.user_id)
        return data
        # return "\nName: %s" % (self.name)


# Temporary Function to create a random hero
def create_random_hero():
    myHero = Hero()
    myHero.strength = 50
    myHero.vitality = 50
    myHero.fortitude = 50
    myHero.gold = 5000
    myHero.update_secondary_attributes
    myHero.refresh_character
    return myHero
# End of temporary functions




# initialization
myHero = create_random_hero()
game = Game(myHero)
enemy = monster_generator(myHero.age)

# Super temporary while testing quests
myHero.inventory.append(Quest_Item("Wolf Pelt", myHero, 50))
myHero.inventory.append(Quest_Item("Spider Leg", myHero, 50))
myHero.inventory.append(Quest_Item("Copper Coin", myHero, 50))
for item in myHero.inventory:
    item.amount_owned = 5




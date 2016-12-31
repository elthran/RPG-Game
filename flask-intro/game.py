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
        self.archetype = "Woodsman"
        self.specialization = "Hunter"
        self.religion = "Dryarch"
        self.house = "None"
        self.current_exp = 0
        self.max_exp = 10
        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        self.ability_points = 5 #TEMP. Soon will use the 4 values below
        self.basic_ability_points = 0
        self.archetype_ability_points = 0
        self.specialization_ability_points = 0
        self.pantheonic_ability_points = 0

        self.attribute_points = 0
        self.primary_attributes = {"Strength": 1, "Resilience": 1, "Vitality": 1, "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1, "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1}
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
        self.max_health = 0
		
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
        self.min_damage = self.primary_attributes["Strength"]
        self.max_damage = self.primary_attributes["Strength"] + self.primary_attributes["Agility"]
        self.attack_speed = 2 * self.primary_attributes["Agility"] + self.primary_attributes["Reflexes"]
        self.attack_accuracy = 30 * self.primary_attributes["Agility"]         # A percentage
        self.first_strike = 3 * self.primary_attributes["Agility"] + self.primary_attributes["Reflexes"]        # A percentage
        self.critical_hit = 5 * self.primary_attributes["Agility"]         # A percentage
        self.defence_modifier = 3 * self.primary_attributes["Resilience"]         # A percentage
        self.evade_chance = 4 * self.reflexes + self.primary_attributes["Agility"]         # A percentage
        self.parry_chance = 3 * self.reflexes + 2 * self.primary_attributes["Agility"] + self.perception         # A percentage
        self.block_chance = 2 * self.reflexes + self.primary_attributes["Agility"]       # A percentage
        self.block_reduction = self.primary_attributes["Strength"] # + shield type/size         # A percentage
        self.poisin_resistance = 5 * self.primary_attributes["Resilience"]          # A percentage
        self.spiritual_resistance = 2 * self.primary_attributes["Resilience"]  + 2 * self.primary_attributes["Divinity"]         # A percentage
        self.stealth_skill = self.primary_attributes["Agility"] + self.primary_attributes["Reflexes"]  + self.primary_attributes["Perception"]         # A percentage
        self.faith = self.primary_attributes["Divinity"]

        self.max_sanctity = 5 * self.primary_attributes["Divinity"]
        self.max_endurance = 5 * self.primary_attributes["Fortitude"]
        self.max_carrying_capacity = 3 * self.primary_attributes["Strength"] + 2 * self.primary_attributes["Fortitude"]
        self.barter = 5 * self.primary_attributes["Charisma"]
        self.oration = 4 * self.primary_attributes["Charisma"] + self.primary_attributes["Wisdom"]
        self.luck = 5 * self.primary_attributes["Fortuity"]                 # A percentage

        previous_max_health = self.max_health
        self.max_health = 5 * self.primary_attributes["Vitality"] + self.primary_attributes["Resilience"]

        # Hidden attributes
        self.experience_gain_modifier = 1 # This is the percentage of exp you gain
        self.gold_gain_modifier = 1 # This is the percentage of gold you gain

        for ability in self.abilities:
            ability.update_stats()
        for item in self.equipped_items:
            item.update_stats()

        # When you update max_health, current health will also change by the same amount
        max_health_change = self.max_health - previous_max_health
        if max_health_change != 0: 
            self.current_health += max_health_change	
        if self.current_health < 0:
            self.current_health = 0	        
        

    def refresh_character(self):
        self.current_sanctity = self.max_sanctity
        self.current_health = self.max_health
        self.current_endurance = self.max_endurance
        self.current_carrying_capacity = self.max_carrying_capacity

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return False
        self.current_exp -= self.max_exp
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.age += 1
        self.ability_points += 2
        self.current_health = self.max_health
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
    myHero.name = "Unknown"
    myHero.gold = 5000
    myHero.update_secondary_attributes()
    myHero.refresh_character()
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




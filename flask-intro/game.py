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
from secondary_attributes import *

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
        self.name = "Admin"
        self.age = 7
        self.archetype = "Woodsman"
        self.specialization = "Hunter"
        self.religion = "Dryarch"
        self.house = "Unknown"
        self.current_exp = 0
        self.max_exp = 10
        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        self.ability_points = 3 #TEMP. Soon will use the 4 values below
        self.basic_ability_points = 0
        self.archetype_ability_points = 0
        self.specialization_ability_points = 0
        self.pantheonic_ability_points = 0

        self.attribute_points = 0
        self.primary_attributes = {"Strength": 1, "Resilience": 1, "Vitality": 1, "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1, "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1}
        self.current_sanctity = 0
        self.current_health = 0
        self.current_endurance = 0
        self.current_carrying_capacity = 0
        self.max_health = 0
		
        self.equipped_items = []
        self.inventory = []
        self.abilities = []
        self.chest_equipped = []

        self.current_quests = []
        self.quest_notification = None
        self.completed_achievements = []
        self.kill_quests = {}
        self.bestiary = []

        self.known_locations = []
        self.current_world = None
        self.current_city = None

        self.wolf_kills = 0
        self.update_secondary_attributes()

    # Sets damage
    def update_secondary_attributes(self):
        self.maximum_damage = update_maximum_damage(self)
        self.minimum_damage = update_minimum_damage(self)
        self.attack_speed = update_attack_speed(self)
        self.attack_accuracy = update_attack_accuracy(self)
        self.first_strike = update_first_strike_chance(self)
        self.critical_hit_chance = update_critical_hit_chance(self)
        self.critical_hit_modifier = update_critical_hit_modifier(self)
        self.defence_modifier = update_defence_modifier(self)
        self.evade_chance = update_evade_chance(self)
        self.parry_chance = update_parry_chance(self)
        self.riposte_chance = update_riposte_chance(self)
        self.block_chance = update_block_chance(self)
        self.block_reduction = update_block_reduction(self)
        self.stealth_skill = update_stealth_skill(self)
        self.faith = update_faith(self)
        self.max_sanctity = update_maximum_sanctity(self)
        self.max_endurance = update_maximum_endurance(self)
        self.max_carrying_capacity = update_carrying_capacity(self)
        self.barter = update_bartering(self)
        self.oration = update_oration(self)
        self.knowledge = update_knowledge(self)
        self.luck = update_luck_chance(self)
        previous_max_health = self.max_health
        self.max_health = update_maximum_health(self)
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

    def page_refresh_character(self):
        self.quest_notification = None

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
                my_item.amount_owned -= 1
                if my_item.amount_owned == 0:
                    self.inventory.remove(my_item)
                break

    def __str__(self):
        """Return string representation of Hero opject.
        """
        
        data = "Character object with attributes:"
        atts = []
        for key in sorted(vars(self).keys()):
            atts.append('{}: {} -> type: {}'.format(key, repr(vars(self)[key]), type(vars(self)[key])))
        data = '\n'.join(atts)
        return data
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def get_primary_attributes(self):
        return sorted(self.primary_attributes.items())


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




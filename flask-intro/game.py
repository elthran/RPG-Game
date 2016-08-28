#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

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
    def __init__(self, user_name="Unknown"):
        self.user_name = user_name
        self.character_name = "Unknown"
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
        
        self.equipped_items = []
        self.inventory = []
        self.abilities = []
        
    # Sets damage
    def update_secondary_attributes(self):
        self.min_damage = 3
        self.max_damage = 5
        self.attack_speed = 1
        self.attack_accuracy = 50         # A percentage
        self.first_strike = 15         # A percentage
        self.critical_hit = 15         # A percentage
        self.defence_modifier = 25         # A percentage
        self.evade_chance = 10         # A percentage
        self.parry_chance = 15         # A percentage
        self.block_chance = 10         # A percentage
        self.block_reduction = 35         # A percentage
        self.poisin_resistance = 5         # A percentage
        self.spiritual_resistance = 5         # A percentage
        self.stealth_skill = 5         # A percentage
        self.faith = 1
        self.max_health = 20
        self.max_sanctity = 10
        self.max_endurance = 25
        self.max_carrying_capacity = 35
        self.barter = 5
        self.oration = 5
        self.luck = 5                  # A percentage
        for ability in self.abilities:
            ability.update_stats()
        for item in self.equipped_items:
            item.update_stats()
        self.current_sanctity = self.max_sanctity
        self.current_health = self.max_health
        self.current_endurance = self.max_endurance
        self.current_carrying_capacity = self.max_carrying_capacity

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return
        self.current_exp = 0
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.age += 1
        self.update_secondary_attributes()

    def __repr__(self):
        return "\nName: %s" % (self.name)

# Temporary Function to create a random hero
def create_random_hero():
    myHero = Hero()
    myHero.update_secondary_attributes
    clothes = [Garment("Ripped Tunic", myHero, 25, 35), Garment("Medium Tunic", myHero, 25, 35), Garment("Strong Tunic", myHero, 25, 35)]
    weapons = [Weapon("Chipped Axe", myHero, 125, 3, 12, -0.5), Weapon("Chipped Knife", myHero, 75, 3, 5, 1), Weapon("Blunt Staff", myHero, 85, 4, 4, -0.7)]
    myHero.update_secondary_attributes
    
    # Abilities & Items (Temporary)
    test_ability = Ability("Stone Skin", myHero, skin_adjective)
    myHero.abilities.append(test_ability)
    myHero.inventory.append(clothes[0])
    myHero.inventory.append(weapons[0])
    myHero.inventory.append(weapons[1])
    
    # Refresh Hero
    myHero.update_secondary_attributes
    return myHero
# End of temporary functions


# initialization
myHero = create_random_hero()
game = Game(myHero)
enemy = monster_generator(myHero.age)


	



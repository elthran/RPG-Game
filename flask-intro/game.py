import math
from flask import request
from items import *
from bestiary import *
from abilities import *


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
        self.name = "Unknown"
        self.starting_class = "None"
        self.current_exp = 0
        self.max_exp = 10
        self.level = 1
        self.attribute_points = 0
        self.strength = 1
        self.endurance = 1
        self.vitality = 1
        self.agility = 1
        self.dexterity = 1
        self.devotion = 1
        self.resistance = 1
        self.wisdom = 1
        self.charm = 1
        self.instinct = 1
        self.abilities = []

    # Allows you to choose your starting class and apply buffs
    def choose_class(self):
        myHero.name = request.form['char_name']
        myHero.starting_class = request.form['spec']
        if myHero.starting_class == "Brute":
            myHero.strength += 2
            myHero.endurance += 1
        if myHero.starting_class == "Scholar":
            myHero.wisdom += 3
        if myHero.starting_class == "Scoundrel":
            myHero.agility += 2
            myHero.dexterity += 1
        return myHero

    # Sets damage
    def update_combat_stats(self):
        self.min_damage = self.strength + self.dexterity
        self.max_damage = (2 * self.strength) + self.dexterity
        self.speed = ((2 * self.agility) + self.dexterity) / 5
        self.defence = (3 * self.endurance) + self.dexterity
        for ability in self.abilities:
            ability.update_stats()

    # Sets max health and fully heals hero
    def update_health(self):
        self.max_hp = (5 * self.vitality) + self.endurance
        self.current_hp = self.max_hp

    def set_items(self,items):
        self.items = items

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return
        self.current_exp = 0
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.level += 1
        self.update_health()

    def __repr__(self):
        return "\nName: %s" % (self.name)

# Temporary Function to create a random hero
def create_random_hero():

    myHero = Hero()
    myHero.update_health()
    
    test_ability = Ability("Stone Skin", myHero, skin_adjective)
    myHero.abilities.append(test_ability)
    myHero.update_combat_stats()

    name = random.choice(["ripped tunic", "torn tunic"])
    dummy_item = Garment(name, myHero)
    item_list = [dummy_item]
    myHero.set_items(item_list)
    for item in myHero.items:
        item.equip()
    return myHero
# End of temporary functions


# initialization


myHero = create_random_hero()
game = Game(myHero)
enemy = monster_generator(myHero.level)

	



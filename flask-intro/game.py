import math
from flask import request
from items import *
from bestiary import *
from abilities import *

class Game(object):
    def __init__(self, hero):
        self.hero = hero

    def set_enemy(self, enemy):
        self.enemy = enemy

class Hero(object):
    def __init__(self, name, starting_class):
        self.name = name
        self.starting_class = starting_class

    # Creates a level 1 hero
    def create_hero(self, current_exp=0, max_exp=10, level=1, attribute_points=0):
        self.current_exp = current_exp
        self.max_exp = max_exp
        self.level = level
        self.attribute_points = attribute_points

    # Initializes attritubes to value of 1
    def create_attributes(self, strength=1, endurance=1, vitality=1, agility=1, dexterity=1, devotion=1, resistance=1, wisdom=1, charm=1, instinct=1):
        self.strength = strength
        self.endurance = endurance
        self.vitality = vitality
        self.agility = agility
        self.dexterity = dexterity
        self.devotion = devotion
        self.resistance = resistance
        self.wisdom = wisdom
        self.charm = charm
        self.instinct = instinct

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
        # Tmporary
        myHero.set_health(myHero.endurance, myHero.vitality)
        name = random.choice(["ripped tunic", "torn tunic"])
        dummy_item = Garment(name, myHero)
        item_list = [dummy_item]
        myHero.set_items(item_list)
        for item in myHero.items:
            item.equip()
        return myHero

    # Sets damage
    def set_damage(self, strength, damage=0):
        self.damage = 2 * strength

    # Sets max health and fully heals hero
    def set_health(self, endurance, vitality, max_hp=0, current_hp=0):
        self.max_hp = (3 * vitality) + endurance
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
        self.set_health(self.endurance, self.vitality, self.max_hp)

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

# Temporary Function to create a random hero
def create_random_hero():
    name = random.choice(["Jimmy", "Jacob", "Jimbo"])
    hero_class = random.choice(["Brute", "Scholar", "Scoundrel"])
    myHero = Hero(name, hero_class)
    myHero.create_hero()
    myHero.create_attributes()
    myHero.set_damage(myHero.strength)
    myHero.set_health(myHero.endurance, myHero.vitality)

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

	



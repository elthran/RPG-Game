import math
from items import *

class Hero(object):
    def __init__(self, name, level, attribute_points, current_exp, max_exp, starting_class, strength, speed, damage, vitality, hp, max_hp, wisdom, faith, affinity, wins):
        self.name = name
        self.level = level
        self.attribute_points = attribute_points
        self.current_exp = current_exp
        self.max_exp = max_exp
        self.starting_class = starting_class

        # Damage is calculated from strength and speed
        self.strength = strength
        self.speed = speed
        self.damage = damage

        # HP is calculated based on your vitality
        self.vitality = vitality
        self.hp = hp
        self.max_hp = max_hp

        # Affinity is calculated based on wisdom and faith
        self.wisdom = wisdom
        self.faith = faith
        self.affinity = affinity
        
        self.wins = wins

    def set_items(self,items):
        self.items = items	
	
    def update_attributes(self, strength, speed, vitality, wisdom, faith):
        self.damage = strength * speed
        self.max_hp = vitality * 10
        self.affinity = wisdom + faith

    def set_health(self, hp):
        self.hp = hp

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return
        self.current_exp = 0
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.level += 1

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

# initialization
myHero = Hero("Unknown", 1, 0, 0, 10, "", 3, 3, 0, 3, 0, 0, 3, 3, 0, 0)
myHero.update_attributes(myHero.strength, myHero.speed, myHero.vitality, myHero.wisdom, myHero.faith)

dummy_item = Garment("ripped tunic", myHero)
item_list = [dummy_item]
myHero.set_items(item_list)
for item in myHero.items:
    item.equip()
	
myHero.set_health(myHero.max_hp)



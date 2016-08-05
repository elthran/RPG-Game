import random
from game import *

class Monster(object):
    def __init__(self, name, level, species, strength, speed, damage, vitality, hp, max_hp, wisdom, faith, affinity):
        self.name = name
        self.level = level
        self.species = species
        
        self.strength = strength
        self.speed = speed
        self.damage = damage
        
        self.vitality = vitality
        self.hp = hp
        self.max_hp = max_hp

        self.wisdom = wisdom
        self.faith = faith
        self.affinity = affinity
		
    # Assign values for damage, max_hp, and affinity based on other stat values.
    def update_attributes(self, strength, speed, vitality, wisdom, faith):
        self.damage = strength * speed
        self.max_hp = vitality * 10
        self.affinity = wisdom + faith

    def set_health(self, hp):
        self.hp = hp

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

def monster_generator(level):
    names = {"Wolf":"Beast","Scout":"Goblin","Spider":"Beast"}
    name = random.choice(list(names.keys()))
    species = names[name]
    monster = Monster(name, level, species, 2, 2, 0, 2, 0, 0, 2, 2, 2)
    monster.update_attributes(monster.strength, monster.speed, monster.vitality, monster.wisdom, monster.faith)
    monster.set_health(monster.max_hp)
    return monster

enemy = monster_generator(myHero.level)

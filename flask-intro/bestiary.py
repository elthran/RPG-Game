import random
from game import *

class Monster(object):
    def __init__(self, name, species, level):
        self.name = name
        self.species = species
        self.level = level
        self.strength = 1 + self.level
        self.vitality = 1 + self.level
        self.experience_rewarded = 5 + level

    def combat_stats(self):        
        self.current_hp = 5 * self.vitality
        self.max_hp = self.current_hp
        self.min_damage = self.strength
        self.max_damage = 2 * self.strength
        self.attack_speed = 0.5 + (0.1 * self.level)
        self.accuracy = 50 + self.level
        self.dodge_chance = 1 + self.level
        self.defence_modifier = 1 + self.level

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

def monster_generator(level):
    name_and_species = {"Wolf":"Beast","Scout":"Goblin","Spider":"Beast"}
    name = random.choice(list(name_and_species.keys()))
    species = name_and_species[name]
    monster = Monster(name, species, level)
    monster.combat_stats()
    return monster

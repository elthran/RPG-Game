import random
from game import *

class Monster(object):
    def __init__(self, name, level, species, strength, speed, vitality, experience):
        self.name = name
        self.level = level
        self.species = species
        self.strength = strength
        self.speed = speed
        self.vitality = vitality
        self.experience = experience

    def combat_stats(self, vitality, strength, speed, current_hp=0, max_hp=0, min_damage=0, max_damage=0):
        
        self.current_hp = 5 * vitality
        self.max_hp = self.current_hp
        self.min_damage = strength
        self.max_damage = 2 * strength
        self.accuracy = 65
        self.dodge_chance = 15
        self.defence_modifier = 15

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

def monster_generator(level):
    name_species = {"Wolf":"Beast","Scout":"Goblin","Spider":"Beast"}
    name = random.choice(list(name_species.keys()))
    species = name_species[name]
    monster = Monster(name, level, species, 2, 0.1, 2, 5 + level)
    monster.combat_stats(monster.vitality, monster.strength, monster.speed)
    return monster

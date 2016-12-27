#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

import random

class Monster(object):
    def __init__(self, monster_id, name, species, species_plural, level, strength, vitality, experience_rewarded):
        self.monster_id = monster_id
        self.name = name
        self.species = species
        self.species_plural = species_plural
        self.level = level
        self.strength = strength + level
        self.vitality = vitality + level
        self.experience_rewarded = experience_rewarded + level
        self.items_rewarded = []

    def combat_stats(self):        
        self.current_health = 2 * self.vitality
        self.max_health = self.current_health
        self.min_damage = self.strength
        self.max_damage = self.strength
        self.attack_speed = 0.1 * self.level
        self.accuracy = 25 + self.level
        self.evade_chance = 5 + self.level
        self.defence_modifier = 5 + self.level

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

class NPC(object):
    def __init__(self, npc_id, name, race, age):
        self.npc_id = npc_id
        self.name = name
        self.race = race
        self.age = age

def monster_generator(level):
    monster = random.choice(bestiary_data)
    monster.level = level
    monster.combat_stats()
    return monster

bestiary_data = [Monster("001", "Alpha Wolf", "Wolf", "Wolves", 1, 1, 1, 1),
                 Monster("002", "Goblin Scout", "Goblin", "Goblins", 1, 1, 1, 1),
                 Monster("003", "Spiderling", "Spider", "Spiders", 1, 1, 1, 1)]
npc_data = [NPC("01", "Old Man", "Human", 87)]

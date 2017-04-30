#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

import random, math
from secondary_attributes import *

def monster_archetype_basic(monster):
    monster.primary_attributes["Vitality"] = random.randint(15,20) * 0.01 * monster.attribute_points
    monster.primary_attributes["Strength"] = random.randint(15,20) * 0.01 * monster.attribute_points
    monster.primary_attributes["Resilience"] = random.randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Fortitude"] = random.randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Reflexes"] = random.randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Agility"] = random.randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Perception"] = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Wisdom"] = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Divinity"] = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Charisma"] = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Survivalism"] = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Fortuity"] = random.randint(5,10) * 0.01 * monster.attribute_points
    return monster

class Monster(object):
    def __init__(self, monster_id, name, species, species_plural, level, archetype):
        self.monster_id = monster_id
        self.name = name
        self.species = species
        self.species_plural = species_plural
        self.level = level
        self.attribute_points = level * 2
        self.primary_attributes = {"Strength": 1, "Resilience": 1, "Vitality": 1, "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1, "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1}
        self.archetype = archetype
        self.experience_rewarded = level * 2
        self.items_rewarded = []

    def update_monster_secondary_attributes(self):        
        self.maximum_damage = update_monster_maximum_damage(self)
        self.minimum_damage = update_monster_minimum_damage(self)
        self.attack_speed = update_monster_attack_speed(self)
        self.attack_accuracy = update_monster_attack_accuracy(self)
        self.first_strike = update_monster_first_strike_chance(self)
        self.critical_hit_chance = update_monster_critical_hit_chance(self)
        self.critical_hit_modifier = update_monster_critical_hit_modifier(self)
        self.defence_modifier = update_monster_defence_modifier(self)
        self.evade_chance = update_monster_evade_chance(self)
        self.parry_chance = update_monster_parry_chance(self)
        self.riposte_chance = update_monster_riposte_chance(self)
        self.block_chance = update_monster_block_chance(self)
        self.block_reduction = update_monster_block_reduction(self)
        self.stealth_skill = update_monster_stealth_skill(self)
        self.faith = update_monster_faith(self)
        self.max_sanctity = update_monster_maximum_sanctity(self)
        self.luck = update_monster_luck_chance(self)
        self.max_health = update_monster_maximum_health(self)

        self.current_health = self.max_health
        self.current_sanctity = self.max_sanctity

    def __repr__(self):
        return "\nName: %s\nDamage: %s-%s\nHealth: %s/%s\nAttack Speed: %s\nAccuracy: %s" % (self.name, self.minimum_damage, self.maximum_damage, self.current_health, self.max_health, self.attack_speed, self.attack_accuracy)

def monster_generator(level):
    monster = random.choice(bestiary_data)
    monster.level = level
    monster.attribute_points = 2 * monster.level
    if monster.archetype == "basic":
        monster = monster_archetype_basic(monster)
    monster.update_monster_secondary_attributes()
    return monster

bestiary_data = [Monster("001", "Feral Dog", "Wolf", "Wolves", level=1, archetype="basic"),
                 Monster("002", "Giant Rat", "Goblin", "Goblins", level=1, archetype="basic")]










""" Don't bother looking below here"""









class NPC(object):
    def __init__(self, npc_id, name, race, age):
        self.npc_id = npc_id
        self.name = name
        self.race = race
        self.age = age
        
npc_data = [NPC("01", "Old Man", "Human", 87)]

#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

import random, math

def monster_archetype_basic(monster):
    monster.vitality = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.strength = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.resilience = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.fortitude = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.reflexes = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.agility = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.perception = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.wisdom = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.divinity = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.charisma = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.survivalism = random.randint(20,25) * 0.01 * monster.attribute_points
    monster.fortuity = random.randint(20,25) * 0.01 * monster.attribute_points
    return monster

def monster_archetype_high_health(monster):
    monster.vitality = random.randint(50,60) * 0.01 * monster.attribute_points
    monster.strength = random.randint(10,15) * 0.01 * monster.attribute_points
    monster.resilience = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.fortitude = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.reflexes = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.agility = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.perception = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.wisdom = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.divinity = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.charisma = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.survivalism = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.fortuity = random.randint(5,10) * 0.01 * monster.attribute_points
    return monster

def monster_archetype_high_damage(monster):
    monster.vitality = random.randint(15,20) * 0.01 * monster.attribute_points
    monster.strength = random.randint(45,55) * 0.01 * monster.attribute_points
    monster.resilience = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.fortitude = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.reflexes = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.agility = random.randint(25,30) * 0.01 * monster.attribute_points
    monster.perception = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.wisdom = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.divinity = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.charisma = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.survivalism = random.randint(5,10) * 0.01 * monster.attribute_points
    monster.fortuity = random.randint(5,10) * 0.01 * monster.attribute_points
    return monster

class Monster(object):
    def __init__(self, monster_id, name, species, species_plural, level, archetype):
        self.monster_id = monster_id
        self.name = name
        self.species = species
        self.species_plural = species_plural
        self.level = level
        self.attribute_points = level * 2
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
        self.archetype = archetype
        self.experience_rewarded = level * 2
        self.items_rewarded = []

    def set_combat_stats(self):        
        self.current_health = math.floor(self.vitality * 2)
        self.max_health = self.current_health
        self.min_damage = math.floor(self.strength * 2)
        self.max_damage = math.floor(self.agility * 2 + self.min_damage)
        self.attack_speed = self.agility * 0.05
        self.accuracy = 25 + self.level
        self.evade_chance = 5 + self.level
        self.defence_modifier = 5 + self.level

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

def monster_generator(level):
    monster = random.choice(bestiary_data)
    monster.level = level
    monster.attribute_points = 2 * monster.level
    if monster.archetype == "basic":
        monster = monster_archetype_basic(monster)
    if monster.archetype == "high health":
        monster = monster_archetype_high_health(monster)
    if monster.archetype == "high damage":
        monster = monster_archetype_high_damage(monster)
    monster.set_combat_stats()
    return monster

bestiary_data = [Monster("001", "Alpha Wolf", "Wolf", "Wolves", level=1, archetype="high health"),
                 Monster("002", "Goblin Scout", "Goblin", "Goblins", level=1, archetype="high damage"),
                 Monster("003", "Spiderling", "Spider", "Spiders", level=1, archetype="basic")]










""" Don't bother looking below here"""









class NPC(object):
    def __init__(self, npc_id, name, race, age):
        self.npc_id = npc_id
        self.name = name
        self.race = race
        self.age = age
        
npc_data = [NPC("01", "Old Man", "Human", 87)]

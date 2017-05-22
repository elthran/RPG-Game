#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from random import randint, choice
from proficiencies_monsters import MonsterProficiencies

monster_archetypes = {"wolf": [1.5, 0.1, 0.1, 0.2, 0.7, 0.5, 1, 1.5, 0.7, 0.8, 0.8, 0.1],
                      "goblin": [0.7, 0.2, 0.1, 0.2, 0.7, 0.5, 1, 1.5, 0.7, 0.8, 0.9, 0.3]
                      }

class AttributesMonster(object):
    def __init__(self, monster_level, monster_type):        
        self.agility = AttributeMonster("Agility", monster_level, monster_type[0])
        self.charisma = AttributeMonster("Charisma", monster_level, monster_type[1])
        self.divinity = AttributeMonster("Divinity", monster_level, monster_type[2])
        self.fortitude = AttributeMonster("Fortitude", monster_level, monster_type[3])
        self.fortuity = AttributeMonster("Fortuity", monster_level, monster_type[4])
        self.perception = AttributeMonster("Perception", monster_level, monster_type[5])
        self.reflexes = AttributeMonster("Reflexes", monster_level, monster_type[6])
        self.resilience = AttributeMonster("Resilience", monster_level, monster_type[7])
        self.strength = AttributeMonster("Strength", monster_level, monster_type[8])
        self.survivalism = AttributeMonster("Survivalism", monster_level, monster_type[9])
        self.vitality = AttributeMonster("Vitality", monster_level, monster_type[10])
        self.wisdom = AttributeMonster("Wisdom", monster_level, monster_type[11])

class AttributeMonster(object):
    def __init__(self, name, monster_level, modifier):
        self.name = name
        self.level = monster_level * modifier

class Monster(object):
    def __init__(self, monster_id, name, species, species_plural, level, monster_archetypes):
        self.monster_id = monster_id
        self.name = name
        self.species = species
        self.species_plural = species_plural
        self.level = level
        self.experience_rewarded = level * 2
        self.items_rewarded = []
        self.monster_archetypes = monster_archetypes

        self.attributes = AttributesMonster(level, monster_archetypes)
        self.proficiencies = MonsterProficiencies(self.attributes)

        self.health = self.proficiencies.health.maximum

    def __repr__(self):
        return "Unfinished Monster build"
    
def monster_generator(level):
    temp_monster = choice(bestiary_data)
    monster = Monster(temp_monster.monster_id, temp_monster.name, temp_monster.species, temp_monster.species_plural, level, temp_monster.monster_archetypes)
    return monster

bestiary_data = [Monster("001", "Feral Dog", "Wolf", "Wolves", level=1, monster_archetypes=monster_archetypes["wolf"]),
                 Monster("002", "Giant Rat", "Goblin", "Goblins", level=1, monster_archetypes=monster_archetypes["goblin"])]





""" Don't bother looking below here"""

class NPC(object):
    def __init__(self, npc_id, name, race, age):
        self.npc_id = npc_id
        self.name = name
        self.race = race
        self.age = age
        
npc_data = [NPC("01", "Old Man", "Human", 87)]

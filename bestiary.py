#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from random import randint, choice
from proficiencies_monsters import MonsterProficiencies

# Give each monster a rating for their attribute where 1 is about average. (So 2 is double, 4 is quadruple, 0.5 is half, 0.25 is a quarter, etc.)
archetypes = {
    "wolf": {"Agility": 3, "Charisma": 0.1, "Divinity": 0.1, "Fortitude": 0.7, "Fortuity": 0.25, "Perception": 0.75,
             "Reflexes": 4, "Resilience": 1, "Strength": 1, "Survivalism": 2, "Vitality": 1.25, "Wisdom": 0.1,
             "Species": "Wolf", "Plural": "Wolves"},
    "goblin": {"Agility": 1.5, "Charisma": 0.25, "Divinity": 0.25, "Fortitude": 0.7, "Fortuity": 1.25, "Perception": 0.6,
               "Reflexes": 1.2, "Resilience": 1.1, "Strength": 0.8, "Survivalism": 1.2, "Vitality": 0.8, "Wisdom": 0.75,
             "Species": "Goblin", "Plural": "Goblins"},
    "spider": {"Agility": 2, "Charisma": 0.1, "Divinity": 0.1, "Fortitude": 0.4, "Fortuity": 0.8, "Perception": 0.9,
               "Reflexes": 0.8, "Resilience": 0.7, "Strength": 0.5, "Survivalism": 2, "Vitality": 0.5, "Wisdom": 0.25,
             "Species": "Spider", "Plural": "Spiders"}
    }

class AttributesMonster(object):
    def __init__(self, monster_level, monster_type):        
        self.agility = AttributeMonster("Agility", monster_level, monster_type["Agility"])
        self.charisma = AttributeMonster("Charisma", monster_level, monster_type["Charisma"])
        self.divinity = AttributeMonster("Divinity", monster_level, monster_type["Divinity"])
        self.fortitude = AttributeMonster("Fortitude", monster_level, monster_type["Fortitude"])
        self.fortuity = AttributeMonster("Fortuity", monster_level, monster_type["Fortuity"])
        self.perception = AttributeMonster("Perception", monster_level, monster_type["Perception"])
        self.reflexes = AttributeMonster("Reflexes", monster_level, monster_type["Reflexes"])
        self.resilience = AttributeMonster("Resilience", monster_level, monster_type["Resilience"])
        self.strength = AttributeMonster("Strength", monster_level, monster_type["Strength"])
        self.survivalism = AttributeMonster("Survivalism", monster_level, monster_type["Survivalism"])
        self.vitality = AttributeMonster("Vitality", monster_level, monster_type["Vitality"])
        self.wisdom = AttributeMonster("Wisdom", monster_level, monster_type["Wisdom"])

class AttributeMonster(object):
    def __init__(self, name, monster_level, modifier):
        self.name = name
        self.level = monster_level * modifier * randint(10,30) * 0.05

class Monster(object):
    def __init__(self, name, archetype, level):
        self.name = name
        self.species = archetype["Species"]
        self.species_plural = archetype["Plural"]
        self.level = level
        self.experience_rewarded = level + 1
        self.items_rewarded = []
        self.archetype = archetype

        self.attributes = AttributesMonster(level, archetype)
        self.proficiencies = MonsterProficiencies(self.attributes)

        self.health = self.proficiencies.health.maximum

    def __repr__(self):
        return "Unfinished Monster build"

# THE CODE BELOW HERE IS SHIT AND I NEED HELP IMPROVING IT
def monster_generator(level):
    data = choice(bestiary_data)
    monster = Monster(*data, level=level)
    return monster

bestiary_data = [("Feral Dog", archetypes["wolf"]),
                 ("Giant Rat", archetypes["goblin"]),
                 ("Poisonous Spider", archetypes["spider"])]





""" Don't bother looking below here"""

class NPC(object):
    def __init__(self, npc_id, name, race, age):
        self.npc_id = npc_id
        self.name = name
        self.race = race
        self.age = age
        
npc_data = [NPC("01", "Old Man", "Human", 87)]

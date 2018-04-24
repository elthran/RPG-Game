#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from hero import Hero
from random import randint, choice
from proficiencies_monsters import MonsterProficiencies

# Give each monster a rating for their attribute where 1 is about average. (So 2 is double, 4 is quadruple, 0.5 is half, 0.25 is a quarter, etc.)
archetypes = {
    "wolf": {"Agility": 3, "Charisma": 0.1, "Divinity": 0.1, "Resilience": 0.7, "Fortuity": 0.25, "Pathfinding": 0.75,
             "Quickness": 4, "Willpower": 1, "Brawn": 1, "Survivalism": 2, "Vitality": 1.25, "Intellect": 0.1,
             "Species": "Wolf", "Plural": "Wolves"},
    "goblin": {"Agility": 1.5, "Charisma": 0.25, "Divinity": 0.25, "Resilience": 0.7, "Fortuity": 1.25, "Pathfinding": 0.6,
               "Quickness": 1.2, "Willpower": 1.1, "Brawn": 0.8, "Survivalism": 1.2, "Vitality": 0.8, "Intellect": 0.75,
             "Species": "Goblin", "Plural": "Goblins"},
    "spider": {"Agility": 2, "Charisma": 0.1, "Divinity": 0.1, "Resilience": 0.4, "Fortuity": 0.8, "Pathfinding": 0.9,
               "Quickness": 0.8, "Willpower": 0.7, "Brawn": 0.5, "Survivalism": 2, "Vitality": 0.5, "Intellect": 0.25,
             "Species": "Spider", "Plural": "Spiders"}
    }

class AttributesMonster(object):
    def __init__(self, monster_level, monster_type):        
        self.agility = AttributeMonster("Agility", monster_level, monster_type["Agility"])
        self.charisma = AttributeMonster("Charisma", monster_level, monster_type["Charisma"])
        self.divinity = AttributeMonster("Divinity", monster_level, monster_type["Divinity"])
        self.willpower = AttributeMonster("Willpower", monster_level, monster_type["Willpower"])
        self.fortuity = AttributeMonster("Fortuity", monster_level, monster_type["Fortuity"])
        self.pathfinding = AttributeMonster("Pathfinding", monster_level, monster_type["Pathfinding"])
        self.quickness = AttributeMonster("Quickness", monster_level, monster_type["Quickness"])
        self.resilience = AttributeMonster("Resilience", monster_level, monster_type["Resilience"])
        self.brawn = AttributeMonster("Brawn", monster_level, monster_type["Brawn"])
        self.survivalism = AttributeMonster("Survivalism", monster_level, monster_type["Survivalism"])
        self.vitality = AttributeMonster("Vitality", monster_level, monster_type["Vitality"])
        self.intellect = AttributeMonster("Intellect", monster_level, monster_type["Intellect"])

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

def generate_monster(terrain=None):
    #terrain = getattr(MonsterTemplate, terrain)
    #monsters = database.session.query(MonsterTemplate).filter(terrain == True).all()
    return Hero(name="monsterBoy")

class NPC(object):
    def __init__(self, id, name, race, age):
        self.id = id
        self.name = name
        self.race = race
        self.age = age

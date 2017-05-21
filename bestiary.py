#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from random import randint, choice
from proficiencies_monsters import MonsterProficiencies

def monster_archetype_basic(monster):
    monster.primary_attributes["Vitality"] = randint(15,20) * 0.01 * monster.attribute_points
    monster.primary_attributes["Strength"] = randint(15,20) * 0.01 * monster.attribute_points
    monster.primary_attributes["Resilience"] = randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Fortitude"] = randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Reflexes"] = randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Agility"] = randint(10,15) * 0.01 * monster.attribute_points
    monster.primary_attributes["Perception"] = randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Wisdom"] = randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Divinity"] = randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Charisma"] = randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Survivalism"] = randint(5,10) * 0.01 * monster.attribute_points
    monster.primary_attributes["Fortuity"] = randint(5,10) * 0.01 * monster.attribute_points
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

        self.proficiencies = MonsterProficiencies()

        self.health = self.proficiencies.health.maximum

    def update_monster(self):        
        for proficiency in self.proficiencies:
            proficiency.update(self)

    def __repr__(self):
        return "Unfinished Monster build"
    
def monster_generator(level):
    monster = choice(bestiary_data)
    monster.level = level
    monster.attribute_points = 2 * monster.level
    if monster.archetype == "basic":
        monster = monster_archetype_basic(monster)
    monster.update_monster()
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

#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

"""Objects used in the database and the game.

Suggestion: change name to game_objects.py
"""

try:
    from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship

    from sqlalchemy import orm
    from sqlalchemy.orm.collections import attribute_mapped_collection
    from sqlalchemy.orm import validates
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e

from base_classes import Base, BaseDict

import math
from flask import request
from attributes import Attributes
from proficiencies import Proficiencies
from inventory import Inventory

import datetime
import pdb

# function used in '/level_up'
#Fix ME! Or put me in a class as a method or something.
def convert_input(x):
    try:
        x = int(x)
    except:
        x = 0
    return x

#Custom constants for primary_attributes list.
AGILITY = 0
CHARISMA = 1
DIVINITY = 2
FORTITUDE = 3
FORTUITY = 4
PERCEPTION = 5
REFLEXES = 6
RESILIENCE = 7
STRENGTH = 8
SURVIVALISM = 10
VITALITY = 11
WISDOM = 11

"""
USE: primary_attributes[AGILITY] == value of agility stored in list at position 0
primary_attributes[FORTITUDE] == value of fortitude stored in list at position 4
"""

class Game(object):
    def __init__(self, hero):
        self.hero = hero
        self.has_enemy = False

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.has_enemy = True


class User(Base):
    """User class holds data about the current gamer.

    This is database ready and connects to the Hero class.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
    timestamp = Column(DateTime)
    is_admin = Column(Boolean)


class Hero(Base):
    """Store data about the Hero/Character object.

    """
    __tablename__ = 'hero'

    id = Column(Integer, primary_key=True)
    name = Column(String) #Was nullable=False now it isn't. I hope that is a good idea.
    character_name = orm.synonym('name')

    age = Column(Integer)
    archetype = Column(String)
    specialization = Column(String)
    religion = Column(String)
    house = Column(String)
    experience = Column(Integer)
    experience_maximum = Column(Integer)
    renown = Column(Integer)    # How famous you are
    virtue = Column(Integer)    # How good/evil you are
    devotion = Column(Integer)  # How religious you are
    gold = Column(Integer)

    basic_ability_points = Column(Integer)
    archetypic_ability_points = Column(Integer)
    specialized_ability_points = Column(Integer)
    pantheonic_ability_points = Column(Integer)
    attribute_points = Column(Integer)
    proficiency_points = Column(Integer)

    #Time code of when the (account?) was created
    timestamp = Column(DateTime)

    #Relationships: see complex_relationships.py

    def __init__(self, **kwargs):
        """Initialize the Hero object.

        Currently only accepts keywords. Consider changing this.
        Consider having some Non-null values?

        NOTE: relationships must be assignment in complex_relationships.py
        and then imported after game.py. But before an object is created.
        Otherwise the relationships will be overwritten.

        exp_percent is now updated by current_exp using a validator.
        max_exp should be assigned a value before current_exp.
        """
        self.attributes = Attributes()
        self.proficiencies = Proficiencies()
        self.inventory = Inventory()

        #Defaults will remain unchanged if no arguments are passed.
        self.age = 7
        self.archetype = None
        self.specialization = None
        self.religion = None
        self.house = None

        self.experience = 0
        self.experience_maximum = 10

        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        self.basic_ability_points = 0
        self.archetypic_ability_points = 0
        self.specialized_ability_points = 0
        self.pantheonic_ability_points = 0
    
        self.attribute_points = 10
        self.proficiency_points = 10

        # Hidden attributes // Maybe they should be a special type of proficiency?
        self.experience_gain_modifier = 1 # This is the percentage of exp you gain
        self.gold_gain_modifier = 1 # This is the percentage of gold you gain

        #Time code
        self.timestamp = datetime.datetime.utcnow()

        for key in kwargs:
            setattr(self, key, kwargs[key])

        #self.refresh_proficiencies()
        self.refresh_character()


    def not_yet_implemented():
        self.kill_quests = BaseDict()

        self.chest_equipped = []
        self.errands = []
        self.completed_quests = []
        self.completed_achievements = []
        self.bestiary = []

        self.wolf_kills = 0


    #May no longer be neccessary? As Proficiencies are dynamic objects.
    # Sets damage
    @orm.reconstructor # Database gatekeeper? Delete this? break into separate parts
    def refresh_proficiencies(self):
        for proficiency in self.proficiencies:
            proficiency.update(self)
            
    def equipped_items(self):
        return [item for item in self.inventory if item.equipped] or [None]
        
    def non_equipped_items(self):
        return self.inventory.unequipped or [None]

    def update_proficiencies(self): # This needs to be renamed because it is not a proficiency updater
        """Update secondary attributes of Hero object on database load.

        See: init_on_load() in SQLAlchemy
        """

        ######Not implemented
        self.chest_equipped = []
        self.errands = []
        self.completed_quests = []
        self.completed_achievements = []
        self.bestiary = []

        self.wolf_kills = 0
        #######

        for ability in self.abilities:
            ability.update_stats(self)
        for item in self.equipped_items:
            item.update_stats(self)

        #Rebuild percent values. Silly but effective.
        self.experience = self.experience

    def refresh_character(self):
        self.proficiencies.health.current = self.proficiencies.health.maximum
        self.proficiencies.sanctity.current = self.proficiencies.sanctity.maximum
        self.proficiencies.endurance.current = self.proficiencies.endurance.maximum
        #self.storage = self.storage_maximum

    def page_refresh_character(self):
        self.quest_notification = None

    # updates field variables when hero levels up
    def level_up(self, attribute_points, experience, experience_maximum):
        if self.experience < self.experience_maximum:
            return False
        self.experience -= self.experience_maximum
        self.experience_maximum = math.floor(1.5 * self.experience_maximum)
        self.attribute_points += 1
        self.proficiency_points += 1
        self.age += 1
        self.proficiencies.health.current = self.proficiencies.health.maximum
        self.update_proficiencies()
        return True

    def consume_item(self, item_name):
        for my_item in self.inventory:
            if my_item.name == item_name:
                my_item.apply_effect()
                my_item.amount_owned -= 1
                if my_item.amount_owned == 0:
                    self.inventory.remove(my_item)
                break


    # @validates('current_city')
    # def validate_current_city(self, key, location):
        # """Assert that current_city is in fact a city.

        # Also allow current_city to be None.
        # """
        # try:
            # assert location.type in ("Cave", "Town")
            # return location
        # except AttributeError:
            # assert location is None
            # return None


    @validates('current_location')
    def validate_current_location(self, key, location):
        """Updates value of current_city on assignment.

        If current_location is a city ... set value of current_city as well.
        If not remove the value of current_city.
        """
        if location.type in ("Cave", "Town"):
            self.current_city = location
        else:
            self.current_city = None
        return location

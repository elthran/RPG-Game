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
    from sqlalchemy import Table, Column, Integer, String, DateTime

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
from secondary_attributes import *
from proficiencies import Proficiency
from attributes import Attributes
    
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


class Inventory(Base):
    """Store a list of items for the hero.
    
    This is a special class that will allow me to do more natural pythonic operations
    on a list of items. In theory. Sort of a 'wrapper' I guess?
    """
    __tablename__ = 'inventory'
 
    id = Column(Integer, primary_key=True)
    
    #Marked for restructuring as causes conflics with multiple heroes?
    #As in if hero1 has 4 of an item then hero2 will as well?
    #Move to Inventory?
    #amount_owned = Column(Integer)
    # Maybe I don't even need this at all?
    
    def add_item(self, item):
        self.items.append(item)
    
    def __iter__(self):
        return (item for item in self.items)
        
  
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
    current_exp = Column(Integer)
    max_exp = Column(Integer)
    renown = Column(Integer)
    virtue = Column(Integer)
    devotion = Column(Integer)
    gold = Column(Integer)

    # Jacob added the new "secondary attributes"
    proficiency_attack_damage = Column(Integer)
    proficiency_attack_speed = Column(Integer)
    proficiency_attack_accuracy = Column(Integer)
    proficiency_first_strike = Column(Integer)
    proficiency_critical_hit = Column(Integer)
    proficiency_defence = Column(Integer)
    proficiency_evade = Column(Integer)
    proficiency_parry = Column(Integer)
    proficiency_riposte = Column(Integer)
    proficiency_block = Column(Integer)
    proficiency_stealth = Column(Integer)
    proficiency_pickpocketing = Column(Integer)
    proficiency_faith = Column(Integer)
    proficiency_bartering = Column(Integer)
    proficiency_oration = Column(Integer)
    proficiency_knowledge = Column(Integer)
    proficiency_resist_frost = Column(Integer)
    proficiency_resist_flame = Column(Integer)
    proficiency_resist_shadow = Column(Integer)
    proficiency_resist_holy = Column(Integer)
    proficiency_resist_blunt = Column(Integer)
    proficiency_resist_slashing = Column(Integer)
    proficiency_resist_piercing = Column(Integer)

    # Jacob's Test Value
    #@Jacob by Marlen
    #This value needs to be asigned as a relationship here.
    #And then this statement would go in __init__.
    # proficiency_test = Proficiency("Testing", "How much testing you do", "Vitality")

    ability_points = Column(Integer)
    basic_ability_points = Column(Integer)
    archetype_ability_points = Column(Integer)
    specialization_ability_points = Column(Integer)
    pantheonic_ability_points = Column(Integer)
    
    attribute_points = Column(Integer)
    proficiency_points = Column(Integer)
        
    current_sanctity = Column(Integer)
    current_health = Column(Integer)

    attack_speed_skill = Column(Integer)
    
    #Marked for rename
    #Consider "endurance" instead.
    current_endurance = Column(Integer)
    current_carrying_capacity = Column(Integer)
    max_health = Column(Integer)
    
    #Time code
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
        self.inventory = Inventory()
        
        #Defaults will remain unchanged if no arguments are passed.
        self.age = 7
        self.archetype = "Woodsman"
        self.specialization = "Hunter"
        self.religion = "Dryarch"
        self.house = "Unknown"
        
        self.max_exp = 10
        self.current_exp = 0
        
        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        #Jacob added new "secondary attributes"
        self.proficiency_attack_damage = 0
        self.proficiency_attack_speed = 0
        self.proficiency_attack_accuracy = 0
        self.proficiency_first_strike = 0
        self.proficiency_critical_hit = 0
        self.proficiency_defence = 0
        self.proficiency_evade = 0
        self.proficiency_parry = 0
        self.proficiency_riposte = 0
        self.proficiency_block = 0
        self.proficiency_stealth = 0
        self.proficiency_pickpocketing = 0
        self.proficiency_faith = 0
        self.proficiency_bartering = 0
        self.proficiency_oration = 0
        self.proficiency_knowledge = 0

        self.proficiency_resist_frost = 0
        self.proficiency_resist_flame = 0
        self.proficiency_resist_shadow = 0
        self.proficiency_resist_holy = 0
        self.proficiency_resist_blunt = 0
        self.proficiency_resist_slashing = 0
        self.proficiency_resist_piercing = 0
    
        self.ability_points = 3 #TEMP. Soon will use the 4 values below
        self.basic_ability_points = 5
        self.archetype_ability_points = 5
        self.specialization_ability_points = 5
        self.pantheonic_ability_points = 5
    
        self.attribute_points = 5
        self.proficiency_points = 10
        
        #Build before *_current so that *_percents and validators work.
        self.max_sanctity = 0
        self.max_endurance = 0
        
        self.current_sanctity = 0
        self.current_health = 0
        self.current_endurance = 0
        self.current_carrying_capacity = 0
        self.attack_speed_skill = 0
        
        #Time code
        self.timestamp = datetime.datetime.utcnow()
        
        for key in kwargs:
            setattr(self, key, kwargs[key])
        
        self.update_secondary_attributes()
        self.refresh_character()

    
    def not_yet_implemented():
        self.kill_quests = BaseDict()
        
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
        
        self.chest_equipped = []
        self.errands = []
        self.completed_quests = []
        self.completed_achievements = []
        self.bestiary = []

        self.wolf_kills = 0
    

    # Sets damage
    @orm.reconstructor
    def update_secondary_attributes(self):
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

        #Make a list of the equipped items or if none are equipt return empty list.
        self.equipped_items = [item for item in self.inventory if item.wearable] or []

        self.max_damage = update_maximum_damage(self)
        self.maximum_damage = self.max_damage #Synonym for max_damage
        self.min_damage = update_minimum_damage(self)
        self.minimum_damage = self.min_damage #Synonym for min_damage
        self.attack_speed = update_attack_speed(self)
        self.attack_accuracy = update_attack_accuracy(self) # Should also have a related attribute of increasing critical hit %
        self.first_strike = update_first_strike_chance(self)
        self.critical_hit_chance = update_critical_hit_chance(self)
        self.critical_hit_modifier = update_critical_hit_modifier(self)
        self.defence_modifier = update_defence_modifier(self)
        self.evade_chance = update_evade_chance(self)
        self.parry_chance = update_parry_chance(self)
        self.riposte_chance = update_riposte_chance(self)
        self.block_chance = update_block_chance(self)
        self.block_reduction = update_block_reduction(self)
        self.stealth_skill = update_stealth_skill(self)
        self.faith = update_faith(self)
        self.max_sanctity = update_maximum_sanctity(self)
        self.max_endurance = update_maximum_endurance(self)
        self.max_carrying_capacity = update_carrying_capacity(self)
        self.barter = update_bartering(self)
        self.oration = update_oration(self)
        self.knowledge = update_knowledge(self)
        self.luck = update_luck_chance(self)
        
        #Marked for restructure
        # try:
            # previous_max_health = self.max_health
        # except KeyError:
            # pass
        self.max_health = update_maximum_health(self)
        # if not previous_max_health:
                # previous_max_health = self.max_health
                
        # Hidden attributes
        self.experience_gain_modifier = 1 # This is the percentage of exp you gain
        self.gold_gain_modifier = 1 # This is the percentage of gold you gain

        for ability in self.abilities:
            ability.update_stats(self)
        for item in self.equipped_items:
            item.update_stats()
        
        #Rebuild percent values.
        self.current_endurance = self.current_endurance
        self.current_exp = self.current_exp
        self.current_sanctity = self.current_sanctity
        
    
    @validates('max_health')
    def sync_current_health(self, key_name, health_value):
        """Reduce current_health if current_health overflows max_health.
        """
        try:
            self.current_health = min(self.current_health, health_value)
        except TypeError:
            self.current_health = 0
        return health_value
        
        
    @validates('current_endurance')
    def sync_endurance_percent(self, key_name, endurance_value):
        """Update endurance_percent on current_endurance change.
        
        """

        try:
            self.endurance_percent = round(endurance_value / self.max_endurance, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.endurance_percent = 0
        
        return max(endurance_value, 0)
        
    @validates('current_sanctity')
    def sync_sanctity_percent(self, key_name, sanctity_value):
        """Update sanctity_percent on current_sanctity change.
        
        """

        try:
            self.sanctity_percent = round(sanctity_value / self.max_sanctity, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.sanctity_percent = 0
        
        return max(sanctity_value, 0)
    
    @validates('current_exp')
    def sync_exp_percent(self, key_name, xp_value):
        """Update exp_percent on current_exp change.
        
        String conversion occurs in HTML and add the percent sign is added there to.
        key_name is "current_exp" .. not actually used here at this time but it is sent to
        this function so it must be accepted.
        """
        
        try:
            self.exp_percent = round(xp_value / self.max_exp, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.exp_percent = 0
        return xp_value
        
    @validates('current_health')
    def sync_health_percent(self, key_name, health_value):
        """Update health_percent on current_health change.
        
        """

        try:
            self.health_percent = round(health_value / self.max_health, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.health_percent = 0
        
        return max(health_value, 0)
        
    def refresh_character(self):
        self.current_sanctity = self.max_sanctity
        self.current_health = self.max_health
        self.current_endurance = self.max_endurance
        self.current_carrying_capacity = self.max_carrying_capacity

    def page_refresh_character(self):
        self.quest_notification = None

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return False
        self.current_exp -= self.max_exp
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.age += 1
        self.ability_points += 2
        self.current_health = self.max_health
        self.update_secondary_attributes()
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
                 
                  
                  
# Temporary Function to create a random hero
def create_random_hero():
    myHero = Hero()
    myHero.name = "Unknown"
    myHero.gold = 5000
    myHero.update_secondary_attributes()
    myHero.refresh_character()
    return myHero
# End of temporary functions





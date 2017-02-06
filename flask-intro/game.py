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
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e
    
from base_classes import Base, BaseDict

import math
from flask import request
from secondary_attributes import *
    
import datetime

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
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)

    def __repr__(self):
       return "<User(username='{}', password='{}', email='{}')>" .format(
                        self.username, self.password, self.email)
                        
                        
class Hero(Base):
    """Store data about the Hero/Character object.
    
    TODO: Builds secondary_attributes on_load constructor.
    """
    __tablename__ = 'heroes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String) #Was nullable=False now it isn't. I hope that is a good idea.
    character_name = orm.synonym('name')  
    
    age = Column(Integer, default=7)
    archetype = Column(String, default="Woodsman")
    specialization = Column(String, default="Hunter")
    religion = Column(String, default="Dryarch")
    house = Column(String, default="Unknown")
    current_exp = Column(Integer, default=0)
    max_exp = Column(Integer, default=10)
    renown = Column(Integer, default=0)
    virtue = Column(Integer, default=0)
    devotion = Column(Integer, default=0)
    gold = Column(Integer, default=50)
    
    ability_points= Column(Integer, default=3) #TEMP. Soon will use the 4 values below
    basic_ability_points = Column(Integer, default=0)
    archetype_ability_points = Column(Integer, default=0)
    specialization_ability_points = Column(Integer, default=0)
    pantheonic_ability_points = Column(Integer, default=0)
    
    attribute_points = Column(Integer, default=0)
        
    current_sanctity = Column(Integer, default=0)
    current_health = Column(Integer, default=10)
    
    #Marked for rename
    #Consider "endurance" instead.
    current_endurance = Column(Integer, default=0)
    current_carrying_capacity = Column(Integer, default=0)
    max_health = Column(Integer, default=10)
    
    #Time code
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    
    #Relationships: see complex_relationships.py
    
    def __init__(self, name=None, archetype=None, user=None):
        self.name = name
        self.archetype = archetype
        self.user = user
        
        self.primary_attributes = BaseDict({"Strength": 1, "Resilience": 1, "Vitality": 1,
            "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1,
            "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1})
        self.kill_quests = BaseDict()

    
    def not_yet_implemented():
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
        self.current_quests = []
        self.completed_quests = []
        self.completed_achievements = []
        self.kill_quests = {}
        self.bestiary = []

        self.known_locations = []
        self.wolf_kills = 0
    

    # Sets damage
    @orm.reconstructor
    def update_secondary_attributes(self):
        """Update secondary attributes of Hero object on database load.
        
        See: init_on_load() in SQLAlchemy
        """
        #Make a list of the equipped items or if none are equipt return empty list.
        self.equipped_items = [item for item in self.inventory if item.equiptable] or []

        self.max_damage = update_maximum_damage(self)
        self.maximum_damage = self.max_damage #Synonym for max_damage
        self.min_damage = update_minimum_damage(self)
        self.minimum_damage = self.min_damage #Synonym for min_damage
        self.attack_speed = update_attack_speed(self)
        self.attack_accuracy = update_attack_accuracy(self)
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
        previous_max_health = self.max_health
        self.max_health = update_maximum_health(self)
        # Hidden attributes
        self.experience_gain_modifier = 1 # This is the percentage of exp you gain
        self.gold_gain_modifier = 1 # This is the percentage of gold you gain

        for ability in self.abilities:
            ability.update_stats()
        for item in self.equipped_items:
            item.update_stats()

        # When you update max_health, current health will also change by the same amount
        max_health_change = self.max_health - previous_max_health
        if max_health_change != 0: 
            self.current_health += max_health_change	
        if self.current_health < 0:
            self.current_health = 0	        
        
    def refresh_character(self):
        self.current_sanctity = self.max_sanctity
        self.current_health = self.max_health
        self.current_endurance = self.max_endurance
        self.current_carrying_capacity = self.max_carrying_capacity

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

           
    def __repr__(self): 
        """Return string data about Hero object.
        """
        atts = []
        column_headers = self.__table__.columns.keys()
        extra_attributes = [key for key in vars(self).keys() if key not in column_headers]
        for key in column_headers:
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
            
        for key in sorted(extra_attributes):
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
        
        data = "<Hero(" + ', '.join(atts) + ')>'
        return data 
    
    # def __eq__(self, other): 
        # return self.__dict__ == other.__dict__
        
    def get_primary_attributes(self):
        return sorted(self.primary_attributes.items())
        

    
      

# Temporary Function to create a random hero
def create_random_hero():
    myHero = Hero()
    myHero.name = "Unknown"
    myHero.gold = 5000
    myHero.update_secondary_attributes()
    myHero.refresh_character()
    return myHero
# End of temporary functions





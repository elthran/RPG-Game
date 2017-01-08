#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

"""Objects used in the database and the game.

Suggestion: change name to game_objects.py
"""

import math
from flask import request
# from items import *
from bestiary import *
# from abilities import Ability, Archetype_Ability, Class_Ability, Religious_Ability
from secondary_attributes import *

try:
    from saveable_objects import Base
    from sqlalchemy import Table, Column, Integer, String, DateTime, ARRAY

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
    
    from sqlalchemy import orm
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")
    
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

# heroes_ablities_association_table = Table('heroes_ablities_association', Base.metadata,
    # Column('heroes_id', Integer, ForeignKey('heroes.id')),
    # Column('abilities_id', Integer, ForeignKey('abilities.id'))
# )

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
    
    heroes = relationship("Hero", order_by='Hero.character_name', back_populates='user')

    def __repr__(self):
       return "<User(username='{}', password='{}', email='{}')>" .format(
                        self.username, self.password, self.email)
                        
                        
class Hero(Base):
    """Store data about the Hero/Character object.
    
    TODO: Builds secondary_attributes on_load constructor.
    """
    __tablename__ = 'heroes'
    
    id = Column(Integer, primary_key=True)
    character_name = Column(String) #Was nullable=False now it isn't. I hope that is a good idea.
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
    current_health = Column(Integer, default=0)
    
    #Marked for rename
    #Consider "endurance" instead.
    current_endurance = Column(Integer, default=0)
    current_carrying_capacity = Column(Integer, default=0)
    max_health = Column(Integer, default=0)
    
    #Time code
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    
    #Relationships
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="heroes")
    primary_attributes = relationship("PrimaryAttributeList", uselist=False, back_populates="hero")
    abilities = relationship("Ability", order_by="Ability.name", back_populates="myHero")
    
    world_map_id = Column(Integer, ForeignKey('world_map.id'))
    current_world = relationship("World_Map", back_populates="heroes")
    
    town_id = Column(Integer, ForeignKey('town.id'))
    current_city = relationship("Town", back_populates="heroes")
    
    #inventor is list of character's items.
    inventory = relationship("Item", order_by="Item.name", back_populates="myHero")
    
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
        self.min_damage = update_minimum_damage(self)
        self.attack_speed = update_attack_speed(self)
        self.attack_accuracy = update_attack_accuracy(self)
        self.first_strike = update_first_strike_chance(self)
        self.critical_hit = update_critical_hit_chance(self)
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
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def get_primary_attributes(self):
        return sorted(self.primary_attributes.items())
        

class PrimaryAttributeList(Base):
    """The list of primary attributes of a Hero object.
    
    This list pretends to be a dictionary and so is subscriptable, see __getitem__ method.
    
    There is a simpler way to do this: http://docs.sqlalchemy.org/en/latest/orm/collections.html?highlight=instrumented#dictionary-collections
    But I used this instead as it allows me to use case insensitive keyword names.
    And because it didn't make sense the first time I read it.
    """
    __tablename__ = "primary_attributes"
    
    id = Column(Integer, primary_key=True)
    agility = Column(Integer, default=1)
    charisma = Column(Integer, default=1)
    divinity = Column(Integer, default=1)
    fortitude = Column(Integer, default=1)
    fortuity = Column(Integer, default=1)
    perception = Column(Integer, default=1)
    reflexes = Column(Integer, default=1)
    resilience = Column(Integer, default=1)
    strength = Column(Integer, default=1)
    survivalism = Column(Integer, default=1)
    vitality = Column(Integer, default=1)
    wisdom = Column(Integer, default=1)
    
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship("Hero", back_populates='primary_attributes')
    
    def __getitem__(self, key):
        """Allows the PrimaryAttributeList to be subscriptable.
        
        USE: primary_attributes['strength'] gets primary_attributes.strength
        
        !Important! NOT case sensitive!
        So: primary_attributes['strength'] == primary_attributes['Strength'] = primary_attributes['stREnGtH']
        
        Oh an using game constants you can also use primary_attributes[STRENGTH] and it should work ... though
        this is untested.
        """
        return getattr(self, key.lower())
    
    def __repr__(self):
        """Returns string representation of PrimaryAttributeList.
        
        NOTE: this is actually a list but behaves like a dictionary too, but is case insensitive.
        """
        atts = []
        for key in self.__table__.columns.keys():
            atts.append('{}={}'.format(key, getattr(self, key)))
        
        data = "<PrimaryAttributeList(" + ', '.join(atts) + ')>'
        return data
      

# Temporary Function to create a random hero
def create_random_hero():
    myHero = Hero()
    myHero.name = "Unknown"
    myHero.gold = 5000
    myHero.update_secondary_attributes()
    myHero.refresh_character()
    return myHero
# End of temporary functions




# initialization
# myHero = create_random_hero()
# game = Game(myHero)
# enemy = monster_generator(myHero.age)

# Super temporary while testing quests
# myHero.inventory.append(Quest_Item("Wolf Pelt", myHero, 50))
# myHero.inventory.append(Quest_Item("Spider Leg", myHero, 50))
# myHero.inventory.append(Quest_Item("Copper Coin", myHero, 50))
# for item in myHero.inventory:
    # item.amount_owned = 5




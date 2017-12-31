import math
import random
import datetime
import pdb

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.orm import validates

from base_classes import Base
from attributes import Attributes
from abilities import Abilities
from proficiencies import Proficiencies
from inventory import Inventory
from journal import Journal


class Hero(Base):
    """Store data about the Hero/Character object.

    """
    __tablename__ = 'hero'

    id = Column(Integer, primary_key=True)
    name = Column(
        String)  # Was nullable=False now it isn't. I hope that is a good idea.
    character_name = orm.synonym('name')

    age = Column(Integer)
    archetype = Column(String)
    calling = Column(String)
    religion = Column(String)
    house = Column(String)
    experience = Column(Integer)
    experience_maximum = Column(Integer)
    renown = Column(Integer)  # How famous you are
    virtue = Column(Integer)  # How good/evil you are
    devotion = Column(Integer)  # How religious you are
    gold = Column(Integer)

    basic_ability_points = Column(Integer)
    archetype_ability_points = Column(Integer)
    calling_ability_points = Column(Integer)
    pantheonic_ability_points = Column(Integer)
    attribute_points = Column(Integer)
    proficiency_points = Column(Integer)

    deepest_dungeon_floor = Column(Integer)  # High score for dungeon runs
    current_dungeon_floor = Column(Integer)  # Which floor of dungeon your on
    current_dungeon_floor_progress = Column(
        Integer)  # Current progress in current cave floor
    random_encounter_monster = Column(
        Boolean)  # Checks if you are currently about to fight a monster

    # Time code of when the (account?) was created
    timestamp = Column(DateTime)
    # Date of last login
    last_login = Column(String)

    login_alerts = Column(
        String)  # Testing messages when you are attacked or get a new message

    # Relationships
    # Many heroes -> one map/world. (bidirectional)
    map_id = Column(Integer, ForeignKey('location.id'))
    current_world = relationship("Location", back_populates='heroes',
                                 foreign_keys='[Hero.map_id]')
    # Each current_location -> can be held by Many Heroes (bidirectional)
    current_location_id = Column(Integer, ForeignKey('location.id'))
    current_location = relationship(
        "Location", back_populates='heroes_by_current_location',
        foreign_keys='[Hero.current_location_id]')

    # Each current_city -> can be held by Many Heroes (bidirectional)
    # (Town or Cave)
    city_id = Column(Integer, ForeignKey('location.id'))
    current_city = relationship(
        "Location", back_populates='heroes_by_city',
        foreign_keys='[Hero.city_id]')

    # When you die, you should return to the last city you were at.
    last_city_id = Column(Integer, ForeignKey('location.id'))
    last_city = relationship(
        "Location", back_populates='heroes_by_last_city',
        foreign_keys='[Hero.last_city_id]')

    # Each hero can have one set of Abilities. (bidirectional, One to One).
    abilities = relationship("Abilities", uselist=False, back_populates='hero')

    # User to Hero. One to many. Ordered!
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates='heroes')

    # Each Hero has One inventory. (One to One -> bidirectional)
    # inventory is list of character's items.
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    inventory = relationship("Inventory", back_populates="hero")

    # Attributes One to One despite the name
    attributes_id = Column(Integer, ForeignKey('attributes.id'))
    attributes = relationship("Attributes", back_populates='hero')

    # Proficiencies One to One despite the name
    proficiencies_id = Column(Integer, ForeignKey('proficiencies.id'))
    proficiencies = relationship("Proficiencies", back_populates='hero')

    # Journal to Hero is One to One
    journal_id = Column(Integer, ForeignKey('journal.id'))
    journal = relationship('Journal', back_populates='hero')

    # Many to one with Triggers, Each hero has many triggers.
    triggers = relationship('Trigger', back_populates='hero')

    # @eltran ... this probably won't work as the var will disappear on
    # database reload.
    # variable used for keeping track of clicked attributes on the user table
    clicked_user_attribute = ""

    @orm.validates('current_world')
    def validate_current_world(self, key, value):
        if 'map' == value.type:
            return value
        raise Exception("'current_world' Location type must be 'map' not '{}'."
                        "".format(value.type))

    def __init__(self, **kwargs):
        """Initialize the Hero object.

        Currently only accepts keywords. Consider changing this.
        Consider having some Non-null values?

        exp_percent is now updated by current_exp using a validator.
        max_exp should be assigned a value before current_exp.
        """

        self.attributes = Attributes()
        self.proficiencies = Proficiencies()
        self.abilities = Abilities()
        self.inventory = Inventory()
        self.journal = Journal()

        # Defaults will remain unchanged if no arguments are passed.
        self.age = 7
        self.archetype = None
        self.calling = None
        self.religion = None
        self.house = None

        self.experience_percent = 0
        self.experience = 0
        self.experience_maximum = 10

        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        self.basic_ability_points = 5
        self.archetype_ability_points = 0
        self.calling_ability_points = 0
        self.pantheonic_ability_points = 0

        self.attribute_points = 0
        self.proficiency_points = 0

        self.deepest_dungeon_floor = 0
        self.current_dungeon_floor = 0
        self.current_dungeon_floor_progress = 0
        self.random_encounter_monster = None

        # Time code
        self.timestamp = datetime.datetime.utcnow()
        self.last_login = ""
        self.login_alerts = "testing"

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.refresh_character(full=True)
        self.init_on_load()

    @orm.reconstructor
    def init_on_load(self):
        """Runs when the database is reload and at the end of __init__.
        """
        # I don't even know if this is supposed to be rebuilt? (Marlen)
        self.refresh_proficiencies()

        # resets experience_percent
        self.experience = self.experience

    @validates('experience')
    def validate_experience(self, key_name, current):
        # Update experience percent on experience change.
        try:
            self.experience_percent = round(
                current / self.experience_maximum, 2
            ) * 100
        except (TypeError, ZeroDivisionError):
            self.experience_percent = 0
        return max(current or 0, 0)

    # def not_yet_implemented(self):
    #     self.kill_quests = BaseDict()
    #     self.chest_equipped = []
    #     self.errands = []
    #     self.completed_quests = []
    #     self.completed_achievements = []
    #     self.bestiary = []
    #     self.wolf_kills = 0

    def refresh_proficiencies(self):
        for proficiency in self.proficiencies:
            proficiency.update(self)

    def refresh_character(self, full=False):
        self.refresh_proficiencies()
        if full:
            self.proficiencies.health.current = \
                self.proficiencies.health.maximum
            self.proficiencies.sanctity.current = \
                self.proficiencies.sanctity.maximum
            self.proficiencies.endurance.current = \
                self.proficiencies.endurance.maximum

    # I dont think this is needed if the validators are working?
    # I don't think I ever call this function and the bar seems
    # to be updating properly
    def update_experience_bar(self):
        self.experience_percent = round(
            self.experience / self.experience_maximum, 2) * 100

    # updates field variables when hero levels up
    def check_if_leveled_up(self):
        if self.experience >= self.experience_maximum:
            self.experience -= self.experience_maximum
            self.experience_maximum = math.floor(1.5 * self.experience_maximum)
            self.attribute_points += 1
            self.proficiency_points += 1
            self.basic_ability_points += 1
            self.archetype_ability_points += 1
            self.age += 1
            self.refresh_character(full=True)
            return True
        return False

    def gain_experience(self, amount):
        new_amount = amount * self.proficiencies.understanding.modifier
        # This will round the number weighted by its decimal
        # (so 1.2 has 20% chance of rounding up)
        new_amount = int(new_amount) + (random.random() < new_amount - int(
            new_amount))
        self.experience += new_amount
        level_up = self.check_if_leveled_up()

        # Return a variable in case you want to know how much experience you
        # just gained or if you leveled up
        return new_amount, level_up

    def equipped_items(self):
        try:
            return [item for item in self.inventory if item.is_equipped()]
        except TypeError as ex:
            if str(ex) == "'NoneType' object is not iterable":
                return []
            raise ex

    def non_equipped_items(self):
        return self.inventory.unequipped or []

    # Can we renamed this? I don't really get what it is from the name
    # (elthran) It's just temporary code while I amtesting notifications.
    # It will be scrapped soon.
    def page_refresh_character(self):
        self.quest_notification = None

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

    def check_daily_login_reward(self, time):
        if self.last_login == "":
            self.login_alerts += "First time logging in!"
            print("first time log in EVER (printed from game.py)")
        elif self.last_login != time[:10]:
            reward = 3
            self.login_alerts += "Thanks for logging in today! You earn " + str(
                reward) + " experience."
            self.experience += reward
            self.check_if_leveled_up()
            print("first time log in TODAY (printed from game.py)")
        else:
            print("you have already logged in today (printed from game.py)")
        self.last_login = time[:10]

    @validates('current_location')
    def validate_current_location(self, key, location):
        """Updates value of current_city on assignment.

        If current_location is a city ... set value of current_city as well.
        If not remove the value of current_city.
        """
        if location.type in ("cave", "town"):
            self.current_city = location
        return location

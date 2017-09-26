# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
# Author: Elthran B, Jimmy Zhang                                              #
# Email : jimmy.gnahz@gmail.com                                               #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

"""Objects used in the database and the game.

Suggestion: change name to game_objects.py
"""
import math
import random
import datetime
import pdb

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.orm import validates

from base_classes import Base, BaseDict
from attributes import Attributes
from abilities import Abilities
from proficiencies import Proficiencies
from inventory import Inventory


# TODO put this somewhere else, in a class, or just delete.
def convert_input(x: int):
    try:
        x = int(x)
    except:
        x = 0
    return x


class Game(object):
    def __init__(self, hero=None):
        self.hero = hero
        self.has_enemy = False
        self.global_chat = []  # I am not sure if this should goin database? Just very temporary chat log that all users can see

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.has_enemy = True

    def set_hero(self, hero):
        self.hero = hero


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
    inbox_alert = Column(Boolean)

    # Relationships
    # Each user can have one inbox. One to One (bidirectional).
    inbox_id = Column(Integer, ForeignKey('inbox.id'))
    inbox = relationship("Inbox", back_populates="user")

    # Many heroes -> one user
    heroes = relationship("Hero", order_by='Hero.character_name',
                          back_populates='user')

    def __init__(self, username, password, email='', timestamp=None, is_admin=False):
        """Create a new user object.

        The user gets special privileges if it is an admin.
        """

        self.inbox = Inbox()

        self.username = username
        self.password = password
        self.email = email
        self.timestamp = timestamp
        self.is_admin = is_admin
        self.inbox_alert = False


class Inbox(Base):
    __tablename__ = 'inbox'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Each inbox has a single user. One to One (bidirectional).
    user = relationship("User", uselist=False, back_populates='inbox')

    # Each inbox can have many sent messages One to Many
    sent_messages = relationship("Message", back_populates='sender',
                                 foreign_keys="[Message.sender_id]")
    received_messages = relationship("Message", back_populates='receiver',
                                     foreign_keys="[Message.receiver_id]")

    def get_sent_messages(self):
        """Return a list of all sent messages.

        These methods can be used for additional functionality
        such as sorting. NotImplemented!

        You can just use:
            user.inbox.sent_messages
        """
        return self.sent_messages

    def get_received_messages(self):
        """Return a list of all received messages.

        These methods can be used for additional functionality
        such as sorting. NotImplemented!

        You can just use:
            user.inbox.received_messages
        """
        return self.received_messages

    def send_message(self, receiver, content):
        """Create a message between the inbox's user and another user.

        A database commit must take place after this method or the
        message won't stay in existance?

        Basically ... the user is in a current session so when
        you add create a message (with bidirectional relationships)
        The Message is automatically added to both users inboxes.
        To save you need to commit.

        So in app.py you will call:
        user.inbox.send_message(other_user, content)
        database.update()
        """
        Message(self, receiver.inbox, content)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    # Relationships
    # Each user can send or receive multiple messages. One to Many (bi).
    sender_id = Column(Integer, ForeignKey('inbox.id'))
    sender = relationship("Inbox", back_populates="sent_messages",
                          foreign_keys="[Message.sender_id]")
    receiver_id = Column(Integer, ForeignKey('inbox.id'))
    receiver = relationship("Inbox", back_populates="received_messages",
                                         foreign_keys="[Message.receiver_id]")

    def __init__(self, sender, receiver, content):
        """A message between two users with some content.

        Both the sender and receiver are User objects.
        The content is a (formated?) string of text.
        """
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.unread = True
        # self.timestamp = timestamp


class Hero(Base):
    """Store data about the Hero/Character object.

    """
    __tablename__ = 'hero'

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Was nullable=False now it isn't. I hope that is a good idea.
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

    # Time code of when the (account?) was created
    timestamp = Column(DateTime)
    # Date of last login
    last_login = Column(String)

    login_alerts = Column(String)  # Testing messages when you are attacked or get a new message

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

    # Each current_city -> can be held by Many Heroes (bidirectional) (Town or Cave)
    # Maybe I should have a City object that extends Location that is the Ancestor for Town and Cave?
    # Location -> City -> (Town, Cave)
    city_id = Column(Integer, ForeignKey('location.id'))
    current_city = relationship(
        "Location", back_populates='heroes_by_city',
        foreign_keys='[Hero.city_id]')

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

    # Heroes to Quests.
    # Hero object relates to quests via the QuestPath object.
    # This path may be either active or completed, but not both.
    # Which establishes a manay to many relationship between quests and heroes.
    # QuestPath provides many special methods.
    quest_paths = relationship("QuestPath", back_populates='hero',
                               foreign_keys='[QuestPath.hero_id]')

    # Many to one with Triggers, Each hero has many triggers.
    triggers = relationship('Trigger', back_populates='hero')

    # @eltran ... this probably won't work as the var will disappear on
    # database relaod.
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

        # Defaults will remain unchanged if no arguments are passed.
        self.age = 7
        self.archetype = None
        self.calling = None
        self.religion = None
        self.house = None

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
            self.experience_percent = round(current / self.experience_maximum, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.experience_percent = 0
        return max(current or 0, 0)

    def not_yet_implemented(self):
        self.kill_quests = BaseDict()
        self.chest_equipped = []
        self.errands = []
        self.completed_quests = []
        self.completed_achievements = []
        self.bestiary = []
        self.wolf_kills = 0

    def refresh_proficiencies(self):
        for proficiency in self.proficiencies:
            proficiency.update(self)

    def refresh_character(self, full=False):
        self.refresh_proficiencies()
        if full:
            self.proficiencies.health.current = self.proficiencies.health.maximum
            self.proficiencies.sanctity.current = self.proficiencies.sanctity.maximum
            self.proficiencies.endurance.current = self.proficiencies.endurance.maximum

    # I dont think this is needed if the valifators are working? I don't think I ever call this funvtion and the bar seems to be updating properly
    def update_experience_bar(self):
        self.experience_percent = round(self.experience / self.experience_maximum, 2) * 100

    # updates field variables when hero levels up
    def level_up(self):
        if self.experience >= self.experience_maximum:
            self.experience -= self.experience_maximum
            self.experience_maximum = math.floor(1.5 * self.experience_maximum)
            self.attribute_points += 1
            self.proficiency_points += 1
            self.age += 1
            self.refresh_character(full=True)
            return True
        return False

    def gain_experience(self, amount):
        new_amount = amount * self.proficiencies.understanding.modifier
        new_amount = int(new_amount) + (random.random() < new_amount - int(new_amount))  # This will round the number weighted by its decimal (so 1.2 has 20% chance of rounding up)
        self.experience += new_amount
        level_up = self.level_up()
        return new_amount, level_up  # Return a variable in case you want to know how much experience you just gained or if you leveled up

    def equipped_items(self):
        try:
            return [item for item in self.inventory if item.is_equipped()]
        except TypeError as ex:
            if str(ex) == "'NoneType' object is not iterable":
                return []
            raise ex

    def non_equipped_items(self):
        return self.inventory.unequipped or []
        
    def page_refresh_character(self):  # Can we renamed this? I don't really get what it is from the name
        # (elthran) It's just temporary code while I amtesting notifications. It will be scrapped soon.
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

    @validates('current_location')
    def validate_current_location(self, key, location):
        """Updates value of current_city on assignment.

        If current_location is a city ... set value of current_city as well.
        If not remove the value of current_city.
        """
        if location.type in ("cave", "town"):
            self.current_city = location
        return location

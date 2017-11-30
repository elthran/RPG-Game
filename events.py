import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from base_classes import Base
import pdb
from pprint import pprint


class Event(Base):
    """Allow extra functions to occur when a specific state is reached.

    E.g. when the hero moves to the Blacksmith shop complete the Visit
    the Blacksmith quest.
    """
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    description = Column(String)
    when = Column(DateTime)
    hero_id = Column(Integer)

    def __init__(self, event_type, hero_id=None, description=None):
        """Build and describe a game event.

        Save this event to the database to have a living log of all the things
        the hero has done. In order. See timestamp/when.

        Tries to answer who, what, where, when, why, how.
        """
        self.type = event_type
        self.hero_id = hero_id
        self.description = description
        self.when = datetime.datetime.utcnow()

    # @classmethod
    # def from_js(cls, arg_dict):
    #     """Build an event object from passed JS/HTML data."""
    #     who = arg_dict.get('who', None, type=int)
    #     what = arg_dict.get('what', None, type=str)
    #     to_whom = arg_dict.get('to_whom', None, type=int)
    #     description = arg_dict.get('description', None, type=str)
    #     return cls(who, what, to_whom, description)

        # arg_dict.get('location', None, type=str)


class Trigger(Base):
    __tablename__ = 'trigger'

    id = Column(Integer, primary_key=True)
    event_name = Column(String)
    extra_info_for_humans = Column(String)
    completed = Column(Boolean)

    # relationships
    # One to Many with Heroes?
    hero_id = Column(Integer, ForeignKey('hero.id'))
    hero = relationship('Hero', back_populates='triggers')

    # One to many with Conditions. Each trigger might have many conditions.
    conditions = relationship('Condition', back_populates='trigger')

    def __init__(self, event_name, conditions, hero=None,
                 extra_info_for_humans=None):
        self.event_name = event_name
        self.conditions = conditions
        self.hero = hero
        self.extra_info_for_humans = extra_info_for_humans

    def link(self, hero):
        """Make this trigger accessible to the game engine for this hero.

        A trigger is considered active if it has a linked hero.
        """

        self.hero = hero

    def unlink(self):
        self.hero = None

    def evaluate(self):
        """Return true if all conditions are true.

        And set the completed flag.

        If they are set completed and return true.
        If not return false.
        """
        for condition in self.conditions:
            if not eval(condition.code, {'self': condition}):
                return False
        self.completed = True
        return self.completed


class Condition(Base):
    """A function that takes a python string and evaluates to boolean.

    Factory?

    hero.current_location.name == location.name
    """
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True)
    code = Column(String)

    # Relationships
    # Each trigger might have many conditions
    trigger_id = Column(Integer, ForeignKey('trigger.id'))
    trigger = relationship('Trigger', back_populates='conditions')

    # Each condition might be connected to a location. One to One.
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location')

    def __init__(self, hero_attribute, comparison, object_of_comparison):
        """Build a condition object.

        The default initial comparison is:
        self.trigger.hero._some_passed_attribute_name_.id
        NOTE: id is applied automatically this will need to be re-specced.
        """
        condition_attribute = object_of_comparison.__table__.name

        self.code = 'self.trigger.hero.{}.id {} self.{}.id'.format(
            hero_attribute, comparison, condition_attribute)

        # Should for example do:
        # self.location = the location I passed.
        setattr(self, condition_attribute, object_of_comparison)


class HandlerMixin(object):
    """Handler mixin to add trigger functionality to a class.

    The basic steps are:
        1. add completion trigger to __init__
        2. add link/try except.
        3. add relationship to trigger (back_population my be unneeded)
        4. add run_if_completed code.
        4a. unlink old trigger
        4b. do the thing that the whole party if for (e.g. quest.advance())
        4c. link next trigger if available.
    """
    id = Column(Integer, primary_key=True)

    # Add relationship to cls spec.
    @declared_attr
    def trigger_id(cls):
        return Column(Integer, ForeignKey('trigger.id'))

    @declared_attr
    def completion_trigger(cls):
        return relationship("Trigger")

    @declared_attr
    def trigger_is_completed(cls):
        return relationship(
            "Trigger",
            primaryjoin="and_({}.trigger_id==Trigger.id, "
                        "Trigger.completed==True)".format(cls.__name__))

    # This might be redundant.
    @declared_attr
    def hero_id(cls):
        return Column(Integer, ForeignKey('hero.id'))

    @declared_attr
    def hero(cls):
        return relationship("Hero")

    def activate(self, completion_trigger=None, hero=None):
        self.completion_trigger = completion_trigger
        self.hero = hero

        self.add_hero_to_trigger(hero)

    def add_hero_to_trigger(self, hero):
        """Add a hero object to be handled.

        Make Trigger available!
        Some kind of linkage between trigger and hero.
        Instantiated triggers must relate to a specific hero.
        """
        try:
            self.completion_trigger.link(hero)
        except AttributeError as ex:
            if str(ex) == "'NoneType' object has no attribute 'link'":
                pass
            else:
                raise ex

    def run_handler(self):
        """Deactivate trigger and run activation code.

        In this case ... unlink the trigger from the given quest
        and the advance the quest to the next stage.

        In theory ... this would bring the new trigger in to play
        through activation of a new quest? Or have I not set that up right?

        NOTE: must have overwritten the run_if_trigger_completed() method
        for this to work.
        """
        self.completion_trigger.unlink()
        next_trigger = self.run_if_trigger_completed()

        self.completion_trigger = next_trigger
        if next_trigger is not None:
            self.add_hero_to_trigger(self.hero)

    def run_if_trigger_completed(self):
        """A method that needs to be over ridden in the inherited class."""
        print("You were supposed to have over ridden this method.")
        print("(in class Handler -> run_if_trigger_completed)")
        print("Returns the next trigger to be hooked up.")
        raise Exception("Read the above message and maybe as me for help.")

if __name__ == "__main__":
    class SomeClassThatUsesTriggers(HandlerMixin, Base):
        __tablename__ = "some_class_that_uses_triggers"

        id = Column(Integer, primary_key=True)

        def __init__(self, kvar=None):
            self._init_handler()
            self.kvar = kvar
            print("My class that now uses triggers.")

    print("SomeClass before init:", repr(SomeClassThatUsesTriggers))
    sc = SomeClassThatUsesTriggers()
    print("SomeClass:", repr(sc))
    # print("SomeClass dir:", dir(sc))
    sc.pprint()



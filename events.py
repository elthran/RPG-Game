if __name__ == "__main__":
    import os
    os.system("python3 -m pytest -vv "
              "rpg_game_tests/test_conditions.py "
              "rpg_game_tests/test_conditions.py")
    exit()  # prevents code from trying to run file afterwards.

import datetime
import pdb
from pprint import pprint

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates, column_property, deferred
from sqlalchemy.ext.hybrid import hybrid_property

from base_classes import Base
from factories import TemplateMixin


class Event(Base):
    """Allow extra functions to occur when a specific state is reached.

    E.g. when the hero moves to the Blacksmith shop complete the Visit
    the Blacksmith quest.
    """
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    description = Column(String(200))
    when = Column(DateTime)
    hero_id = Column(Integer)

    def __init__(self, event_type, hero_id=None, description=None):
        """Build and describe a game event.

        Save this event to the database to have a living log of all the things
        the hero has done. In order. See timestamp/when.

        Tries to answer who, what, where, when, why, how.
        """

        # Trigger special names that should never be triggered by an Event.
        assert event_type not in ['Blank', 'Deactivated']

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


condition_to_trigger = Table('condition_to_trigger', Base.metadata,
    Column('condition_id', Integer, ForeignKey('condition.id',
                                               ondelete="SET NULL")),
    Column('trigger_id', Integer, ForeignKey('trigger.id',
                                             ondelete="SET NULL"))
)


class Condition(Base):
    """A function that takes a python string and evaluates to boolean.

    Factory?

    hero.current_location.name == location.name
    """
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True)

    hero_attribute = Column(String(50))
    comparison = Column(String(2))
    condition_attribute = Column(String(50))
    code = Column(String(200))

    # Relationships
    # Condition to Trigger is Many To Many
    triggers = relationship("Trigger", secondary=condition_to_trigger,
                            back_populates="conditions")

    # Each condition might be connected to a location. One to One.
    location_id = Column(Integer, ForeignKey('location.id',
                                             ondelete="CASCADE"))
    location = relationship('Location')

    def __init__(self, hero_attribute, comparison, object_of_comparison):
        """Build a condition object.

        The default initial comparison is:
        self.trigger.hero._some_passed_attribute_name_.id
        NOTE: id is applied automatically this will need to be re-specced.
        """

        self.hero_attribute = hero_attribute
        self.comparison = comparison

        self.condition_attribute = object_of_comparison.__table__.name

        self.code = """hero.{}.id {} self.{}.id""".format(
            hero_attribute, comparison, self.condition_attribute)

        # Should for example do:
        # self.location = the location I passed.
        setattr(self, self.condition_attribute, object_of_comparison)


class Trigger(TemplateMixin, Base):
    __tablename__ = 'trigger'

    id = Column(Integer, primary_key=True)
    event_name = Column(String(50))
    extra_info_for_humans = Column(String(200))
    completed = Column(Boolean)

    # relationships
    # One to Many with Heroes?
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship('Hero', back_populates='triggers')

    # One to many with Conditions. Each trigger might have many conditions.
    conditions = relationship("Condition", secondary=condition_to_trigger,
                              back_populates="triggers")

    def __init__(self, event_name, conditions, extra_info_for_humans=None,
                 template=True):
        self.event_name = event_name
        self.extra_info_for_humans = extra_info_for_humans
        self.completed = False
        self.conditions = conditions

        self.template = template

    def clone(self):
        """Clone this template.
        """
        if not self.template:
            raise Exception("Only use this method if obj.template == True.")

        return Trigger(self.event_name, self.conditions, self.extra_info_for_humans, template=False)

    def deactivate(self):
        """Deactivate this trigger.

        As it has no conditions it should never run.
        Maybe this should just delete the Trigger from the database?
        """
        self.event_name = "Deactivated"
        self.conditions = []
        self.extra_info_for_humans = None
        self.completed = False
        self.hero = None

    def evaluate(self):
        """Return true if all conditions are true.

        And set the completed flag.

        If they are set completed and return true.
        If not return false.

        NOTE: if there are _no_ conditions will evaluate to True!
        This basically means that when the first correct event occurs
        the Trigger will complete.
        e.g.
            equip_event spawns ... self.coditions = []
            ->
            self.completed = True
        """
        for condition in self.conditions:
            if not eval(condition.code, {'self': condition, 'hero': self.hero}):
                return False
        self.completed = True
        return self.completed  # mostly not used.


class Handler(Base):
    __tablename__ = 'handler'

    id = Column(Integer, primary_key=True)

    completed = Column(Boolean, default=False)

    # Add relationship to cls spec.
    trigger_id = Column(Integer, ForeignKey('trigger.id', ondelete="CASCADE"))

    trigger = relationship("Trigger", cascade="all, delete-orphan",
                            single_parent=True)

    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))

    hero = relationship("Hero", cascade="all, delete-orphan",
                            single_parent=True)

    @hybrid_property
    def trigger_is_completed(self):
        return self.trigger.completed

    # @declared_attr
    # def something(cls):
    #     return something

    def activate(self, trigger_template, hero):
        """Fully activate this Handler.

        This is used when all variables are available.
        This is needed to support templates as the template won't
        have any of the data until it is linked to a hero as a non-template
        object and then activated.

        The subclass should run:
            super().activate(some_local_trigger_template, hero)
        when all of these variables are available.

        NOTE: this is because the location of next triggers may vary between
        Handler sub classes as may the location of the hero object.
        """
        if self.completed:
            self.deactivate()
        else:
            self._hero = hero
            self.trigger = trigger_template.clone()
            self.trigger.hero = hero

    def deactivate(self):
        """Deactivate self and current trigger."""
        self.trigger.deactivate()
        self.trigger = None
        self._hero = None

    def run(self, trigger_template):
        """Deactivate or update the current trigger.

        NOTE: sub-class needs its own local version!
        Which should:
            1. run some local code -> which should have a possibility of
                triggering the 'completed' flag
            2. run super().run(maybe_a_trigger)

        i.e.
        self.advance()
        super().run(self.current_quest.trigger)
        """
        if self.completed:
            self.deactivate()
        elif trigger_template:
            self.trigger.deactivate()
            self.trigger = trigger_template.clone()
            print(self.trigger.id)


class HandlerMixin(object):
    """Handler mixin to add trigger functionality to a class.

    The basic steps are:
        1. add an 'activate' method to sub-class that can be run when a
            hero and trigger are available
        2. add some code that causes sub-class to 'complete'
        3.
    """
    # Add relationship to cls spec.
    @declared_attr
    def handler_id(cls):
        return Column(Integer, ForeignKey('handler.id', ondelete="CASCADE"))

    @declared_attr
    def handler(cls):
        return relationship("Handler", cascade="all, delete-orphan",
                            single_parent=True)

    @property
    def new_handler(self):
        return lambda: Handler()

    @declared_attr
    def completed(cls):
        return Column(Boolean, default=False)

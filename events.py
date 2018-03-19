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
from sqlalchemy.orm import backref
from sqlalchemy.orm import validates, column_property, deferred
from sqlalchemy.ext.hybrid import hybrid_property

from base_classes import Base


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


# trigger_to_hero = Table('trigger_to_hero', Base.metadata,
#     Column('hero_id', Integer, ForeignKey('hero.id', ondelete="SET NULL")),
#     Column('trigger_id', Integer, ForeignKey('trigger.id',
#                                              ondelete="SET NULL"))
# )


class Trigger(Base):
    __tablename__ = 'trigger'

    id = Column(Integer, primary_key=True)
    event_name = Column(String(50))
    extra_info_for_humans = Column(String(200))
    completed = Column(Boolean)

    # # Relationship
    # # Many to Many with Heroes.
    # heroes = relationship('Hero', secondary=trigger_to_hero,
    #                       back_populates='triggers')

    # One to many with Conditions. Each trigger might have many conditions.
    conditions = relationship("Condition", secondary=condition_to_trigger,
                              back_populates="triggers")

    def __init__(self, event_name, conditions, extra_info_for_humans=None):
        self.event_name = event_name
        self.extra_info_for_humans = extra_info_for_humans
        self.completed = False
        self.conditions = conditions


class Handler(Base):
    __tablename__ = 'handler'

    id = Column(Integer, primary_key=True)
    _master = Column(String(50))

    # Relationships
    trigger_id = Column(Integer, ForeignKey('trigger.id', ondelete="CASCADE"))
    trigger = relationship("Trigger")

    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero")  # Don't set cascade here or you will delete the hero object.

    @hybrid_property
    def trigger_is_completed(self):
        return self.evaluate()

    # @declared_attr
    # def something(cls):
    #     return something

    def __init__(self, master):
        """Create a new Handler object with the passed master.

        This is probably done by a class that sub-classes HandlerMixin and
        is using the self.new_hander() method.
        """
        self._master = master

    def activate(self, trigger, hero, completed=False):
        """Fully activate this Handler.

        This is used when all variables are available.
        This is needed to support templates as the template won't
        have any of the data until it is linked to a hero as a non-template
        object and then activated.

        The subclass should run:
            self.handler.activate(some_local_trigger, hero)
        when all of these variables are available.

        NOTE: this is because the location of next triggers may vary between
        Handler sub classes as may the location of the hero object.
        """

        if completed:
            self.deactivate()
        else:
            self.hero = hero
            self.trigger = trigger

    def deactivate(self):
        """Break trigger and hero relationship."""

        # self.trigger.heroes.remove(self.hero)
        # self.hero.triggers.remove(self.trigger)
        self.trigger = None
        self.hero = None

    def evaluate(self, event):
        """Return true if all Trigger conditions are true.

        NOTE: if there are _no_ conditions this will evaluate to True!
        This basically means that when the first correct event occurs
        the Trigger will complete.
        e.g.
            equip_event spawns ... self.coditions = []
            ->
            self.completed = True
        """
        if self.trigger.event_name != event.type:
            return False

        for condition in self.trigger.conditions:
            if not eval(condition.code, {'self': condition, 'hero': self.hero}):
                return False
        return True

    def run(self):
        """Run the object that controls this handler.

        This method must have been implement in a class that implements
        HandlerMixin. The master is the tablename of the object that
        this object was create by.

        This is to accommodate the fact that many objects can have handlers
        but I'm only interested in the one that created this object.
        """

        obj = getattr(self, self._master)
        if obj:
            obj.run()


class HandlerMixin(object):
    """Handler mixin to adds handler functionality to a class.

    The basic steps are:
        1. add and 'activate' method to sub-class that can be run when a
            hero and trigger are available

    e.g. In quests.py -> QuestPath I have built a journal class validator.
    @validates('journal')
    def activate_path(self, key, journal):
        assert self.template is False
        assert self.handler is None
        self.handler = self.new_handler()
        self.handler.activate(self.current_quest.trigger, journal.hero)
        return journal

        2. Add a run method to the subclass that is a stub to whatever the
        subclass actually does. This method needs to deactivate the handler
        appropriately.

    e.g. In quests.py -> QuestPath
    def advance(self):
        if self.completed:
            raise AssertionError("This path '{}' is completed and should have been deactivated!".format(self.name))

        if self.stage == self.stages-1:
            self.completed = True
            self.reward_hero(final=True)
            self.handler.deactivate()
            self.handler = None
        else:
            self.reward_hero()  # Reward must come before stage increase.
            self.stage += 1
            # Activate the latest trigger. This should deactivate the trigger if 'completed'.
            self.handler.activate(self.current_quest.trigger, self.journal.hero)

    def run(self):
        self.advance()
    """

    # Add relationship to cls spec.
    @declared_attr
    def handler_id(cls):
        return Column(Integer, ForeignKey('handler.id', ondelete="CASCADE"))

    # The backref here populates the list of handler mixin stubs.
    @declared_attr
    def handler(cls):
        return relationship("Handler", cascade="all, delete-orphan",
                            single_parent=True,
                            backref=backref(cls.__tablename__, uselist=False))

    @property
    def new_handler(self):
        return lambda: Handler(self.__tablename__)

    def run(self):
        raise NotImplementedError("You need to override this on the '{}' class.".format(self.__class__))

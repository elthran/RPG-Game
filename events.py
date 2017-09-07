"""
Event specification:
    -use the app.py <cmd> code.
    -transition to using a "game engine" kind of interface.
    -describe the action, person, place and thing.
    -some actions may not have a person. 
        e.g. "leaving town" would have an action "move", a place "current_location" and
            a thing "location_moving_to"
    -an event should occur whenever the User interacts with the game.
        i.e. mainly <button> and <a> tags.
    
Format:
    -<button class="command" name="consume" data="{{ item.id }}" data-function="functionName">
        AnyHTML you want.</button>
    -Where class="command" means this object runs command code.
    -Where data is the items database id or any other data you want to send.
        Id is just the simplest.
    -Where Consume is the buttons command identifier (the command function to run).

Old Format:
    -<button class="command" data="{{ item.id }}" data-function="functionName">Consume</button>
    -<button class="command" data="{{ item.id }}" onClick="remove(this)">Consume</button>
    -Where class="command" means this object runs command code.
    -Where data is the items database id.
    -Where Consume is the buttons command identifier (the command function to run).
    -Where data-function is the name of a function that can be sent data from the python
        code. This function runs after the python code returns a response. onClick
        does not. It runs first/or independently?
    -Where onClick is a local function to run. "this" is the button object itself.
        
This should be used to create and event object such that:
    >>> event = Event(request.args)
    
    >>> event
    Event<(action: 'buy', location: ['World', 'Thornwall', 'Blacksmith'],
        person: "Steve_The_Blacksmith", thing: "Medium Helmet")>
    >>> event.action
    'buy'

Events should active triggers .. or maybe they are the same thing.

#Usage of trigger/events with Quests
use triggers .... build a game engine :P
Thus to advance a quest you would spawn an event any time the hero did anything
and the engine would check the events data against each quest. Any quest that 
met the requirements of this trigger would advance.
eg. Trigger for "Talk to the Blacksmith" quest would be:
    t1 = Trigger(Location=Blacksmith, action=talk)
    t2 = Trigger(Location=Blacksmith, action=buy)
    t3 = Trigger((Location=Blacksmith, action=sell)
While the Quest object would look like
    q1 = Quest(name="Get aquainted with Blacksmith", descript="Talk to blacksmith",
        triggers=[t1], stage=1, next_quests=[q2], past_quests=[])
    q2 = Quest(name="Get aquainted with Blacksmith", descript="Buy or sell an item.",
        triggers=[t2, t3], stage=2, next_quests=[], past_quests=[q1])

A Trigger can have multiple actions. A Quest can have multiple Triggers. Only one needs to be met
to cause the Quest to advance? 
"""

# Response spec
"""
A response object could be:
respose type: do nothing
respose type: update, plus a list of id tags to update and their new values.
This might need to be written in JS.
"""

"""
Who, what, when, where, why, how?

who did what to whom,
when,
why?
how?

example:
quest completed:
    Hero (id=1, name=Marlen) completed quest (id=1, name=Blacksmith)
    at 15:50 (time=now())
    why?
    how - by going to talk to the Blacksmith (location id=14, name=Blacksmith)
    
    "How" is the "Trigger".
    
This would be triggered by event:
    Hero (id=0) talking/visiting location Blacksmith (id=14)
    at 15:50 (time=now()
    why?? - move/talk (event type) what == event type?
    how - hero.current_location.id == database.get_object_by_name('Location', 'Blacksmith').id
    
    Now how to I use truth value testing using conditions? Like WTF. I mean via strings?
    So like do I use compile/eval? or just compare ids always?
    or maybe store a type + id so that I compare attribute + type + id for all events?
    Assuming all events rely on Objects?
    
    And how do I know what events to test? I need some way to have a "Type" of event.
    Maybe that is the why? Or what kind of?
    Why == event type?
    why = 'move' would trigger all trigger = 'move' events
    trigger is now description!
"""
import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey
)
from sqlalchemy import orm
from sqlalchemy.orm import relationship

from base_classes import Base


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
        self.type = event_type
        self.hero_id = hero_id
        self.description = description
        self.when = datetime.datetime.utcnow()

    # @classmethod
    # def from_js(cls, arg_dict):
    #     who = arg_dict.get('who', None, type=int)
    #     what = arg_dict.get('what', None, type=str)
    #     to_whom = arg_dict.get('to_whom', None, type=int)
    #     description = arg_dict.get('description', None, type=str)
    #     return cls(who, what, to_whom, description)

        # arg_dict.get('location', None, type=str)


# class Handler:
#     def __init__(self, event, **kwargs):
#         """Save a compiled trigger object.
#
#         :param conditions: A complex python statement that must evaluate to
#          True or False!
#         Example:
#         ?Trigger("hero.current_location.name == 'Blacksmith'")
#         """
#         # self.condition = conditions
#         # self.code = compile(conditions, '<string>', 'exec')
#
#         self.event = event
#
#     def run(self, namespace={}):
#         if exec(self.code, namespace):
#             return event
#
#     def activate_if_true(self, event):
#         pass
#
#
# # I need a handler factory and then an actual handler function.
# def move_event_handler(self, hero, location):
#     if hero.current_location.name == location.name:
#         return True


class Trigger(Base):
    __tablename__ = 'trigger'

    id = Column(Integer, primary_key=True)
    event_name = Column(String)
    extra_info_for_humans = Column(String)
    completed = Column(Boolean)

    # relationships
    # Many to one with quests.
    quests = relationship("Quest", back_populates='completion_trigger')

    # One to Many with Heroes?
    hero_id = Column(Integer, ForeignKey('hero.id'))
    hero = relationship('Hero', back_populates='triggers')

    # One to many with Conditions. Each trigger might have many conditions.
    conditions = relationship('Condition', back_populates='trigger')

    def __init__(self, event_name, conditions, hero_id=None,
                 extra_info_for_humans=None):
        self.event_name = event_name
        self.conditions = conditions
        self.hero_id = hero_id
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
        self.trigger.hero._some_passed_attribute_name_
        """
        condition_attribute = object_of_comparison.__table__.name

        self.code = 'self.trigger.hero.{}.id {} self.{}.id'.format(
            hero_attribute, comparison, condition_attribute)

        # Should for example do:
        # self.location = the location I passed.
        setattr(self, condition_attribute, object_of_comparison)


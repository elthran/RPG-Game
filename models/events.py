import datetime

import sqlalchemy as sa
import sqlalchemy.orm

import models


class Event(models.Base):
    """Allow extra functions to occur when a specific state is reached.

    E.g. when the hero moves to the Blacksmith shop complete the Visit
    the Blacksmith quest.
    """
    type = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))
    when = sa.Column(sa.DateTime)
    hero_id = sa.Column(sa.Integer)

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


condition_to_trigger = sa.Table(
    'condition_to_trigger',
    models.Base.metadata,
    sa.Column('condition_id', sa.Integer, sa.ForeignKey('condition.id', ondelete="SET NULL")),
    sa.Column('trigger_id', sa.Integer, sa.ForeignKey('trigger.id', ondelete="SET NULL"))
)


class Condition(models.Base):
    """A function that takes a python string and evaluates to boolean.

    Factory?

    hero.current_location.name == location.name
    """
    hero_attribute = sa.Column(sa.String(50))
    comparison = sa.Column(sa.String(2))
    condition_attribute = sa.Column(sa.String(50))
    code = sa.Column(sa.String(200))

    # Relationships
    # Condition to Trigger is Many To Many
    triggers = sa.orm.relationship("Trigger", secondary=condition_to_trigger, back_populates="conditions")

    # Each condition might be connected to a location. One to One.
    location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id', ondelete="CASCADE"))
    location = sa.orm.relationship('Location')

    def __init__(self, hero_attribute, comparison, object_of_comparison):
        """Build a condition object.

        The default initial comparison is:
        self.trigger.hero._some_passed_attribute_name_.id
        NOTE: id is applied automatically this will need to be respecced.
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
#     sa.Column('hero_id', Integer, ForeignKey('hero.id', ondelete="SET NULL")),
#     sa.Column('trigger_id', Integer, ForeignKey('trigger.id',
#                                              ondelete="SET NULL"))
# )


class Trigger(models.Base):
    event_name = sa.Column(sa.String(50))
    extra_info_for_humans = sa.Column(sa.String(200))
    completed = sa.Column(sa.Boolean)

    # # Relationship
    # # Many to Many with Heroes.
    # heroes = sa.orm.relationship('Hero', secondary=trigger_to_hero,
    #                       back_populates='triggers')

    # One to many with Conditions. Each trigger might have many conditions.
    conditions = sa.orm.relationship("Condition", secondary=condition_to_trigger, back_populates="triggers")

    def __init__(self, event_name, conditions, extra_info_for_humans=None):
        self.event_name = event_name
        self.extra_info_for_humans = extra_info_for_humans
        self.completed = False
        self.conditions = conditions


class Handler(models.Base):
    _master = sa.Column(sa.String(50))

    # Relationships
    trigger_id = sa.Column(sa.Integer, sa.ForeignKey('trigger.id', ondelete="CASCADE"))
    trigger = sa.orm.relationship("Trigger")

    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship("Hero")  # Don't set cascade here or you will delete the hero object.

    # @sa.ext.hybrid.hybrid_property
    # def trigger_is_completed(self):
    #     return self.evaluate()

    # @declared_attr
    # def something(cls):
    #     return something

    def __init__(self, master):
        """Create a new Handler object with the passed master.

        This is probably done by a class that sub-classes HandlerMixin and
        is using the self.new_handler() method.
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


if __name__ == "__main__":
    import os
    os.system("python3 -m pytest -vv "
              "rpg_game_tests/test_conditions.py "
              "rpg_game_tests/test_conditions.py")

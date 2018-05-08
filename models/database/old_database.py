"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at:
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""
import hashlib
import base64
import importlib
import datetime
import random
import os
# Testing only


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
import sqlalchemy.exc

# Base is the initialize SQLAlchemy base class. It is used to set up the
# table metadata.
# Used like so in the __init__ method: Base.metadata.create_all(engine)
# What this actually means or does I have no idea but it is neccessary.
# And I know how to use it.
# !Important!: Base can only be defined in ONE location and ONE location ONLY!
from models import base_classes
# Internal game modules
from game import round_number_intelligently
from models.hero import Hero
from models.abilities import Ability
from models.locations import Location
from models.items import Item
from models.quests import QuestPath
from models.proficiencies import Proficiency
import prebuilt_objects

from services.session_helpers import scoped_session, safe_commit_session
import services

# Constants#
# UPDATE_INTERVAL = 3600  # One endurance per hour.
UPDATE_INTERVAL = 30 # One endurance per 30 seconds
Session = sessionmaker()


class EZDB:
    """Basic frontend for SQLAlchemy.

    This class allows you to use the old game methods with modern SQLAlchemy.
    At some point it may be worth using SQLAlchemy directly.

    All add_* methods should end with a commit!
    """
    def __init__(self, database="sqlite:///:memory:", debug=True,
                 testing=False):
        """Create a basic SQLAlchemy engine and session.

        Attribute "file_name" is used to find location of database for python.

        Hidden method: _delete_database is for testing and does what it
        sounds like it does :).
        """
        first_run = False
        server = database[0:database.rindex('/')]
        name = database.split('/').pop()
        self.filename = name

        engine = create_engine(
            server + "/?charset=utf8mb4", pool_recycle=3600, echo=debug)

        # Build a new database if this one doesn't exist.
        # Also set first_run variable!
        if not engine.execute("SHOW DATABASES LIKE '{}';".format(name)).first():
            print("Building database for first time!")
            first_run = True
            engine.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(name))

        # Select the database ... not sure if I need this.
        # Or if I should create a new engine instead ..
        engine = create_engine(
            database + "?charset=utf8mb4", pool_recycle=3600, echo=debug)

        base_classes.Base.metadata.create_all(engine, checkfirst=True)

        # Set up Session for this engine.
        Session.configure(bind=engine)
        self.Session = Session

        self.engine = engine
        self.session = self.Session()
        if first_run and not testing:
            self.add_prebuilt_objects()

    def add_prebuilt_objects(self):
        """Add all the predefined object into the database.

        If one is already there then ignore and continue.
        Note: each prebuilt_object must be a list.
        NOTE2: users must come first as it somehow gets built before it gets
        built if it doesn't?
        Maybe because .. it has a hero which has a current_world? So when
        current_world gets
        built then the user gets built too? Which may mean most of my code
        here is redundant
        and I only really need to build the users list?
        """

        # global prebuilt_objects
        # I can't remember why I need to reload this ...
        importlib.reload(prebuilt_objects)

        for obj_list in [
                prebuilt_objects.users,
                prebuilt_objects.game_worlds,
                # prebuilt_objects.all_abilities,
                prebuilt_objects.all_store_items,
                prebuilt_objects.all_marketplace_items,
                prebuilt_objects.all_quests,
                prebuilt_objects.all_specializations,
                prebuilt_objects.all_forums,
                prebuilt_objects.all_monsters]:
            for obj in obj_list:
                self.session.add(obj)
                if isinstance(obj, User):
                    obj.password = services.secrets.encrypt(obj.password)
                    obj.timestamp = EZDB.now()
                self.update()
        default_quest_paths = self.get_default_quest_paths()
        for hero in self.session.query(Hero).all():
            hero.journal.quest_paths = default_quest_paths
        self.update()

    def delete_item(self, item_id):
        """Delete an Item object from the database.
        """
        self.delete_object_by_id("Item", item_id)

    def delete_object_by_id(self, obj_name, obj_id):
        """Delete an object given its type and id.

        NOTE: the delete will not take effect until the session is flushed/
        commited/closed.
        """
        try:
            obj = globals()[obj_name]
        except IndexError:
            raise Exception(
                "Object name: '{}' is not an "
                "object, or has not been imported into "
                "'database' module yet.".format(obj_name))
        db_obj = self.session.query(obj).get(obj_id)
        if db_obj:
            self.session.delete(db_obj)
        else:
            raise IndexError(
                "No '{}' with id '{}' exists.".format(obj_name, obj_id))

    def get_object_by_id(self, obj_name, obj_id):
        """Return an object given its class name and id.

        Return error if name doesn't exist in global scope.
        obj = getattr(globals(), name)

        Name must be properly capitalized!
        """
        try:
            obj = globals()[obj_name]
        except IndexError:
            raise Exception(
                "Object name: '{}' is not an "
                "object, or has not been imported into "
                "'database' module yet.".format(obj_name))
        db_obj = self.session.query(obj).get(obj_id)
        if db_obj:
            return db_obj
        else:
            raise IndexError(
                "No '{}' with id '{}' exists.".format(obj_name, obj_id))

    def get_all_objects(self, obj_name, template=True):
        """Return all objects given a class name and template condition.

        Return error if name doesn't exist in global scope.
        obj = getattr(globals(), name)

        Name must be properly capitalized!

        NOTE: if object isn't template compatible it returns it anyways.
        Just ignore the template flag.
        """

        try:
            obj = globals()[obj_name]
        except IndexError:
            raise Exception(
                "Object name: '{}' is not an "
                "object, or has not been imported into "
                "'database' module yet.".format(obj_name))
        db_obj = None
        try:
            db_obj = self.session.query(obj).filter_by(template=template).all()
        except sqlalchemy.exc.InvalidRequestError as ex:
            if "has no property 'template'" in str(ex):
                db_obj = self.session.query(obj).all()
        if db_obj:
            return db_obj
        else:
            raise IndexError(
                "No '{}' objects exist.".format(obj_name))

    def get_learnable_abilities(self, hero):
        """Get all learnable abilities of a given hero."""
        return self.session.query(Ability).\
            filter_by(abilities_id=hero.abilities.id).\
            filter_by(locked=False).all()

    def get_object_by_name(self, obj_class_name, obj_name):
        """Retrieve an object from the database by name.

        And error will occur if the object name is not unique.
        Or if you specify an object that doesn't exist in the database.
        """
        obj = globals()[obj_class_name]
        return self.session.query(obj).filter_by(name=obj_name).one()

    def get_proficiency_by_id(self, prof_id):
        """Return a proficiency object by id."""
        return self.session.query(Proficiency).get(prof_id)

    def get_item_by_id(self, item_id):
        """Return an item from its ID.
        """
        return self.session.query(Item).get(item_id)

    @safe_commit_session
    def create_item(self, template_id):
        """Create a new item from a given template name.

        Autocommit using @safe_commit_session.
        """
        template = self.session.query(Item).get(template_id)
        item = template.clone()
        return item

    def get_random_item(self):
        """Return a new random item."""
        num_rows = self.session.query(Item).count()
        item_id = random.randint(1, num_rows)
        item = self.create_item(item_id)
        self.session.add(item)
        return item

    def get_all_users(self):
        """Return all Users order_by id.
        """
        return self.session.query(User).order_by(User.id).all()

    def get_all_heroes(self):
        """Return all Hero objects ordered by id."""
        return self.session.query(Hero).order_by(Hero.id).all()

    def get_ability_by_id(self, ability_id):
        """Return an ability from its ID."""
        return self.session.query(Ability).get(ability_id)

    def get_all_store_items(self):
        """Return all items in the database ordered by name.
        """
        return self.session.query(
            Item).filter_by(template=True).filter(
            Item.type != "Consumable").order_by(
            Item.name).all()

    def get_all_marketplace_items(self):
        """Return a list of all consumables in the marketplace.
        """
        return self.session.query(
            Item).filter_by(template=True).filter_by(type="Consumable").all()

    def get_default_world(self):
        """Get the default world for starting heroes.
        """
        return self.session.query(
            Location).filter_by(name="Htrae", type="map").first()

    def get_default_location(self):
        """Get the default location for starting heroes.
        """
        return self.session.query(
            Location).filter_by(name="Old Man's Hut", type="building").first()

    def get_default_quest_paths(self):
        """Return the quest that are applied to starting heroes.

        NOTE: This is a placeholder! The implementation should probably have
        a "is_default" flag for QuestPath objects.
        """
        return self.session.query(
            QuestPath).filter_by(
            is_default=True, template=True).all()

    @scoped_session
    def validate_reset(self, username, key):
        """Make sure the reset key matches.

        Additionally make sure you can't use a blank reset key.
        """
        user = self.session.query(User).filter_by(username=username).first()
        # For some reason the key get converted to binary then back
        # so it looks like "b'______'" instead of b'________' or
        # '_________'. I strip the "b'" of the start and "'" of the end.
        if user.reset_key and user.reset_key == key:
            return True
        return False

    def fetch_hero_by_username(self, username, character_name=None):
        """Return hero objected based on username_or_id and character_name.

        If no character_name is passed just return first hero.
        Note: Providing a username when you have the hero/character id is
        redundant.
        """
        user_id = self.get_user_id(username)
        if character_name is not None:
            return self.session.query(
                Hero).filter_by(
                user_id=user_id, character_name=character_name).first()
        return self.session.query(User).filter_by(id=user_id).first().heroes[0]

    def fetch_hero_by_id(self, hero_id):
        return self.session.query(Hero).get(hero_id)

    def fetch_sorted_heroes(self, attribute, descending=False):
        """Return a list of all heroes sorted by attribute.

        :param attribute: an attribute of the Hero object.
        :param descending: the desired direction for the sorted list
            ascending/descending
        :return: list sorted by attribute.

        NOTE: this code is not very flexible. If you tried to access
        hero.inventory.id it would not work.

        A more generic function might do:
        extended_attr, attr = attribute.split('.')
        join_attr = getattr(Hero, extended_attr)?
        self.session.query(Hero).join(join_attr).order_by(attr).all()

        NOTE: to order by descending:
        order_by(attribute + " desc")
        or
        order_by(desc(attribute))

        Former does not work for numbers

        https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
        """
        if '.' not in attribute:
            if descending:
                return self.session.query(Hero).order_by(desc(attribute)).all()
            else:
                return self.session.query(Hero).order_by(attribute).all()
        elif attribute.startswith('user'):
            _, attribute = attribute.split('.')
            if descending:
                return self.session.query(
                    Hero).join(Hero.user).order_by(desc(attribute)).all()
            else:
                return self.session.query(
                    Hero).join(Hero.user).order_by(attribute).all()
        else:
            raise Exception("Trying to access an attribute that this code"
                            " does not accommodate.")

    def update(self):
        """Commit, handle errors, close the session, open a new one.

        Provide a context manager type behavior for the session.
        See:
        http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
        """
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            self.session = self.Session()

    def add_object(self, obj):
        """Add an object to the database.

        Hides the session object. And the commit :P
        """
        self.session.add(obj)

    # def get_all_handlers_with_completed_triggers(self, hero):
    #     """Return all the handler objects with completed triggers.
    #
    #     This occurs when an event has happened that 'completed' a trigger
    #     for a given event.
    #     """
    #     objs = [QuestPath]
    #     handlers = []
    #     for obj in objs:
    #         handlers += self.session.query(obj).\
    #             filter(obj.trigger_is_completed).\
    #             filter(obj._hero_id == hero.id).all()
    #
    #     return handlers
    #
    # def get_all_triggers_by(self, event_name, hero_id):
    #     """Return all triggers for this hero that fit a given event."""
    #
    #     return self.session.query(
    #         Trigger).filter_by(
    #         event_name=event_name, hero_id=hero_id).all()
    #
    # def get_all_garbage_triggers(self):
    #     return self.session.query(Trigger).filter_by(event_name="Deactivated").all()

    def hero_has_quest_path_named(self, hero, name):
        """Returns True if hero has a ques_path of the given name.

        If hero has 2 quest_paths of the same name it throws an error.
        """
        quest = self.session.query(
            QuestPath).filter_by(
            name=name, journal_id=hero.journal.id).one_or_none()

        if quest:
            return True
        return False

    def get_quest_path_template(self, name):
        """Return the quest path template of the given name."""
        return self.session.query(
            QuestPath).filter_by(name=name, template=True).one()

    def update_time_all_heroes(self):
        """Run update_time on all hero objects.

        Consider moving the While True: + sleep somewhere else?
        Seems a little out of place here.
        """

        for hero in self.get_all_heroes():
            self.update_time(hero)

    # Marked for renaming as it effects Hero endurance as well as time.
    # Consider update_endurance_and_time()
    # Or update_game_clock
    # Or update_hero_clock
    @safe_commit_session
    def update_time(self, hero):
        """Update the game time clock of a specific Hero and endurance values.

        This increases the hero's endurance by the difference between past
        timestamp and current time.
        NOTE: Updates current timestamp in character table but only if has
        been incremented.
        Which may not be a good idea but ...

        Suggestion: Currently only affects the passed Hero, perhaps it
        should update all heroes?
        """

        endurance = hero.base_proficiencies['endurance']
        summed_endurance = hero.get_summed_proficiencies('endurance')
        stamina = hero.get_summed_proficiencies('stamina')
        stamina = round_number_intelligently(stamina.final)
        endurance.current = min(endurance.current + stamina, summed_endurance.final)

        health = hero.base_proficiencies['health']
        summed_health = hero.get_summed_proficiencies('health')
        regeneration = hero.get_summed_proficiencies('regeneration')
        regeneration = round_number_intelligently(regeneration.final)
        health.current = min(health.current + regeneration, summed_health.final)

        sanctity = hero.base_proficiencies['sanctity']
        summed_sanctity = hero.get_summed_proficiencies('sanctity')
        redemption = hero.get_summed_proficiencies('redemption')
        redemption = round_number_intelligently(redemption.final)
        sanctity.current = min(sanctity.current + redemption, summed_sanctity.final)

        for item in hero.equipped_items():
            item.affinity += 1

        # print("Hero {} updated on schedule.".format(hero.id))

    # def get_world(self, name):
    #     """Return WorldMap object from database using by name.
    #     """
    #     return self.session.query(WorldMap).filter_by(name=name).first()

    @scoped_session
    def add(self, objects=()):
        try:
            self.session.add_all(objects)
        except TypeError as ex:
            if "object is not iterable" in str(ex):
                self.session.add(objects)
            else:
                raise ex

    def _delete_database(self):
        """Deletes current database file.

        Use with caution, mainly for testing.
        """
        self.engine.execute(
            "DROP DATABASE IF EXISTS {};".format(self.filename))

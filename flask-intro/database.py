"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import sqlalchemy
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e

#Base is the initialize SQLAlchemy base class. It is used to set up the table metadata.
#Used like so in the __init__ method: Base.metadata.create_all(engine)
#What this actually means or does I have no idea but it is neccessary. And I know how to use it.
#!Important!: Base can only be defined in ONE location and ONE location ONLY!
import base_classes

import hashlib
import datetime
import os #Testing only

#Internal game modules
from game import User, Hero
from abilities import Ability
from locations import Location, WorldMap, Town, Cave
from items import Item
import complex_relationships
import prebuilt_objects

import pdb

import datetime


#Constants#
SECOND_PER_ENDURANCE = 10


class EZDB:
    """Basic frontend for SQLAlchemy.
    
    This class allows you to use the old game methods with modern SQLAlchemy.
    At some point it may be worth using SQLAlchemy directly.
    """
    def __init__(self, database='sqlite:///:memory:', debug=True, testing=False):
        """Create a basic sqlalchemy engine and session.
        
        Attribute "file_name" is used to find location of database for python.
        
        Hidden method: _delete_database is for testing and does what it sounds like it does :).
        """
        engine = create_engine(database, echo=debug)
        self.file_name = database[10:]
        
        base_classes.Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        
        self.engine = engine
        self.session = Session()
        if not testing:
            self.add_prebuilt_objects()
        
    def add_prebuilt_objects(self):
        """Add all the predefined object into the database.
        
        If one is already there then igore and continue.
        Note: each prebuilt_object must be a list.
        NOTE2: users must come first as it somehow gets built before it gets built if it doesn't?
        Maybe becuase .. it has a hero which has a current_world? So when current_world gets
        built then the user gets built too? Which may mean most of my code here is redundant
        and I only really need to build the users list?
        """
        for obj_list in [prebuilt_objects.users,
                prebuilt_objects.game_worlds,
                prebuilt_objects.all_abilities,
                prebuilt_objects.all_store_items,
                prebuilt_objects.all_marketplace_items,
                prebuilt_objects.testing_quests]:
            for obj in obj_list:
                try:
                    if type(User()) == type(obj):
                        obj.password = hashlib.md5(obj.password.encode()).hexdigest()
                    self.session.add(obj)
                    self.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    self.session.rollback()
                    
    def get_all_abilities(self):
        """Return all abilities in the database ordered by name.
        """

        return self.session.query(Ability).order_by(Ability.name).all()
        
        
    def get_all_store_items(self):
        """Not Implemented!
        """
        return []
        
        
    def get_all_marketplace_items(self):
        """Not Implemented!
        """
        return []
        
                    
    def get_default_world(self):
        """Get the default world for starting heroes.
        """
        return self.session.query(WorldMap).filter_by(name="Test_World2").first()
    
    
    def get_default_location(self):
        """Get the default location for starting heroes.
        """
        return self.session.query(Town).filter_by(name="Thornwall").first()
        
    def get_default_quests(self):
        """Get the default quests for starting heroes.
        
        Quests not yet implemented.
        NOTE: this query assumes that the test quests have 'test' in their name.
        Some other query could of course be used.
        """
        return []
        # return self.session.query(Quest).filter(Quest.name.like('%test'))
        
        
    def get_user_id(self, username):
        """Return the id of the user by username from the User's table.
        
        """
        try:
            return self.session.query(User).filter_by(username=username).first().id
        except AttributeError as e:
            print(e)
            if str(e) == "'NoneType' object has no attribute 'id'":
                return
            else:
                raise e
                
    def add_new_user(self, username, password, email=''):
        """Add a user to the username with a given a unique username and a password.
        
        The password is hashed.
        """
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.session.add(User(username=username, password=hashed_password, email=email))
        self.session.commit()
        
    def add_new_character(self, username_or_id, character_name=None, archetype=None):
        """Add a character with the specified archetype to a given user by id or username.
        
        Username is a unique field and is more human readable then using id's.
        """
        
        user = None
        if isinstance(username_or_id, int):
            user = self.session.query(User).filter_by(id=username_or_id).first()
        else:
            user = self.session.query(User).filter_by(username=username_or_id).first()
        self.session.add(Hero(name=character_name, archetype=archetype, user=user))
        self.session.commit()
    
    def validate(self, username, password):
        """Check if password if valid for user.
        """
        try:
            hashed_password = self.session.query(User).filter_by(username=username).first().password
            return  hashed_password == hashlib.md5(password.encode()).hexdigest()
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'password'":
                return
            else:
                raise e
        
        
    def fetch_hero(self, username_or_id=None, character_name_or_id=None):
        """Return live hero objected based on username_or_id and character_name.
        
        If no character_name is passed just return first hero.
        Note: Providing a username when you have the hero/character id is redundant.
        """
        
        if character_name_or_id and isinstance(character_name_or_id, int):
            if username_or_id:
                exit("Providing a username when you have the hero/character id is redundant.")
            return self.session.query(Hero).filter_by(id=character_name_or_id).first()
           
        if isinstance(username_or_id, str):
            username_or_id = self.get_user_id(username_or_id)
        
        if character_name_or_id:
            return self.session.query(Hero).filter_by(user_id=username_or_id, character_name=character_name_or_id).first()
        return self.session.query(User).filter_by(id=username_or_id).first().heroes[0]
    
    
    def update(self):
        """Commit current session.
        
        NOTE: update function is now mostly redundant! Only use on program exit or logout.
        When you edit the hero ... he stayes edited! Using any of the other methods will push him to database.
        """
        self.session.commit()
        
    def now():
        """Return current UTC time as datetime object in string form.
        
        NOTE: I am using UTC as we are working in different time zones and I think it might screw up otherwise.
        """
        return datetime.datetime.utcnow()
    
    #Marked for renaming as it effects Hero endurance as well as time.
    #Consider update_endurance_and_time()
    #Or update_game_clock
    #Or update_hero_clock
    def update_time(self, hero):
        """Update the game time clock of a specific Hero and endurance values.
        
        This increases the hero's endurance by the difference between past timestamp and current time.
        NOTE: Updates current timestamp in charater table but only if has been incremented.
        Which may not be a good idea but ...
        
        Suggestion: Currently only affects the passed Hero, perhaps it should update all heros?
        """
        timestamp = hero.timestamp
        time_diff = (EZDB.now() - timestamp).total_seconds()
        endurance_increment = int(time_diff / SECOND_PER_ENDURANCE)
        hero.current_endurance += endurance_increment
        
        if hero.current_endurance > hero.max_endurance:
            hero.current_endurance = hero.max_endurance
        
        if endurance_increment: #Only update if endurance has been incremented.
            hero.timestamp = EZDB.now()
        self.session.commit()
        
    def get_world(self, name):
        """Return WorldMap object from database using by name.
        """
        return self.session.query(WorldMap).filter_by(name=name).first()
    
    def _delete_database(self):
        """Deletes current database file.
        
        Use with caution, mainly for testing.
        """
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            #Ignore because the file has already been deleted.
            pass
        except PermissionError:
            pass
                            
                        
if __name__ == "__main__":
    import tests.database_tests.py
    
    
    
    

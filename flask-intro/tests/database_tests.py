from database import EZDB
from game import Hero, User
import locations
import complex_relationships
import datetime


"""
This program runs as a test suite for the EasyDatabase class when it is imported.
This modules is run using  :>python database_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""
import unittest

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db = EZDB('sqlite:///tests/test.db', debug=False)
    
    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()
            
    def rebuild_instance(self):
        """Tidy up and rebuild database instance.

        ... otherwise you may not be retrieving the actual data
        from the database only from memory.
        """
        
        self.db.session.commit()
        self.tearDown(delete=False)
        self.setUp()

    def test_initialize(self):
        """Check if database is actually created.
        
        This checks if init method throws any errors. And if a database is actually created.
        If it doesn't then the init is assumed to be valid.
        
        Consider adding a check to see if file of correct name is created?
        """
        self.assertIsNotNone(self.db)

    def test_add_new_user(self):
        """Check if new user is added to database.
        
        Check if database has a user called Marlen with a password of Brunner in it.
        
        Considering using:
        str_user = str(user)
        self.assertEqual(str(user2), str_user)
        
        This would allow for changes in the implementation. My current way is more 
        explicit though ...
        """
        self.db.add_new_user('Marlen', 'Brunner') #I should be able to add a bunch of users from a text file.
        user = self.db.session.query(User).filter_by(id=1).first()
        
        self.rebuild_instance()
        
        user2 = self.db.session.query(User).filter_by(id=1).first()
        self.assertEqual(str(user2), "<User(username='Marlen', password='8ced689733d29d5fd000c97bacd9b9d1', email='')>")


    def test_get_user_id(self):
        """Test if user is stored correctly.
        
        And can be retrieved by the databases own methods.
        """
        self.db.add_new_user('Marlen', 'Brunner')
        
        self.rebuild_instance()
        
        user_id = self.db.get_user_id("Marlen")
        self.assertEqual(user_id, 1)
        

    def test_add_new_character(self):
        """Check if characters can be created, saved and retrieved.

        
        Bug: Hero is not the same when returned.
            max_health is dropping from 10 to 5. Pre save?
        Then on load ... but before database close:
            current_health is staying at 10 but should be 5 (in theory).
        After database restarted:
            current_health is dropping from 10 to 5.
        This may be a Hero object bug. Will test.
        """
        self.db.add_new_user('Marlen', 'Brunner')
        user_id = 1
        character_name = "Haldon"
        self.db.add_new_character(user_id, "Haldon", "Wizard")
        self.db.add_new_character(user_id, "Haldon", "Welder")
        
        welder = self.db.session.query(User).filter_by(id=1).first().heroes[1]
        str_welder = str(welder)
        
        self.rebuild_instance()
        
        user2 = self.db.session.query(User).filter_by(id=1).first()
        # self.maxDiff = None
        exit("See docstring. Bug found, not cured.")
        self.assertEqual(str(user2.heroes[1]), str_welder)


def test_validate():
    """Test if the validate function in the Database class works.
    
    NOTE: my first real unit test!
    """
    db = set_up()
    username = 'Marlen'
    password = "Brunner"
    db.add_new_user(username, password)
    assert db.validate(username, password)
    tear_down(db)
    
def test_fetch_hero():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    db.add_new_character(1, "Haldon", "Welder")
    hero1 = db.fetch_hero("Marlen") #Username only
    hero2 = db.fetch_hero(1) #User id only
    hero3 = db.fetch_hero(character_name_or_id=1) #character id only, note providing username is redundant.
    hero4 = db.fetch_hero("Marlen", "Haldon") #Username and character name
    hero5 = db.fetch_hero(1, "Haldon") #User id and character name
    assert hero1.character_name == "Haldon"
    assert hero1 == hero2 == hero3 == hero4 == hero5
    tear_down(db)

def test_update():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = db.fetch_hero("Marlen", "Haldon")
    hero.archetype = "Welder"
    # db.update() #NOTE: update function is now redundant! Only use on program exit. 
    # The fetch_hero in the next line actually updates the hero in the database.
    assert db.fetch_hero(character_name_or_id=1).archetype == "Welder"
    tear_down(db)


def test_update_time():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = db.fetch_hero(character_name_or_id=1)
    hero.timestamp -= datetime.timedelta(seconds=11)
    oldtime = hero.timestamp 
    db.update_time(hero)
    assert hero.current_endurance == 1 #May fail on very slow machines do too slow code execution.
    tear_down(db)
    

if __name__ == '__main__':
    unittest.main()

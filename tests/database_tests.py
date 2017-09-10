import unittest
import datetime
from pprint import pformat

from database import EZDB
from game import User
import locations

"""
This program runs as a test suite for the EasyDatabase class when it is
    imported.
This modules is run using  :>python database_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)

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
        
        This checks if init method throws any errors. And if a database is
        actually created.
        If it doesn't then the init is assumed to be valid.
        
        Consider adding a check to see if file of correct name is created?
        """
        self.assertIsNotNone(self.db)

    def test_add_new_user(self):
        """Check if new user is added to database.
        
        Check if database has a user called Marlen with a password
        of Brunner in it.
        
        Considering using:
        str_user = str(user)
        self.assertEqual(str(user2), str_user)
        
        This would allow for changes in the implementation. My current way
        is more explicit though ...
        """
        # I should be able to add a bunch of users from a text file.
        self.db.add_new_user('Marlen', 'Brunner')
        user = self.db.session.query(User).get(1)
        str_user = user.pretty_str()
        self.rebuild_instance()

        user2 = self.db.session.query(User).get(1)
        self.assertEqual(user2.pretty_str(), str_user)

    def test_get_user_id(self):
        """Test if user is stored correctly.
        
        And can be retrieved by the databases own methods.
        """
        self.db.add_new_user('Marlen', 'Brunner')

        self.rebuild_instance()

        user_id = self.db.get_user_id("Marlen")
        self.assertEqual(user_id, 1)

    def test_add_new_hero_to_user(self):
        """Check if characters can be created, saved and retrieved.
        """
        self.maxDiff = None
        self.db.add_new_user('Marlen', 'Brunner')
        user = self.db.get_object_by_id("User", 1)
        self.db.add_new_hero_to_user(user)
        self.db.add_new_hero_to_user(user)
        wizard = user.heroes[0]
        wizard.name = "Haldon"
        wizard.archetype = "Wizard"
        wizard_str = wizard.pretty_str()

        welder = user.heroes[1]
        welder.name = "Haldon"
        welder.archetype = "Welder"
        welder_str = welder.pretty_str()
        self.rebuild_instance()

        user2 = self.db.get_object_by_id("User", 1)
        wizard2 = self.db.get_object_by_id("Hero", 1)
        welder2 = self.db.get_object_by_id("Hero", 2)
        self.assertEqual(wizard2.pretty_str(), wizard_str)
        self.assertEqual(welder2.pretty_str(), welder_str)

    def test_validate(self):
        """Test if the validate function in the Database class works.

        NOTE: my first real unit test!
        """

        username = 'Marlen'
        password = "Brunner"
        self.db.add_new_user(username, password)

        self.rebuild_instance()
        self.assertTrue(self.db.validate(username, password))

    def test_get_object_by_id(self):
        self.db.add_new_user('Marlen', 'Brunner')
        marlen = self.db.get_object_by_id("User", 1)
        self.db.add_new_hero_to_user(marlen)
        wizard = marlen.heroes[0]
        wizard.name = "Haldon"
        wizard.archetype = "Wizard"
        wizard_str = wizard.pretty_str()
        marlen_str = marlen.pretty_str()

        self.rebuild_instance()
        marlen2 = self.db.get_object_by_id("User", 1)
        wizard2 = self.db.get_object_by_id("Hero", 1)

        self.assertEqual(marlen2.pretty_str(), marlen_str)
        self.assertEqual(wizard2.pretty_str(), wizard_str)

    def test_update(self):
        """Test update function.
        
        NOTE: update function is now mostly redundant!
            Only use on program exit.
        The fetch_hero line actually updates the hero in the database.
        Consider running commit on program update as well. 
        """
        self.db.add_new_user('Marlen', 'Brunner')
        user = self.db.get_object_by_id("User", 1)
        self.db.add_new_hero_to_user(user)
        hero = user.heroes[0]
        hero.name = "Haldon"
        hero.archetype = "Welder"
        self.db.update()
        user_str = user.pretty_str()
        hero_str = hero.pretty_str()

        self.rebuild_instance()
        user2 = self.db.get_object_by_id("User", 1)
        hero2 = user2.heroes[0]
        self.assertEqual(user2.pretty_str(), user_str)
        self.assertEqual(hero2.pretty_str(), hero_str)

    def test_update_time(self):
        """May fail on very slow machines do too slow code execution.
        """
        self.db.add_new_user('Marlen', 'Brunner')
        user = self.db.get_object_by_id("User", 1)
        self.db.add_new_hero_to_user(user)
        hero = self.db.get_object_by_id("Hero", 1)
        hero.timestamp -= datetime.timedelta(seconds=11)
        self.db.update_time(hero)


if __name__ == '__main__':
    unittest.main()

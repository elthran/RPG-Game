'''
This program runs as a test suite for the game.py module when it is imported.
This modules is run using  :>python game_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial https://docs.python.org/3.6/library/unittest.html
'''
from models.game import Hero

from database import EZDB
from models.basic_types import BaseItem, BaseDict

import unittest

class BaseItemTestCase(unittest.TestCase):
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
            
    def test_base_item_init(self):
        item = BaseItem('*', 0)
        item.key = 'a'
        item.value = 1
        self.db.session.add(item)
        self.db.session.commit()
        str_item = str(item)
        
        self.rebuild_instance()
        item2 = self.db.session.query(BaseItem).filter_by(id=1).first()
        self.assertEqual(str_item, str(item2))
        self.assertEqual(item2.key, 'a')
        self.assertEqual(item2.value, 1)

class BaseDictTestCase(unittest.TestCase):
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
            
    def test_base_dict_init(self):
        d = BaseDict({'*': 0})
        d.remove('*')
        
        d['a'] = 1
        self.db.session.add(d)
        self.db.session.commit()
        str_dict = str(d)
        
        self.rebuild_instance()
        d2 = self.db.session.query(BaseDict).filter_by(id=1).first()
        self.assertEqual(str_dict, str(d2))
        self.assertEqual(d2['a'], 1)
        
    
    def test_muti_value(self):
        d = BaseDict({'a': 1, 'b': 2, 'c': 3})
        
        self.db.session.add(d)
        self.db.session.commit()
                
        self.rebuild_instance()
        d2 = self.db.session.query(BaseDict).filter_by(id=1).first()
        d2['b'] += 4
        str_dict = str(d2)
        self.db.session.commit()
        
        self.rebuild_instance()
        d3 = self.db.session.query(BaseDict).filter_by(id=1).first()        
        self.assertEqual(str_dict, str(d3))
        
    def test_unique_element(self):
        d = BaseDict({'a': 1, 'b': 2, 'c': 3})
        d2 = BaseDict({'a': 1, 'b': 2, 'c': 3})
        self.db.session.add(d)
        self.db.session.add(d2)
        self.db.session.commit()
        
        self.rebuild_instance()
        d = self.db.session.query(BaseDict).filter_by(id=1).first()
        d2 = self.db.session.query(BaseDict).filter_by(id=2).first()
        d['c'] = 8
        self.db.session.commit()
        
        self.rebuild_instance()
        d = self.db.session.query(BaseDict).filter_by(id=1).first()
        d2 = self.db.session.query(BaseDict).filter_by(id=2).first()
        self.assertNotEqual(d['c'], d2['c'])
        

class BaseStringOfTestCase(unittest.TestCase):
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
            
    def test_max_recursion_str(self):
        """Prove that the a hero object can be converted to a string without infinte recursion.
        
        As Hero decends from Base it loads the Base __str__ method.
        This currently results in max recursion depth. Which is lame because it was so nice before.
        """
        hero = Hero(name="Haldon")
        self.db.session.add(hero)
        self.db.session.commit()

        str_hero = str(hero)       
        self.rebuild_instance()
        
        hero2 = self.db.session.query(Hero).filter_by(name="Haldon").first()
        # self.maxDiff = None
        self.assertEqual(str_hero, str(hero2))

from database import EZDB
from game import Hero
from quests import Quest
import complex_relationships

import unittest
import pdb

class QuestsTestCase(unittest.TestCase):
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

    def test_Quest_init(self):
        """Check if object is created, storeable and retrievable.
        """
        quest = Quest("Get Acquainted with the Blacksmith", "Go talk to the blacksmith.")
        self.db.session.add(quest)
        self.db.session.commit()
        str_quest = str(quest)
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        self.assertEqual(str_quest, str(quest2))
        
    def test_if_relationship_is_a_set(self):
        self.assertEqual('Not built', '')
        
    def test_active_heroes(self):
        self.assertEqual('Not built', '')
        
    def test_completed_heroes(self):
        self.assertEqual('Not built', '')
        
    def test_hero_cannot_be_active_and_completed_at_the_same_time(self):
        self.assertEqual('Not built', '')        
        
    def test_heroes_relationship(self):
        self.assertEqual('Not built', '')
        
    def test_past_quests(self):
        self.assertEqual('Not built', '')
        
    def test_next_quests(self):
        self.assertEqual('Not built', '')
        
    def test_relationship_with_self(self):
        self.assertEqual('Not built', '')
        
    def test_advance_quest(self):
        self.assertEqual('Not built', '')

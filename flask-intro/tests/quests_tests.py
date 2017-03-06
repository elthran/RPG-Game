from database import EZDB
from game import Hero
from quests import Quest
import complex_relationships

import unittest
import pdb

class QuestsTestCase(unittest.TestCase):
    def setUp(self):
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        self.quest = Quest("Get Acquainted with the Blacksmith", "Go talk to the blacksmith.")
    
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
        """Proves that even if you add an item to a relationship twice only one copy will exist.
        
        NOTE: You must do a commit after adding each element or you will get an error
        of "added the same object twice." With the commit in between it seems to work.
        """
        quest = Quest("Get Acquainted with the Blacksmith", "Go talk to the blacksmith.")
        quest2 = Quest("Get Acquainted with the Blacksmith", "Buy your first item.", reward_xp=7)
        self.db.session.add(quest)
        self.db.session.add(quest2)
        
        #Append first time.
        quest.next_quests.append(quest2)
        self.db.session.commit()
        str_quest = str(quest)
        
        #Add again while already there.
        quest.next_quests.append(quest2)
        self.db.session.commit()
        
        str2_quest = str(quest)
        
        self.rebuild_instance()
        quest3 = self.db.session.query(Quest).filter_by(id=1).first()
        
        self.assertEqual(str_quest, str2_quest)
        self.assertEqual(str_quest, str(quest3))
        
        
    def test_active_heroes(self):
        hero = Hero(name="Haldon")
        self.quest.activate(hero)
        self.db.session.add(self.quest)
        self.db.session.commit()
        str_quest = str(self.quest)
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        
        self.assertEqual(str_quest, str(quest2))
        
    def test_completed_heroes(self):
        hero = Hero(name="Haldon")
        self.quest.activate(hero)
        self.db.session.add(self.quest)
        self.db.session.commit()
        len_active = len(self.quest.active_heroes)
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        len_active2 = len(quest2.active_heroes)
        
        hero = quest2.active_heroes[0]
        quest2.mark_completed(hero)
        self.db.session.commit()
        len_active3 = len(quest2.active_heroes)
        len_completed = len(quest2.completed_heroes)
        
        self.rebuild_instance()
        quest3 = self.db.session.query(Quest).filter_by(id=1).first()
        len_active4 = len(quest3.active_heroes)
        len_completed2 = len(quest3.completed_heroes)
       
        self.assertEqual(len_active, 1)
        self.assertEqual(len_active2, 1)
        self.assertEqual(len_active3, 0)
        self.assertEqual(len_active4, 0)
        self.assertEqual(len_completed, 1)
        self.assertEqual(len_completed2, 1)
        
    def test_hero_cannot_be_active_and_completed_at_the_same_time(self):
        hero = Hero(name="Haldon")
        self.quest.activate(hero)
        self.db.session.add(self.quest)
        self.db.session.commit()
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        
        with self.assertRaises(AssertionError):
            quest2.completed_heroes.append(quest2.active_heroes[0])
        
        quest2.mark_completed(quest2.active_heroes[0])   
        self.db.session.commit()
            
        with self.assertRaises(AssertionError):
            quest2.active_heroes.append(quest2.completed_heroes[0])    
                
        
    def test_heroes_relationship(self):
        """Test if hero/quest backref is set up properly.
        """
        self.assertEqual('Not built', '')
        
    def test_past_quests(self):
        self.assertEqual('Not built', '')
        
    def test_next_quests(self):
        self.assertEqual('Not built', '')
        
    def test_relationship_with_self(self):
        self.assertEqual('Not built', '')
        
    def test_advance_quest(self):
        self.assertEqual('Not built', '')

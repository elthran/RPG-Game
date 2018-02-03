import unittest
import pdb

from database import EZDB
from game import Hero
from quests import Quest, QuestPath


class QuestsTestCase(unittest.TestCase):
    def setUp(self):
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        self.quest = Quest("Get Acquainted with the Blacksmith",
                           "Go talk to the blacksmith.")
    
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
        """Check if object is created, storable and retrievable.
        """
        quest = Quest("Get Acquainted with the Blacksmith",
                      "Go talk to the blacksmith.")
        self.db.session.add(quest)
        self.db.session.commit()
        str_quest = str(quest)
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        self.assertEqual(str_quest, str(quest2))

    def test_if_relationship_is_a_set(self):
        """Test if relationship can contain duplicates.
        
        NOTE: You must do a commit after adding each element or you will
        get an error of "added the same object twice." With the commit
        in between it seems to work.
        """
        quest = Quest("Get Acquainted with the Blacksmith",
                      "Go talk to the blacksmith.")
        quest2 = Quest("Get Acquainted with the Blacksmith",
                       "Buy your first item.", reward_experience=7)
        self.db.session.add(quest)
        self.db.session.add(quest2)
        
        # Append first time.
        quest.next_quests.append(quest2)
        self.db.session.commit()
        str_quest = str(quest)
        
        # Add again while already there.
        quest.next_quests.append(quest2)
        self.db.session.commit()
        
        str2_quest = str(quest)
        
        self.rebuild_instance()
        quest3 = self.db.session.query(Quest).filter_by(id=1).first()
        
        self.assertEqual(str_quest, str2_quest)
        self.assertEqual(str_quest, str(quest3))
     
    def test_quest_path_adding(self):
        hero = Hero(name="Haldon")
        quest = self.quest
        
        # self.quest.quest_paths.append(QuestPath(self.quest, hero))
        # same as:
        # QuestPath(quest, hero)
        quest.add_hero(hero)
        
        self.db.session.add(quest)
        self.db.session.commit()
        str_quest = str(quest)
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        
        self.assertEqual(str_quest, str(quest2))

    def test_active_heroes(self):
        hero = Hero(name="Haldon")
        hero2 = Hero(name="Elthran")
        hero3 = Hero(name="Not_Active")
        quest = self.quest
        QuestPath(quest, hero)
        QuestPath(quest, hero2)
        QuestPath(quest, hero3, active=False)
        
        self.db.session.add(quest)
        self.db.session.commit()
        str_active_heroes = str([
            'hero.name={}'.format(hero.name)
            for hero in QuestPath.active_heroes(quest)])
         
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        
        str_active_heroes2 = str([
            'hero.name={}'.format(hero.name)
            for hero in QuestPath.active_heroes(quest2)])
        
        self.assertEqual(str_active_heroes, str_active_heroes2)
        self.assertEqual(str_active_heroes,
                         "['hero.name=Haldon', 'hero.name=Elthran']")
        
    def test_completed_heroes(self):
        hero = Hero(name="Haldon")
        hero2 = Hero(name="Elthran")
        hero3 = Hero(name="Not_Active")
        quest = self.quest
        QuestPath(quest, hero)
        QuestPath(quest, hero2)
        QuestPath(quest, hero3, active=False)
        
        self.db.session.add(quest)
        self.db.session.commit()
        len_active = len(QuestPath.active_heroes(quest))
        len_completed = len(QuestPath.completed_heroes(quest))    
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        active_heroes = QuestPath.active_heroes(quest2)
        
        quest2.mark_completed(active_heroes[0])
        quest2.mark_completed(active_heroes[1])
        self.db.session.commit()
        len_active2 = len(QuestPath.active_heroes(quest2))
        len_completed2 = len(QuestPath.completed_heroes(quest2))
        
        self.assertEqual(len_completed, 0)
        self.assertEqual(len_active, 2)
        self.assertEqual(len_completed2, 2)
        self.assertEqual(len_active2, 0)
        
    def test_hero_cannot_be_active_and_completed_at_the_same_time(self):
        quest = self.quest
        hero = Hero(name="Haldon")
        quest.add_hero(hero)
        self.db.session.add(self.quest)
        self.db.session.commit()
        
        self.rebuild_instance()
        quest2 = self.db.session.query(Quest).filter_by(id=1).first()
        
        active_state = quest2.quest_paths[0].active
        completed_state = quest2.quest_paths[0].completed
        quest2.mark_completed(QuestPath.active_heroes(quest2)[0])   
        active_state2 = quest2.quest_paths[0].active
        completed_state2 = quest2.quest_paths[0].completed
        
        self.assertTrue(active_state)
        self.assertTrue(completed_state2)
        self.assertFalse(active_state2)
        self.assertFalse(completed_state)

    @unittest.skip("Not built.")
    def test_path_advance(self):
        self.assertEqual('Not built', '')

    # def test_heroes_relationship(self):
        # """Test if hero/quest backref is set up properly.
        # """
        # self.assertEqual('Not built', '')
        
    # def test_past_quests(self):
        # self.assertEqual('Not built', '')
        
    # def test_next_quests(self):
        # self.assertEqual('Not built', '')
        
    # def test_relationship_with_self(self):
        # self.assertEqual('Not built', '')
        
    # def test_advance_quest(self):
        # self.assertEqual('Not built', '')

from database import EZDB
import abilities
from game import Hero
from abilities import Ability, Archetype_Ability, Class_Ability, Religious_Ability
import complex_relationships

import unittest
import pdb

class AbilitiesTestCase(unittest.TestCase):
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

    def test_Ability_init(self):
        """Check if object is created, storeable and retrievable.
        """
        ability = Ability("Determination", 5, "Increases Endurance by 3 for each level.")
        self.db.session.add(ability)
        self.db.session.commit()
        str_ability = str(ability)
        
        self.rebuild_instance()
        ability2 = self.db.session.query(Ability).filter_by(name='Determination').first()
        self.assertEqual(str_ability, str(ability2))
        
    def test_add_hero(self):
        ability = Ability("Determination", 5, "Increases Endurance by 3 for each level.")
        hero = Hero(name="Haldon")
        self.db.session.add(ability)
        ability.add_hero(hero)
        self.db.session.commit()
        str_ability = str(ability)
        
        self.rebuild_instance()
        ability2 = self.db.session.query(Ability).filter_by(name='Determination').first()
        self.assertEqual(str_ability, str(ability2))
        
    def test_requirements(self):
        """Test if abilities can have a relationship with other abilities.
        
        I don't know if this should in fact be a Many to Many?
        """
        ability = Ability("Determination", 5, "Increases Endurance by 3 for each level.")
        ability2 = Ability("Salubrity", 5, "Increases Health by 4 for each level.")
        ability3 = Archetype_Ability("Sagacious", 10, "Increases experience gained by 5% for each level.")
        self.db.session.add_all([ability, ability2, ability3])
        ability.requirements += [ability2, ability3]
        self.db.session.commit()
        str_ability = str(ability)
        
        self.rebuild_instance()
        ability4 = self.db.session.query(Ability).filter_by(name='Determination').first()
        self.assertEqual(str_ability, str(ability4))
        
    def test_update_stats(self):
        """Test if update_stats works.
        
        update_stats runs when hero object is reloaded. Or it can be run
        manually. See docstring for correct usage.
        """
        ability = Ability("Determination", 5, "Increases Endurance by 3 for each level.")
        hero = Hero(name="Haldon")
        self.db.session.add(ability)
        ability.add_hero(hero)
        self.db.session.commit()
        endurance = hero.max_endurance
        for ability in hero.abilities:
            ability.update_stats(hero)
        endurance2 = hero.max_endurance
        
        self.rebuild_instance()
        hero2 = self.db.session.query(Hero).filter_by(name='Haldon').first()
        self.assertEqual(endurance + 3, hero2.max_endurance)
        self.assertEqual(endurance2, hero.max_endurance)
        
    def test_cast_gain_gold(self):
        """Test hero spell casting.
        
        NOTE: hero sanctity depends on Divinity and Wisdom.
        then you must run update_secondary_attributes and then refresh_character.
        Casting "Gain gold to test" costs sanctity and produces gold.
        This is a basic example spell but the logic should work for all spells.
        
        Considering: Sublcass Ability into Spell and have Spells hold
        the necessary extra attributes and logic.
        """
        spell = Ability("Gain Gold to Test", 5,
            "Gain 3 gold for each level, every time you actvate this ability.",
            castable=True, cost=2)
        hero = Hero(name="Haldon")
        hero.primary_attributes['Divinity'] = 10
        hero.primary_attributes['Wisdom'] = 10
        hero.update_secondary_attributes()
        hero.refresh_character()
        self.db.session.add(spell)
        hero.abilities += [spell]
        
        self.db.session.commit()
        
        gold_before_cast = hero.gold
        sanctity_before_cast = hero.current_sanctity
        spell.cast(hero)
        gold_after_cast = hero.gold
        sanctity_after_cast = hero.current_sanctity
        
        self.rebuild_instance()
        hero2 = self.db.session.query(Hero).filter_by(name='Haldon').first()
        self.assertEqual(gold_before_cast + 3, gold_after_cast)
        self.assertEqual(gold_after_cast, hero2.gold)
        self.assertEqual(sanctity_before_cast - 2, sanctity_after_cast)
        self.assertEqual(sanctity_after_cast, hero2.current_sanctity)
        
    def test_prebuilt_objects(self):
        self.assertEqual('Not built', '')

        
if __name__ == '__main__':
    unittest.main()

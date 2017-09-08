import unittest
import pdb

from database import EZDB
from game import Hero
from abilities import (
    Abilities, Ability, Archetype_Ability, Class_Ability, Religious_Ability
)
# I don't know why it says this is unused ... maybe we can make it
# obsolete? I mean you did say it made so of the variables hard to understand.
# It is _very_ important. And must always go last.
import complex_relationships


class AbilitiesTestCase(unittest.TestCase):
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

    def test_Abilities_init(self):
        """Check if object is created, storeable and retrievable.
        """

        abilities = Abilities()
        self.db.session.add(abilities)
        self.db.session.commit()
        str_abilities = abilities.pretty

        self.rebuild_instance()
        abilities2 = self.db.session.query(
            Abilities).filter_by(id=1).first()
        self.assertEqual(str_abilities, abilities2.pretty)

    @unittest.skip("Not built")
    def test_add_hero(self):
        ability = Ability("Determination", 5,
                          "Increases Endurance by 3 for each level.")
        hero = Hero(name="Haldon")
        self.db.session.add(ability)
        ability.add_hero(hero)
        self.db.session.commit()
        str_ability = str(ability)
        
        self.rebuild_instance()
        ability2 = self.db.session.query(
            Ability).filter_by(name='Determination').first()
        self.assertEqual(str_ability, str(ability2))

    @unittest.skip("Not built")
    def test_requirements(self):
        """Test if abilities can have a relationship with other abilities.
        
        I don't know if this should in fact be a Many to Many?
        """
        ability = Ability("Determination", 5,
                          "Increases Endurance by 3 for each level.")
        ability2 = Ability("Salubrity", 5,
                           "Increases Health by 4 for each level.")
        ability3 = Archetype_Ability(
            "Sagacious", 10,
            "Increases experience gained by 5% for each level."
        )
        self.db.session.add_all([ability, ability2, ability3])
        ability.requirements += [ability2, ability3]
        self.db.session.commit()
        str_ability = str(ability)
        
        self.rebuild_instance()
        ability4 = self.db.session.query(
            Ability).filter_by(name='Determination').first()
        self.assertEqual(str_ability, str(ability4))

    @unittest.skip("Not built")
    def test_update_stats(self):
        """Test if update_stats works.
        
        update_stats runs when hero object is reloaded. Or it can be run
        manually. See docstring for correct usage.
        """
        ability = Ability("Determination", 5,
                          "Increases Endurance by 3 for each level.")
        hero = Hero(name="Haldon")
        self.db.session.add(ability)
        ability.add_hero(hero)
        self.db.session.commit()
        endurance = hero.proficiencies.endurance.maximum
        for ability in hero.abilities:
            ability.update_stats(hero)
        endurance2 = hero.proficiencies.endurance.maximum
        
        self.rebuild_instance()
        hero2 = self.db.session.query(Hero).filter_by(name='Haldon').first()
        self.assertEqual(endurance + 3, hero2.proficiencies.endurance.maximum)
        self.assertEqual(endurance2, hero.proficiencies.endurance.maximum)

    @unittest.skip("Not built")
    def test_cast_gain_gold(self):
        """Test hero spell casting.
        
        NOTE: hero sanctity depends on Divinity and Wisdom.
        then you must run update_secondary_attributes and then
        refresh_character.
        Casting "Gain gold to test" costs sanctity and produces gold.
        This is a basic example spell but the logic should work for all spells.
        
        Considering: Sublcass Ability into Spell and have Spells hold
        the necessary extra attributes and logic.
        """
        spell = Ability("Gain Gold to Test", 5,
                        "Gain 3 gold for each level, every time you "
                        "activate this ability.",
                        castable=True, cost=2)
        hero = Hero(name="Haldon")
        hero.attributes.divinity.level = 10
        hero.attributes.wisdom.level = 10
        hero.refresh_character()
        self.db.session.add(spell)
        hero.abilities += [spell]
        
        self.db.session.commit()
        
        gold_before_cast = hero.gold
        sanctity_before_cast = hero.proficiencies.sanctity.current
        spell.cast(hero)
        gold_after_cast = hero.gold
        sanctity_after_cast = hero.proficiencies.sanctity.current
        
        self.rebuild_instance()
        hero2 = self.db.session.query(Hero).filter_by(name='Haldon').first()
        self.assertEqual(gold_before_cast + 3, gold_after_cast)
        self.assertEqual(gold_after_cast, hero2.gold)
        self.assertEqual(sanctity_before_cast - 2, sanctity_after_cast)
        self.assertEqual(sanctity_after_cast, hero2.current_sanctity)

    @unittest.skip("Not built")
    def test_prebuilt_objects(self):
        self.assertEqual('Not built', '')

        
if __name__ == '__main__':
    unittest.main()

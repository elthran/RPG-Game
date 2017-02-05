'''
This program runs as a test suite for the game.py module when it is imported.
This modules is run using  :>python game_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial https://docs.python.org/2/library/unittest.html
'''
from base_classes import Base
from test_all import pr
from database import EZDB
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property
from game import Hero
import complex_relationships

import pdb

def setup():
    return EZDB('sqlite:///tests/test.db', debug=False)

def teardown(database):
    database.session.close()
    database.engine.dispose()
    database._delete_database()

def testPrimaryAttributes():
    """Test hero primary_attributes

    Tests increment
    Tests that two heroes primary_attributes are not the same object (that one was anoying).
    Tests that list iteration works.
    Tests that data is retrieved as an ordered list when printing.
    Tests this from a saving/loading perspective as well.
    
    NOTE: actual data order is dictionary random.
    NOTE: query should occur using a new database object or it will simply return the old object
    without actually pulling it from the database. I need to fix this in my other test suites.
    """
    
    hero = Hero()
    pal = hero.primary_attributes
    pal["Strength"] += 3
    assert pal["Strength"] == 4
    
    hero2 = Hero()
    pal2 = hero2.primary_attributes
    assert id(pal) != id(pal2)    
    
    for attribute in pal2:
        pal2[attribute] += 1
    assert str(pal2) == "{'Agility': 2, 'Charisma': 2, 'Divinity': 2, 'Fortitude': 2, 'Fortuity': 2, 'Perception': 2, 'Reflexes': 2, 'Resilience': 2, 'Strength': 2, 'Survivalism': 2, 'Vitality': 2, 'Wisdom': 2}"
    
    #Test save/load
    db = setup()
    hero3 = Hero(name="Haldon")
    db.session.add(hero3)
    db.session.commit()
    
    db2 = setup()
    hero4 = db2.session.query(Hero).filter_by(name='Haldon').first()
    
    assert hero3.primary_attributes == hero4.primary_attributes
    teardown(db)
    teardown(db2)

def testKillQuests():
    db = setup()
    hero = Hero(name="Haldon")
    hero.kill_quests['Kill a wolf'] = "Find and kill a wolf!"
    db.session.add(hero)
    db.session.commit()
    
    db2 = setup()
    hero2 = db2.session.query(Hero).filter_by(name='Haldon').first()
    assert hero.kill_quests == hero2.kill_quests
    teardown(db)
    teardown(db2)
    
    
    
def run_all():
    """Run all tests in the module.

    The test currently only fail if the code is broken ... not if the info is invalid.
    I hope to use an assert statement at some point in each test to make sure the output is correct as well.
    """
    testPrimaryAttributes()
    testKillQuests()
    
    print("All game_tests passed. No Errors, yay!")

run_all()

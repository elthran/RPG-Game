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
from game import PrimaryAttributeList

import pdb

def testPrimaryAttributeList():
    
    pal = PrimaryAttributeList()
    pal["Strength"] += 3
    assert pal["Strength"] == 4
    
    pal = PrimaryAttributeList()
    # pdb.set_trace()
    for attribute in pal:
        pal[attribute] += 1
    assert repr(pal) == "<PrimaryAttributeList(id=None, agility=2, charisma=2, divinity=2, fortitude=2, fortuity=2, perception=2, reflexes=2, resilience=2, strength=2, survivalism=2, vitality=2, wisdom=2, hero_id=None)>"
    
    #NOTE: I should test this from a saving/loading perspective as well as it may not hold up.
    
    
def run_all():
    """Run all tests in the module.

    The test currently only fail if the code is broken ... not if the info is invalid.
    I hope to use an assert statement at some point in each test to make sure the output is correct as well.
    """
    testPrimaryAttributeList()
    
    print("All game_tests passed. No Errors, yay!")
    exit()

run_all()

"""
This test suite should be run each time I make changes to the main game code before I push the changes.
This should ensure that my changes didn't break anything.

This modules is run using  :>python test_all.py

It then imports all of the unit tests for each module in the game.
These test suites should run on import.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""

def pr(*args):
    return print(args[0], repr(args[-1]))
    

def dict_diff(left, right):
    """Tell if two dicts are the same, return differences.
    
    Use: print(dict_diff(hero.__dict__, hero2.__dict__))
    NOTE: not a test ... just used for testing.
    """
    diff = dict()
    diff['left_only'] = set(left) - set(right)
    diff['right_only'] = set(right) - set(left)
    diff['different'] = {k for k in set(left) & set(right) if left[k]!=right[k]}
    return diff
    

import tests.game_tests
import tests.locations_tests

# import tests.database_tests

# import tests.app_tests

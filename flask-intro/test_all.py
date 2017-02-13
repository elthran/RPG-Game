"""
This test suite should be run each time I make changes to the main game code before I push the changes.
This should ensure that my changes didn't break anything.

This modules is run using  :>python test_all.py

It then imports all of the unit tests for each module in the game.
These test suites should run on import.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""

import unittest
import os


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
    
def get_test_cases_in_module(module):
    """Return a reference to each TestCase object in a given module.
    """
    return [getattr(module, member) for member in vars(module) if "TestCase" in member]
    
def get_test_case_list_from_modules(modules):
    """Return all the TextCases in a list of modules.
    """
    test_list = []
    for module in modules:
        test_list.extend(get_test_cases_in_module(module))
    return test_list

def build_suite_of_all_tests(*modules):
    """Return a suite of all tests in all TestCases in all passed modules.
    
    Pass in a bunch of mondules ... the output should be similar to a suite
    created for each TestCase in each Modules. This will allow the user
    to run the entire test suite from one place.
    """
    caseList = []
    for testCase in get_test_case_list_from_modules(modules):
        testSuite = unittest.defaultTestLoader.loadTestsFromTestCase(testCase)
        caseList.append(testSuite)
 
    return unittest.TestSuite(caseList)
   


if __name__ == "__main__":
    from tests import locations_tests, game_tests#, database_tests
       
    all_tests_suite = build_suite_of_all_tests(game_tests, locations_tests)
    
    all_tests_runner = unittest.TextTestRunner(verbosity=2)
    all_tests_runner.run(all_tests_suite)
    

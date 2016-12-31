'''
This program runs as a test suite for the EasyDatabase class when it is imported.
This modules is run using  :>python game_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial https://docs.python.org/2/library/unittest.html
'''

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import game
import unittest

class TestStringMethods(unittest.TestCase):

    def test_convert_input(self):
        self.assertEqual(game.convert_input(2), 2)
        self.assertEqual(game.convert_input("2"), 2)
        self.assertEqual(game.convert_input("string"), 0)

    # Code given by the tutorial
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    # Code given by the tutorial	
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

def set_up():
    test_hero = Hero()
    test_hero.name = "Unknown"
    test_hero.gold = 5000
    test_hero.update_secondary_attributes()
    test_hero.refresh_character()
			
if __name__ == '__main__':
    unittest.main()

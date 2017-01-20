'''
This program runs as a test suite for the EasyDatabase class when it is imported.
This modules is run using  :>python game_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial https://docs.python.org/2/library/unittest.html
'''

def testPrimaryAttributesList():
    exit("""
    primary_attributes["Strength"] += 3 -> Default of strenght is None until object is saved! Then it is 1.
    So this is like saying None += 3 which fails
    
    primary_attributes["Strength"] = 3 -> Does not support item assignment.
    See @hybrid_property and @value.setter!
    """)
    
def run_all():
    """Run all tests in the module.

    The test currently only fail if the code is broken ... not if the info is invalid.
    I hope to use an assert statement at some point in each test to make sure the output is correct as well.
    """
    testPrimaryAttributesList()
    
    print("All game_tests passed. No Errors, yay!")

run_all()

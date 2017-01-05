from database import EasyDatabase
from saveable_objects import EZDB, User, pr
from game import Hero
import time


"""
This program runs as a test suite for the EasyDatabase class when it is imported.
This modules is run using  :>python database_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""

def set_up():
    #return EasyDatabase('static/test_database.db')
    return EZDB('sqlite:///static/test_database.db', debug=False)

def tear_down(database):
    database.session.close()
    database.engine.dispose()
    database._delete_database()

def test__init():
    """Note yet implemented: Check if database is actually created.
    
    This checks if init method throws any errors.
    If it doesn't then the init is assumed to be valid.
    """
    db = set_up()
    # print(db)
    assert db #looks like it is supposed to ... that will be hard ... :P
    tear_down(db)

def test_add_new_user():
    """Check if new user is added at to database.
    
    Check if database has a user called Marlen with a password of Brunner in it.
    """
    db = set_up()
    db.add_new_user('Marlen', 'Brunner') #I should be able to add a bunch of users from a text file.
    user = db.session.query(User).filter_by(id=1).first()
    assert user.username == 'Marlen'
    tear_down(db)


def test_get_user_id():
    """Test if user is stored correctly.
    """
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    user_id = db.get_user_id("Marlen")
    assert user_id == 1
    tear_down(db)

def test_add_new_character():
    """Check if character that is created has a user_id of 1.
    """
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    user_id = 1
    character_name = "Haldon"
    db.add_new_character(user_id, "Haldon", "Wizard")
    db.add_new_character(user_id, "Haldon", "Welder")
    user = db.session.query(User).filter_by(id=1).first()
    assert user.heroes[1].archetype == 'Welder'
    tear_down(db)

def test_validate():
    """Test if the validate function in the Database class works.
    
    NOTE: my first real unit test!
    """
    db = set_up()
    username = 'Marlen'
    password = "Brunner"
    db.add_new_user(username, password)
    assert db.validate(username, password)
    tear_down(db)
    
def test_fetch_hero():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    db.add_new_character(1, "Haldon", "Welder")
    hero1 = db.fetch_hero("Marlen") #Username only
    hero2 = db.fetch_hero(1) #User id only
    hero3 = db.fetch_hero(character_name_or_id=1) #character id only, note providing username is redundant.
    hero4 = db.fetch_hero("Marlen", "Haldon") #Username and character name
    hero5 = db.fetch_hero(1, "Haldon") #User id and character name
    assert hero1.character_name == "Haldon"
    assert hero1 == hero2 == hero3 == hero4 == hero5
    tear_down(db)

def test_update():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = db.fetch_hero("Marlen", "Haldon")
    hero.archetype = "Welder"
    # db.update() #NOTE: update function is now redundant! Only use on program exit. 
    # The fetch_hero in the next line actually updates the hero in the database.
    assert db.fetch_hero(character_name_or_id=1).archetype == "Welder"
    tear_down(db)
    
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

def test_update_time():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = db.fetch_hero(character_name_or_id=1)
    oldtime = hero.current_time
    sleep(11)
    db.update_time(hero)
    print(hero.current_time - oldtime)
    exit("testing in database_tests update_time")
    assert 1 #not implemented
    # tear_down(db)
    

def run_all():
    """Run all tests in the module.

    The test currently only fail if the code is broken ... not if the info is invalid.
    I hope to use an assert statement at some point in each test to make sure the output is correct as well.
    """
    test__init()
    test_add_new_user()
    test_get_user_id()
    test_add_new_character()
    test_validate()
    test_fetch_hero()
    test_update()
    test_update_time()
    
    print("No Errors, yay!")

run_all()

from base_classes import Base
import locations
from locations import Location, Cave, Town, World_Map
import complex_relationships
from sqlalchemy import inspect
from test_all import pr
from database import EZDB
import os

"""
This program runs as a test suite for the locations module when it is imported.
This modules is run using  :>python locations_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""

def set_up():
    return EZDB('sqlite:///tests/test.db', debug=False)

def tear_down(database):
    database.session.close()
    database.engine.dispose()
    database._delete_database()

def test_adjacent_locations():
    db = set_up()
    home = Location(name="Home")
    # mapper = inspect(Location)
    # for e in mapper.relationships:
        # print(e)
    # exit()
    db.session.add(home)
    db.session.commit()
    home2 = db.session.query(Location).filter_by(name='Home').first()
    home2.adjacent_locations = [2, 3, 4]
    db.session.add(home2)
    db.session.commit()
    home3 = db.session.query(Location).filter_by(name='Home').first()
    assert home.adjacent_locations == home2.adjacent_locations == home3.adjacent_locations == [2, 3, 4]
    assert home == home2 == home3
    tear_down(db)
    
def test_town():
    db = set_up()
    town = Town(name="Thornwall")
    db.session.add(town)
    db.session.commit()
    town2 = db.session.query(Town).filter_by(name="Thornwall").first()
    assert town == town2
    tear_down(db)
    
def test_cave():
    db = set_up()
    cave = Cave(name="Creepy Cave")
    db.session.add(cave)
    db.session.commit()
    cave2 = db.session.query(Cave).filter_by(name="Creepy Cave").first()
    assert cave == cave2
    tear_down(db)
    
def test_world_map():
    db = set_up()
    map = World_Map(name="Picatanin")
    # print(map)
    # exit()
    db.session.add(map)
    db.session.commit()
    map2 = db.session.query(World_Map).filter_by(name="Picatanin").first()
    print(map2)
    assert map == map2
    tear_down(db)
    
def test_add_world_map():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = db.fetch_hero(character_name_or_id=1)
    print(hero.current_world)
    print(type(locations.game_worlds[0]))
    hero.current_world = locations.game_worlds[0]
    print(hero.current_world)
    exit("test_add_world_map")
    assert 0
    tear_down(db)
    
def run_all():
    db = set_up()
    try:
        test_adjacent_locations()
        test_town()
        test_cave()
        test_world_map()
    finally:
        tear_down(db)
    # test_add_world_map()
    print("All locations_tests passed. No Errors, yay!")
    
run_all()

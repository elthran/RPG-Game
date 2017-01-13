from base_classes import Base
import locations
from locations import Location, Cave, Town, World_Map
import complex_relationships
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


def not_used():
    test_locations = []
    test_locations2 = []

    '''
     +Test Map Visual Representation:
     +
     +0 ---- 1 ---- 2 (Creepy Cave)
     +| \    |
     +|  \   |
     +|   \  |
     +3    \ |
     +|     5 ---- 6 ---- 7
     +|    / \     |
     +4   /   \    |
     +   /     \   |
     +  /       \  |
     + /         \ |
     +8           9
     +
     +
     +Thornwall at location 5
     +Creepy Cave at location 2
     +'''
     
    for i in range(0, 12):
        test_location = Location(name=("location " + str(i)),id=i)
        test_locations2.append(test_location)

    test_locations2[5] = Town(name="Thornwall", id=5)
    test_locations2[2] = Cave(name="Creepy cave", id=2)

    """ Define all connections

    #------------------------------------
    #
    #  Initializing Game Worlds
    #  (To be moved to a common
    #   init function later)
    #
    #------------------------------------
    TEST_WORLD_ID = 999 # ...

    test_locations = []

    '''
    Test Map Visual Representation:

    0 ---- 1 ---- 2 (Creepy Cave)
    | \    |
    |  \   |
    |   \  |
    3    \ |
    |     5 ---- 6 ---- 7
    |    / \     |
    4   /   \    |
       /     \   |
      /       \  |
     /         \ |
    8           9


    Thornwall at location 5
    Creepy Cave at location 2
    '''

    for i in range(0,10):
        test_location = Location("location " + str(i),i)
        test_locations.append(test_location)

    test_locations[5] = Town("Thornwall", 5, "Test_World")
    test_locations[2] = Cave("Creepy cave", 2, "Test_World")

    # Define all connections
    test_locations[0].adjacent_locations = [1, 3, 5]
    test_locations[1].adjacent_locations = [0, 2, 5]
    test_locations[2].adjacent_locations = [1]
    test_locations[3].adjacent_locations = [0, 4]
    test_locations[4].adjacent_locations = [3]
    test_locations[5].adjacent_locations = [0, 1, 6, 8, 9]
    test_locations[6].adjacent_locations = [5, 7, 9]
    test_locations[7].adjacent_locations = [6]
    test_locations[8].adjacent_locations = [5]
    test_locations[9].adjacent_locations = [5, 6]"""

    test_locations2[1].adjacent_locations = [2, 3, 4]
    test_locations2[2].adjacent_locations = [1, 5]
    test_locations2[3].adjacent_locations = [1, 4]
    test_locations2[4].adjacent_locations = [1, 3, 5, 7]
    test_locations2[5].adjacent_locations = [2, 4, 6, 8]
    test_locations2[6].adjacent_locations = [5, 9, 10]
    test_locations2[7].adjacent_locations = [4, 8]
    test_locations2[8].adjacent_locations = [5, 7, 9]
    test_locations2[9].adjacent_locations = [6, 8]
    test_locations2[10].adjacent_locations = [6]

    game_worlds = [World_Map(name="Test_World2", current_location_id=5, all_map_locations=test_locations2)]
    return game_worlds
    
def test_location_all():
    game_worlds = setup()
    test_locations2 = game_worlds[0].all_map_locations
    map = game_worlds[0]
    # for location in map.all_map_locations:
        # print(location.name, location.location_type, location.adjacent_locations)

    cave = test_locations2[2]
    town = test_locations2[5]
    # print(map.caves)
    # print(cave.location_world)
    # print(map.towns)
    # print(town.location_world)
        
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    # session.add(map)

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
    test_adjacent_locations()
    test_town()
    test_cave()
    test_world_map()
    # test_add_world_map()
    print("All locations_tests passed. No Errors, yay!")
    
run_all()

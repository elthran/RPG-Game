
# from locations import Base
from locations import Location
from locations import World_Map, Town, Cave
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
This program runs as a test suite for the locations module when it is imported.
This modules is run using  :>python locations_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""



def setup():
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

    game_world = [World_Map(name="Test_World2", current_location_id=5, all_map_locations=test_locations2)]
    return game_worlds
    
    
    test_locations2 = locations.test_locations2
    map = locations.game_worlds[0]
    for location in map.all_map_locations:
        print(location.name, location.location_type, location.adjacent_locations)

    cave = test_locations2[2]
    town = test_locations2[5]
    print(map.caves)
    print(cave.location_world)
    print(map.towns)
    print(town.location_world)
        
    # engine = create_engine('sqlite:///:memory:', echo=True)
    # Base.metadata.create_all(engine, checkfirst=True)
    # Session = sessionmaker(bind=engine)
    # session = Session()

def run_all():
    setup()
    
run_all()

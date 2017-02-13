from base_classes import Base
from database import EZDB
import locations
from locations import Location, Cave, Town, WorldMap, Display
from game import Hero
import complex_relationships
import prebuilt_objects
import pdb

"""
This program runs as a test suite for the locations.py module when it is imported.
This modules is run using  :>python locations_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""

import unittest

class LocationTestCase(unittest.TestCase):
    def setUp(self):
        self.db = EZDB('sqlite:///tests/test.db', debug=False)

    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()

    def test_adjacent_locations(self):
        home = Location(name="Home")
        self.db.session.add(home)
        self.db.session.commit()
        adjacent_locations = str(home.adjacent_locations)
        
        self.tearDown(delete=False)
        self.setUp()
        
        home2 = self.db.session.query(Location).filter_by(name='Home').first()
        home2.adjacent_locations = [2, 3, 4]
        self.db.session.add(home2)
        self.db.session.commit()
        adjacent_locations2 = str(home2.adjacent_locations)
        
        self.tearDown(delete=False)
        self.setUp()
        home3 = self.db.session.query(Location).filter_by(name='Home').first()
        self.assertEqual(adjacent_locations, '[]')
        self.assertEqual(adjacent_locations2, '[2, 3, 4]')
        self.assertEqual(home3.adjacent_locations, [2, 3, 4])
        
    
    def test_town(self):
        town = Town(name="Thornwall")
        self.db.session.add(town)
        self.db.session.commit()
        
        self.tearDown(delete=False)
        self.setUp()
        town2 = self.db.session.query(Town).filter_by(name="Thornwall").first()
        self.assertEqual(str(town2), "<Town(id=1, name='Thornwall', type='Town', map=None, adjacent_locations=[], display=None>")
        
    
    def test_cave(self):
        cave = Cave(name="Creepy Cave")
        self.db.session.add(cave)
        self.db.session.commit()
        
        self.tearDown(delete=False)
        self.setUp()
        cave2 = self.db.session.query(Cave).filter_by(name="Creepy Cave").first()
        self.assertEqual(str(cave2), "<Cave(id=1, name='Creepy Cave', type='Cave', map=None, adjacent_locations=[], display=None>")
    
    def test_world_map(self):
        map = WorldMap(name="Picatanin")
        town = Town(name="Thornwall")
        map.current_location = town
        self.db.session.add(map)
        self.db.session.commit()
        
        self.tearDown(delete=False)
        self.setUp()
        map2 = self.db.session.query(WorldMap).filter_by(name="Picatanin").first()
        self.assertEqual(str(map2), "<WorldMap(id=1, name='Picatanin', type='WorldMap', current_location='Thornwall', adjacent_locations=[], locations=[], display=None>")
    
    def test_add_world_map(self):
        hero = Hero(name="Haldon")
        map = WorldMap(name="Picatanin")
        
        hero.current_world = map
        self.db.session.add(hero)
        self.db.session.commit()
        
        self.tearDown(delete=False)
        self.setUp()
        hero2 = self.db.session.query(Hero).filter_by(name="Haldon").first()
        self.assertEqual(str(hero2.current_world), "<WorldMap(id=1, name='Picatanin', type='WorldMap', current_location=None, adjacent_locations=[], locations=[], display=None>")
        
    def test_prebuilt_objects_game_worlds(self):
        """Test the creation of some prebuilt objects.
        
        !IMPORTANT! complex_relationships.py must be imported before location.py objects are used.
        
        Do: import locations; import complex_relationships
        DON'T Do: 
            import locations
            [FAIL TO: import complex_relationships]
            worldmap = locations.WorldMap(all_map_locations=[etc.])
            session.add(worldmap)
        This will fail because all_map_locations will be a list object instead of 
        a "relationship" object.
        """
        
        self.db.session.add(prebuilt_objects.game_worlds[0])
        self.db.session.commit()

        self.tearDown(delete=False)
        self.setUp()
        world2 = self.db.session.query(WorldMap).filter_by(name="Test_World2").first()
        self.assertEqual(str(world2), """<WorldMap(id=1, name='Test_World2', type='WorldMap', current_location='Thornwall', adjacent_locations=[], locations=['location 0', 'location 1', 'Creepy cave', 'location 3', 'location 4', 'Thornwall', 'location 6', 'location 7', 'location 8', 'location 9', 'location 10', 'location 11'], display=
    <Display(
        page_title = 'Test_World2',
        page_heading = 'You are wandering in the world',
        page_image = 'worldmap',
        paragraph = 'Be safe',
        places_of_interest = []
    )>
>""")
        
    
def test_show_directions():
    db = setup()
    map = locations.game_worlds[0]
    directions = map.show_directions()
    
    #This only works if map.current_location is a Town or Cave.
    #Which it currently is in locations.game_worlds[0]
    assert map.map_cities == [map.current_location]
    assert str(map.display.places_of_interest) == "[(url='/Town/Thornwall', places=['Thornwall'])]"
    teardown(db)
    
def test_places_of_interest():
    db = setup()
    town = locations.game_worlds[0].current_location
    # ps = town.display.places_of_interest
    # for p in ps:
        # print(p.url, p.places)
        
    map = locations.game_worlds[0]
    directions = map.show_directions()
    # ps = map.display.get_places_of_interest()
    # for p in ps:
        # print(p.url, p.places[0].name)
    teardown(db)
    
# def run_all():
    # db = setup()
    # try:
        # test_adjacent_locations()
        # test_town()
        # test_cave()
        # test_world_map()
        # test_add_world_map()
        # test_show_directions()
        # test_places_of_interest()
    # finally:
        # teardown(db)
    # print("All locations_tests passed. No Errors, yay!")
    
# run_all()

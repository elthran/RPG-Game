import unittest
from pprint import pprint
import importlib

from base_classes import Base
from database import EZDB
import locations
from locations import Location  # , Cave, Town, WorldMap, Display
from game import Hero
import complex_relationships
#import prebuilt_objects


"""
This program runs as a test suite for the locations.py module when it is imported.
This modules is run using  :>python locations_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""


class LocationTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the generic environment for each test function.
        
        NOTE: Bizar bug that is related to the fact that prebuilt_objects
        can only be used once. Once used in one test function it no longer exists. And so I reimport it.
        """
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        
        #importlib.reload(prebuilt_objects)

    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()

    def test_main(self):
        game_map = Location("Earth", "map")
        town = Location("Thornwall", "town", parent=game_map)
        cave = Location("Scary Cave", "cave", parent=game_map, siblings=[town])
        blacksmith = Location("Hendrick's", 'blacksmith', parent=town)
        merchant = Location("Mathers", 'merchant', parent=town,
                            siblings=[blacksmith])

        self.db.session.add_all([game_map, town, cave, blacksmith, merchant])
        self.db.update()
        print(game_map.pretty_str())
        print(town.pretty_str())
        print(cave.pretty_str())
        print(blacksmith.pretty_str())
        print(merchant.pretty_str())
        print(Base.pretty_list(merchant.siblings))
        print(merchant.display.pretty_str())

    @unittest.skip("Disabled for debugging.")
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

    @unittest.skip("Disabled for debugging.")
    def test_town(self):
        town = Town(name="Thornwall")
        self.db.session.add(town)
        self.db.session.commit()
        str_town = str(town)
        
        self.tearDown(delete=False)
        self.setUp()
        town2 = self.db.session.query(Town).filter_by(name="Thornwall").first()
        self.assertEqual(str_town, str(town2))

    @unittest.skip("Disabled for debugging.")
    def test_cave(self):
        cave = Cave(name="Creepy Cave")
        self.db.session.add(cave)
        self.db.session.commit()
        str_cave = str(cave)
        
        self.tearDown(delete=False)
        self.setUp()
        cave2 = self.db.session.query(
            Cave).filter_by(name="Creepy Cave").first()
        self.assertEqual(str_cave, str(cave2))

    @unittest.skip("Disabled for debugging.")
    def test_world_map(self):
        game_map = WorldMap(name="Picatanin")
        town = Town(name="Thornwall")
        game_map.locations.append(town)
        self.db.session.add(game_map)
        self.db.session.commit()
        str_map = str(game_map)
        
        self.tearDown(delete=False)
        self.setUp()
        map2 = self.db.session.query(
            WorldMap).filter_by(name="Picatanin").first()
        self.assertEqual(str(map2), str_map)

    @unittest.skip("Disabled for debugging.")
    def test_add_world_map(self):
        hero = Hero(name="Haldon")
        game_map = WorldMap(name="Picatanin")
        
        hero.current_world = game_map
        self.db.session.add(hero)
        self.db.session.commit()
        str_world = str(hero.current_world)
        
        self.tearDown(delete=False)
        self.setUp()
        hero2 = self.db.session.query(Hero).filter_by(name="Haldon").first()
        self.assertEqual(str(hero2.current_world), str_world)

    @unittest.skip("Disabled for debugging.")
    def test_prebuilt_objects_game_worlds(self):
        """Test the creation of some prebuilt objects.
        
        !IMPORTANT! complex_relationships.py must be imported before
        location.py objects are used.
        
        Do: import locations; import complex_relationships
        DON'T Do: 
            import locations
            [FAIL TO: import complex_relationships]
            worldmap = locations.WorldMap(all_map_locations=[etc.])
            session.add(worldmap)
        This will fail because all_map_locations will be a list object
        instead of a "relationship" object.
        """
        world = prebuilt_objects.game_worlds[0]
        self.db.session.add(world)
        self.db.session.commit()

        str_world = str(world)

        self.tearDown(delete=False)
        self.setUp()
        world2 = self.db.session.query(
            WorldMap).filter_by(name="Test_World2").first()
        self.maxDiff = None
        
        self.assertEqual(str(world2), str_world)

    @unittest.skip("Disabled for debugging.")
    def test_show_directions(self):
        """Test the show directions function of the WorldMap object.
        
        NOTE: during self.setUp() prebuilt_objects is re-imported as it is
        erased each time it is used.
        I don't know why.
        """
        game_map = prebuilt_objects.world
        self.db.session.add(game_map)
        self.db.session.commit()
 
        # directions = game_map.show_directions(
        # prebuilt_objects.current_location)
        # This only works if prebuilt_objects.current_location
        # is a Town or Cave.
        # Which it currently is.
        self.assertEqual(game_map.map_cities,
                         [prebuilt_objects.current_location])

    @unittest.skip("Disabled for debugging.")
    def test_places_of_interest(self):
        game_map = prebuilt_objects.world
        self.db.session.add(game_map)
        self.db.session.commit()
 
        # directions = map.show_directions(prebuilt_objects.current_location)
        # This only works if prebuilt_objects.current_location is
        # a Town or Cave.
        # Which it currently is.
        self.assertEqual(
            str(game_map.display.places_of_interest),
            "[(url='/Town/Thornwall', places=['Thornwall'])]")
        
    
if __name__ == '__main__':
    unittest.main()

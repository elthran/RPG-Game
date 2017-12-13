import unittest
from pprint import pprint
import importlib

from base_classes import Base
from database import EZDB
from locations import Location
from game import Hero
import prebuilt_objects


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
        
        NOTE: Bizarre bug that is related to the fact that prebuilt_objects
        can only be used once. Once used in one test function it no longer
        exists. And so I re-import it.
        """
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        
        importlib.reload(prebuilt_objects)

    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()

    @unittest.skip("Disable for Debugging.")
    def test_main(self):
        game_map = Location("Earth", "map")
        town = Location("Thornwall", "town", parent=game_map)
        cave = Location("Scary Cave", "cave", parent=game_map, siblings=[town])
        blacksmith = Location("Hendrick's", 'blacksmith', parent=town)
        merchant = Location("Mathers", 'merchant', parent=town,
                            siblings=[blacksmith])

        self.db.session.add_all([game_map, town, cave, blacksmith, merchant])
        self.db.session.commit()
        # print(game_map.pretty_str())
        # print(town.pretty_str())
        # print(cave.pretty_str())
        # print(blacksmith.pretty_str())
        # print(merchant.pretty_str())
        # print(Base.pretty_list(merchant.siblings))
        # print(merchant.display.pretty_str())

    @unittest.skip("Disabled for debugging.")
    def test_siblings(self):
        town = Location("Thornwall", "town")
        home = Location("Home", 'house', parent=town)
        blacksmith = Location("Hendrick's", 'blacksmith', parent=town)
        merchant = Location("Mathers", 'merchant', parent=town)
        self.db.session.add(town)
        self.db.session.commit()
        sibling_str = Base.pretty_list(home.siblings, key='name')
        print(sibling_str)

        self.tearDown(delete=False)
        self.setUp()
        
        home2 = self.db.session.query(Location).filter_by(name='Home').first()
        sibling_str2 = Base.pretty_list(home2.siblings, key='name')
        print(sibling_str2)
        self.assertEqual(sibling_str2, sibling_str)

    @unittest.skip("Disabled for debugging.")
    def test_grid(self):
        world = Location(name="Htrae", location_type="map")
        world.display.page_heading = "You are wandering in the world"
        world.display.paragraph = "Be safe"

        node_grid = []
        for i in range(0, 12):
            node_grid.append(
                Location(name="Location{}".format(i),
                         location_type='explorable'))
        world.children = node_grid

        town = node_grid[5]
        town.name = "Thornwall"
        town.type = 'town'
        cave = node_grid[2]
        cave.name = "Creepy cave"
        cave.type = 'cave'

        self.db.session.add(world)

        """
        Test Map Visual Representation:
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
        """
        node_grid[0].adjacent = [node_grid[1], node_grid[3], node_grid[5]]
        node_grid[1].adjacent = [node_grid[0], node_grid[2], node_grid[5]]
        node_grid[2].adjacent = [node_grid[1]]
        node_grid[3].adjacent = [node_grid[0], node_grid[4]]
        node_grid[4].adjacent = [node_grid[3]]
        node_grid[5].adjacent = [node_grid[0], node_grid[1], node_grid[6],
                                 node_grid[8], node_grid[9]]
        node_grid[6].adjacent = [node_grid[5], node_grid[7], node_grid[9]]
        node_grid[7].adjacent = [node_grid[6]]
        node_grid[8].adjacent = [node_grid[5]]
        node_grid[9].adjacent = [node_grid[5], node_grid[6]]
        node_grid[10].adjacent = []

        str_town = str(town)
        str_adjacent = Base.pretty_list(town.adjacent, key='name')
        
        self.tearDown(delete=False)
        self.setUp()
        town2 = self.db.session.query(
            Location).filter_by(name="Thornwall").first()
        str_adjacent2 = Base.pretty_list(town2.adjacent, key='name')
        self.assertEqual(str_town, str(town2))
        self.assertEqual(str_adjacent, str_adjacent2)

    @unittest.skip("Disabled for debugging.")
    def test_map(self):
        game_map = Location("Picatanin", 'map')
        town = Location("Thornwall", 'town')
        game_map.locations.append(town)
        self.db.session.add(game_map)
        self.db.session.commit()
        str_game_map = str(game_map)

        self.tearDown(delete=False)
        self.setUp()
        game_map2 = self.db.session.query(
            Location).filter_by(name="Picatanin").first()
        self.assertEqual(str(game_map2), str_game_map)

    @unittest.skip("Disabled for debugging.")
    def test_add_map(self):
        hero = Hero(name="Haldon")
        game_map = Location("Picatanin", 'map')
        
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

        """
        world = prebuilt_objects.game_worlds[0]
        self.db.session.add(world)
        self.db.session.commit()
        str_world = world.pretty

        self.tearDown(delete=False)
        self.setUp()
        world2 = self.db.session.query(
            Location).filter_by(name="Htrae").first()

        self.maxDiff = None
        self.assertEqual(world2.pretty, str_world)

    # @unittest.skip("Disabled for debugging.")
    # def test_show_directions(self):
    #     """Test the show directions function of the WorldMap object.
    #
    #     NOTE: during self.setUp() prebuilt_objects is re-imported as it is
    #     erased each time it is used.
    #     I don't know why.
    #     """
    #     game_map = prebuilt_objects.world
    #     self.db.session.add(game_map)
    #     self.db.session.commit()
 
        # directions = game_map.show_directions(
        # prebuilt_objects.current_location)
        # This only works if prebuilt_objects.current_location
        # is a Town or Cave.
        # Which it currently is.
        # self.assertEqual(game_map.map_cities,
        #                  [prebuilt_objects.current_location])

    # @unittest.skip("Disabled for debugging.")
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

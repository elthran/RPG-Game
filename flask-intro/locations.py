"""
Author: Marlen Brunner and Elthran B.

1. This module should provide a class for each type of location within the game.
2. These classes should use inheritance as much as possible.
3. Each class should provide a render function which uses a flask template and
can be inserted into the main website.

Basic layout should be:
Map
    WorldMap - I tried to make this a location too, but the relationships are too hard to implement.
    TownMap
    CaveMap
    LocationMap
Location
    Town
    Cave
Display
    ...?
    
Each object should have separte data and display properties.
eg.

Town
    id
    name
    adjacent_locations
    location_world
    display
        page_title
        page_heading
        page_image
        paragraph
        places_of_interest
    
"""

try:
    from sqlalchemy import Column, Integer, String, Boolean
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy import orm
    from sqlalchemy.ext.hybrid import hybrid_property
    ####!IMPORTANT!####
    #Sqlite does not implement sqlalchemy.ARRAY so don't try and use it.
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e

#!Important!: Base can only be defined in ONE location and ONE location ONLY!
#Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base


class BaseListElement(Base):
    """Stores list objects in database.
    
    To implement:
    1. add line in this class: parent_table_name_id = Column(Integer, ForeignKey('parent_table_name.id'))
    2. add line in foreign class: _my_list = relationship("BaseListElement")
    3. add method to foreign class:
    @hybrid_property
    def my_list(self):
        '''Return a list of elements.
        '''
        return [element.value for element in self._my_list]

    4. add method to foreign class:
    @my_list.setter
    def my_list(self, values):
        '''Create list of BaseListElement objects.
        '''
        self._my_list = [BaseListElement(value) for value in values]
    
    See Location class for example implementation.
    5. Probably a better way using decorators ...?
    """
    __tablename__ = "base_list"
    id = Column(Integer, primary_key=True)
    int_value = Column(Integer)
    str_value = Column(String)    
    
    location_id = Column(Integer, ForeignKey('location.id'))
    map_id = Column(Integer, ForeignKey('map.id'))
    
    def __init__(self, value):
        """Build BaseListElement from value.
        """
        self.value = value
    
    
    @hybrid_property
    def value(self):
        """Return value of list element.
        
        Can be string or integer.
        """
        return self.int_value or self.str_value


    @value.setter
    def value(self, value):
        """Assign value to appropriate column.
        
        Currently implements the strings and integers.
        """
        if type(value) is type(str()):
            self.str_value = value
        elif type(value) is type(int()):
            self.int_value = value
        else:
            raise "TypeError: BaseListElement does not accept type '{}':".format(type(value))
                        

class Place(Base):
    """Store the name of a place.
    
    eg. Blacksmith or Shops
    """
    __tablename__ = 'place'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    place_of_interest_id = Column(Integer, ForeignKey('place_of_interest.id'))
    
    def __repr__(self):
        return "'{}'".format(self.name)

class PlaceOfInterest(Base):
    """Store data about the url and names of places at a given location.
    
    eg. 
    [("/store/greeting", "Blacksmith", "Shops"),
     ("/barracks", "Barracks"),
     ("/marketplace/greeting", "Marketplace"),
     ("/tavern", "Tavern", "Other"),
     ("/old_mans_hut", "Old Man's Hut"),
     ("/leave_town", "Village Gate", "Outskirts"),
     ("/World_Map/" + self.location_world + "/" + str(self.id), "World Map")]
     
     Note: each url can have many places. When printed it would look like the above.
    """
    __tablename__ = "place_of_interest"
    
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    places = relationship("Place")
    display_id = Column(Integer, ForeignKey('display.id'))
    
    def __init__(self, url=None, places=None):
        self.url = url
        self.places = [Place(name=name) for name in places]
    
    def __repr__(self):
        return """(url='{}', places={})""".format(self.url, self.places)
    

class Display(Base):
    """Stores data for location and map objects that is displayed in the game using html.
    
    Note: When modifing attributes ...
    
    places_of_interest is not implemented ... except during initialization.
    """
    __tablename__ = "display"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    page_title = orm.synonym('name')
    page_heading = Column(String)
    page_image = Column(String)
    paragraph = Column(String)
    
    town_id = Column(Integer, ForeignKey('town.id'))
    town = relationship("Town", back_populates="display")
    
    cave_id = Column(Integer, ForeignKey('cave.id'))
    cave = relationship("Cave", back_populates="display")
    
    world_map_id = Column(Integer, ForeignKey('world_map.id'))
    world_map = relationship("WorldMap", back_populates="display")
    
    _places_of_interest = relationship('PlaceOfInterest')    
    @hybrid_property
    def places_of_interest(self):
        """Return a list of places_of_interest.
        """
        return self._places_of_interest


    @places_of_interest.setter
    def places_of_interest(self, places):
        """Create list of PlaceOfInterest objects.
        """
        if places:
            self._places_of_interest = [PlaceOfInterest(url=p[0], places=p[1:]) for p in places]
        else:
            self._places_of_interest = []
        
        
    def __init__(self, obj, page_heading=None, paragraph=None, places_of_interest=None):
        """Build display object based on objects attributes.
        """
        
        self.name = obj.name
        self.page_heading = page_heading
        
        #eg. page_image = town if Town object is passed or cave if Cave object is passed.
        self.page_image = obj.type.lower()
        self.paragraph = paragraph
        self.places_of_interest = places_of_interest
         
    
    def __str__(self):
        return """
    <{}(
        page_title = '{}',
        page_heading = '{}',
        page_image = '{}',
        paragraph = '{}',
        places_of_interest = {}
    )>
""".format("Display", self.page_title,
        self.page_heading, self.page_image, self.paragraph, self.places_of_interest)


#Marked for refractor
#Consider using a grid and implementing (x,y) coordinates for each location.
class Location(Base):
    """Create a place a character can travel to that is storable in the database.
    
    Note: adjacent_locations is a list of integers. Note a list of locations, I could figure out how to do that.
    Maybe when I implement x,y coordinates for each location it could calculate the adjacent ones
    automatically.
    Note: 'locaton_type' is now 'type'. But you can still use location_type because orm.synonym! ... bam!
    
    Use:
    loc1 = Location(id=1, name="test")
    loc1.adjacent_locations = [2, 3, 4]
    """
    __tablename__ = "location"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    location_type = orm.synonym('type')
    
    map_id = Column(Integer, ForeignKey('map.id'))
    map = relationship("Map", back_populates="locations")
    location_world = orm.synonym('map')
    
    current_location_map_id = Column(Integer, ForeignKey('world_map.id'))
    current_location_map = relationship("Map", back_populates="current_location")
     
        
    __mapper_args__ = {
        'polymorphic_identity':'Location',
        'polymorphic_on':type
    }
    
    #relationships
    # display = etc. one to one.
    # location_world one to one with WorldMap? but each WorldMap can have many locations ...?
    #   so many to one it is!
    # adjacent_locations = one to many relationship with self.
    _adjacent_locations = relationship("BaseListElement")
    
    @hybrid_property
    def adjacent_locations(self):
        """Return a list of ids of adjacent locations.
        """
        return [element.value for element in self._adjacent_locations]


    @adjacent_locations.setter
    def adjacent_locations(self, values):
        """Create list of BaseListElement objects.
        """
        self._adjacent_locations = [BaseListElement(value) for value in values]
        
    def __str__(self):
        return """<{}(id={}, name='{}', type='{}', map='{}', adjacent_locations={}>""".format(
        "Location", self.id, self.name, self.type, self.map.name, self.adjacent_locations)
    
    
class Town(Location):
    """Town object database ready class.
    
    This object is currently for only one town. It would require a bit of work to make it an actual
    generic "Town" object that could be used for any town you want.
    """
    __tablename__ = "town"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)
    
    display = relationship("Display", uselist=False, back_populates="town")

    
    __mapper_args__ = {
        'polymorphic_identity':'Town',
    }
    
    def __str__(self):
        return """<{}(id={}, name='{}', type='{}', map='{}', adjacent_locations={}, display={}>""".format(
        "Town", self.id, self.name, self.type, self.map.name, self.adjacent_locations, self.display)
        

class Cave(Location):
    __tablename__ = "cave"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)
    
    display = relationship("Display", uselist=False, back_populates="cave")

    __mapper_args__ = {
        'polymorphic_identity':'Cave',
    }
    
    def __str__(self):
        return """<{}(id={}, name='{}', type='{}', map='{}', adjacent_locations={}, display={}>""".format(
        "Cave", self.id, self.name, self.type, self.map.name, self.adjacent_locations, self.display)


class Map(Base):
    """Basically a location clone but without the mess of joins and relationship problems :P.
    
    Solves: Incest ...
    """
    __tablename__ = "map"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    location_type = orm.synonym('type')
    
    
    current_location = relationship("Location", uselist=False, back_populates="current_location_map")
    
    locations = relationship("Location", back_populates="map")
    all_map_locations = orm.synonym('locations')
        
    __mapper_args__ = {
        'polymorphic_identity':'Map',
        'polymorphic_on':type
    }
    
    _adjacent_locations = relationship("BaseListElement")
    
    @hybrid_property
    def adjacent_locations(self):
        """Return a list of ids of adjacent locations.
        """
        return [element.value for element in self._adjacent_locations]


    @adjacent_locations.setter
    def adjacent_locations(self, values):
        """Create list of BaseListElement objects.
        """
        self._adjacent_locations = [BaseListElement(value) for value in values]
        
        
    def __str__(self):
        return """<{}(id={}, name='{}', type='{}', current_location='{}' adjacent_locations={}""".format(
        "Map", self.id, self.name, self.type, self.current_location.name, self.adjacent_locations)
    
    
class WorldMap(Map):
    __tablename__ = "world_map"
    
    id = Column(Integer, ForeignKey('map.id'), primary_key=True)
    
    display = relationship("Display", uselist=False, back_populates="world_map")

    __mapper_args__ = {
        'polymorphic_identity':'WorldMap',
    }
    
    #Marked for rebuild
    #Cause I don't no what it does.
    def show_directions(self):
        # print(self.display)
        # exit('test show_directions')
        directions = self.current_location.adjacent_locations
        if directions == []:
            directions = [1,2,3]
        self.map_cities = [location for location in self.all_map_locations if (location == self.current_location and (location.type == "Town" or location.type == "Cave"))] # too long, but will refactor later
        if len(self.map_cities) > 0:
            self.display.places_of_interest = [("/{}/{}".format(self.map_cities[0].type, self.map_cities[0].name),
            self.map_cities.name)]
        else:
            self.display.places_of_interest = []
        return directions
        
        
    # temporarily location_id is the same as the index in the list of all_map_locations
    def find_location(self, location_id):
        id = int(location_id)
        return self.all_map_locations[int(id)]
    
    def __str__(self):
        return """<{}(id={}, name='{}', type='{}', current_location='{}', adjacent_locations={}, display={}""".format(
        "WorldMap", self.id, self.name, self.type, self.current_location.name, self.adjacent_locations, self.display)

#Just another synonym for backwards compatability        
World_Map = WorldMap        
    
"""
    def get_locations(self):

        with open("data\town." + name + ".txt", 'r') as f:
            data = f.read()
            return Town.parse(data)

    def display(self):
        Return an html object of the town built from a template.

        This should be able to be "popped" into the main post-login site in the content section.
        pass

    def parse(data):
        pass
"""


 #------------------------------------
 #
 #  Initializing Game Worlds
 #  (To be moved to a common
 #   init function later)
 #
 #------------------------------------

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
town = test_locations2[5]
test_locations2[2] = Cave(name="Creepy cave", id=2)
cave = test_locations2[2]

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

world = WorldMap(name="Test_World2", current_location=town, all_map_locations=test_locations2)

#Note: Displays must be added after all objects are defined. Or you get error that I was to lazy to fix.
world.diplay = Display(world, page_heading="You are wandering in the world", paragraph="Be safe")


town.display = Display(town, page_heading="You are in {}".format(town.name),
    paragraph="There are many places to visit within the town. Have a look!",
    places_of_interest=[("/store/greeting", "Blacksmith", "Shops"),
        ("/barracks", "Barracks"),
        ("/marketplace/greeting", "Marketplace"),
        ("/tavern", "Tavern", "Other"),
        ("/old_mans_hut", "Old Man's Hut"),
        ("/leave_town", "Village Gate", "Outskirts"),
        ("/World_Map/{}/{}".format(town.location_world.name, town.id), "World Map")])
        
cave.display = Display(cave, page_heading="You are in a cave called {}".format(cave.name),
    paragraph="There are many scary places to die within the cave. Have a look!",
    places_of_interest=[("/World_Map/{}/{}".format(cave.location_world.name, cave.id), "World Map")])

game_worlds = [world]
#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
#game_worlds = [World_Map("Test_World", TEST_WORLD_ID, test_locations)]

#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
if __name__ == "__main__":
    """For testing run module.
    
    Because of circular imports I can't work out how to import the test suite here ....
    
    """
    # import tests.locations_tests
    print('yay!')
    

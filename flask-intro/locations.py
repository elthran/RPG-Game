"""
Author: Marlen Brunner

1. This module should provide a class for each type of location within the game.
2. These classes should use inheritance as much as possible.
3. Each class should provide a render function which uses a flask template and
can be inserted into the main website.

Basic layout should be:
Map
    WorldMap
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
    #!Important!: Base can only be defined in ONE location and ONE location ONLY!
    #Well ... ok, but for simplicity sake just pretend that that is true.
    from sqlalchemy import Column, Integer, String, Boolean
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy import orm

    ####!IMPORTANT!####
    #Sqlite does not implement sqlalchemy.ARRAY so don't try and use it.
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e
    
from base_classes import Base

class BaseList(Base):
    """Stores list objects in database.
    
    To implement:
    1. add line in this class: parent_id = Column(Integer, ForeignKey('parent.id'))
    2. add line in foreign class: dummy_children = relationship("BaseList")
    3. add __setattr__ method in foreign class
    4. build init_on_load method in foreign class
    5. build _add_children method in foreign class
    
    See Location (locations.py) class for implementation.
    """
    __tablename__ = "base_list"
    id = Column(Integer, primary_key=True)
    int_value = Column(Integer)
    str_value = Column(String)
    value = None
    
    
    location_id = Column(Integer, ForeignKey('base_location.id'))
    
    def __init__(self, value):
        self.value = value
        if type(value) is type(str()):
            self.str_value = value
        elif type(value) is type(int()):
            self.int_value = value
        
    @orm.reconstructor
    def init_on_load(self):
        """Build extra data attributes on object load.
        
        Currently implements the str_value attribute.
        Currently implements the int_value attribute.
        """
        self.value = self.int_value or self.str_value
    
    def __str__(self):
        return repr(self.value)
        
    def __repr__(self): 
        """Returns string representation of object.
        """
        atts = []
        column_headers = self.__table__.columns.keys()
        extra_attributes = [key for key in vars(self).keys() if key not in column_headers]
        for key in column_headers:
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
            
        for key in sorted(extra_attributes):
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
        
        data = "<{}({})>".format('BaseList', ', '.join(atts))
        return data


class BaseLocation(Base):
    __tablename__ = "base_location"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity':'BaseLocation',
        'polymorphic_on':type
    }
    
    dummy_adjacent_locations = relationship('BaseList')
    adjacent_locations = []
    dummy_places_of_interest = relationship('BaseList')
    places_of_interest = []
    
    def __setattr__(self, key, value):
        """Sets the attributes of Location class.
        
        Special case: if attribute is "adjacent_location" then attribute takes a list
        of integers and sets it to a list of BaseList elements
        Special case: if attribute is "places_of_interest" then attribute takes a list
        of integers and sets it to a list of BaseList elements
        """
        if key is "adjacent_locations":
            assert type(value) == type([])
            self._add_adjacent_locations(value)
        elif key is "places_of_interest":
            assert type(value) == type([])
            self._add_places_of_interest(value)
        
        super().__setattr__(key, value)
    
    
    @orm.reconstructor
    def init_on_load(self):
        """Build extra data attributes on object load.
        
        Currently implements the adjacent_locations attribute.
        Currently implements the places_of_interest attribute.
        """
        self.adjacent_locations = [element.value for element in self.dummy_adjacent_locations]
        self.places_of_interest = [element.value for element in self.dummy_places_of_interest]
        self.location_type = self.type
    
    
    def _add_adjacent_locations(self, values):
        """Store adjacent_locations assignment as a list of attributes.
        """
        self.dummy_adjacent_locations = [BaseList(value) for value in values]
    
    
    def _add_places_of_interest(self, values):
        """Store places_of_interest assignment as a list of attributes.
        """
        self.dummy_places_of_interest = [BaseList(value) for value in values]
    
    
    def __str__(self): 
        """Returns string representation of object.
        """
        atts = []
        column_headers = self.__table__.columns.keys()
        extra_attributes = [key for key in vars(self).keys()
            if key not in column_headers
            if key != '_sa_instance_state'
            if 'dummy' not in key]
        for key in column_headers:
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
            
        for key in sorted(extra_attributes):
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
        
        data = "<{}({})>".format(self.type, ', '.join(atts))
        return data
        
        
    def __repr__(self): 
        """Returns string representation of object.
        """
        atts = []
        column_headers = self.__table__.columns.keys()
        extra_attributes = [key for key in vars(self).keys() if key not in column_headers]
        for key in column_headers:
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
            
        for key in sorted(extra_attributes):
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
        
        data = "<{}({})>".format(self.type, ', '.join(atts))
        return data

        
#Marked for refractor
#Consider implementing different adjacent_locations attribute that is a list of locations
#Consider using a grid and implementing (x,y) coordinates for each location.
class Location(BaseLocation):
    __tablename__ = "location"
    
    id = Column(Integer, ForeignKey('base_location.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'Location'
    }
    
    #relationship
    world_map_id = Column(Integer, ForeignKey('world_map.id'))
    location_world = relationship("World_Map", foreign_keys=[world_map_id], back_populates="locations")


class World_Map(BaseLocation):
    """World map database ready class.
    
    Notes:
        current_location is a location object in the all_map_locations list.
        id : initial location id, must be on the map
    """
    __tablename__ = "world_map"
    
    world_map_id = Column('id', Integer, primary_key=True)
    base_location_id = Column(Integer, ForeignKey('base_location.id'), primary_key=True)
    

    page_heading = Column(String, default="You are wandering in the world")
    page_image = Column(String, default="map")
    paragraph = Column(String, default="Be safe")

    __mapper_args__ = {
        'polymorphic_identity':'World_Map',
    }
    
    current_location_id = Column(Integer)

    #Relationships
    #Should be a list of all location objects that the World_Map contains.
    # all_map_locations = relationship("Location", foreign_keys='[Location.world_map_id]',
        # back_populates="location_world") 
        
    locations = relationship("Location", foreign_keys="Location.world_map_id", back_populates="location_world")
    # towns = relationship("Towns", foreign_keys="Town.world_map_id", back_populates="location_world")
    # caves = relationship("Caves", foreign_keys="Cave.world_map_id", back_populates="location_world")
    
    
    # def __init__(self, name="Test_World2", current_location_id=None, all_map_locations=[]):
        # """Build World_Map extend attributes.
        
        # Sets up caves attribute.
        # """
        # self.name = name
        # self.current_location_id = current_location_id
        # self.all_map_locations = all_map_locations
        
    
    
    @orm.reconstructor
    def init_on_load(self):
        """Build derived attributes of object on database load.
        
        See: init_on_load() in SQLAlchemy
        """
        self.current_location = self.all_map_locations[int(self.current_location_id)]
        self.map_cities = [location for location in self.all_map_locations if (location == self.current_location and (location.location_type == "Town" or location.location_type == "Cave"))] # too long, but will refactor later
        
        self.towns = [location for location in self.all_map_locations if location.type == "Town"]
        self.caves = [location for location in self.all_map_locations if location.type == "Cave"]
        
        self.page_title = self.name
        self.page_image = self.name
        self.location_type = self.type
    

    def show_directions(self):
        directions = self.current_location.adjacent_locations
        if directions == []:
            directions = [1,2,3]
        if len(self.map_cities) > 0:
            self.places_of_interest = [("/" + self.map_cities[0].location_type + "/" + self.map_cities[0].name, self.map_cities[0].name)]
        else:
            self.places_of_interest = []
        return directions
        

class Town(Location):
    """Town object database ready class.
    
    This object is currently for only one town. It would require a bit of work to make it an actual
    generic "Town" object that could be used for any town you want.
    """
    __tablename__ = "town"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'Town',
    }
    
    #Relationships
    # world_map_id = Column(Integer, ForeignKey('world_map.id'))
    # location_world = relationship("World_Map", foreign_keys=[world_map_id], back_populates="towns")
   
    
    @orm.reconstructor
    def init_on_load(self):
        """Build derived attributes of object on database load.
        
        See: init_on_load() in SQLAlchemy
        """
        #Marked for restructure
        #Consider adding these during creation or making them column defaults
        self.location_type = self.type
        self.page_title = self.name
        self.page_heading = "You are in " + self.name
        self.page_image = "town"
        self.paragraph = "There are many places to visit within the town. Have a look!"
        self.places_of_interest = [("/store/greeting", "Blacksmith", "Shops"),
                                  ("/barracks", "Barracks"),
                                  ("/marketplace/greeting", "Marketplace"),
                                  ("/tavern", "Tavern", "Other"),
                                  ("/old_mans_hut", "Old Man's Hut"),
                                  ("/leave_town", "Village Gate", "Outskirts"),
                                  ("/World_Map/" + self.location_world + "/" + str(self.id), "World Map")]
        

class Cave(Location):
    __tablename__ = "cave"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Cave',
    }
    
    #Relationships
    # world_map_id = Column(Integer, ForeignKey('world_map.id'))
    # location_world = relationship("World_Map", foreign_keys=[world_map_id], back_populates="caves")
   
    
    @orm.reconstructor
    def init_on_load(self):
        """Runs on object load from database.
        """
        #Marked for restructure.
        #Consider making defaults in columns
        self.location_type = self.type
        self.page_title = self.name
        self.page_heading = "You are in a cave called " + self.name
        self.page_image = "cave"
        self.paragraph = "There are many scary places to die within the cave. Have a look!"
        self.places_of_interest = [("/World_Map/" + str(self.location_world) + "/" + str(self.id), "World Map")]
        
    
    def __repr__(self): 
        """Returns string representation of object.
        """
        atts = []
        column_headers = self.__table__.columns.keys()
        extra_attributes = [key for key in vars(self).keys() if key not in column_headers]
        for key in column_headers:
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
            
        for key in sorted(extra_attributes):
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
        
        data = "<{}({})>".format(self.location_type, ', '.join(atts))
        return data


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
#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
#game_worlds = [World_Map("Test_World", TEST_WORLD_ID, test_locations)]

#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
if __name__ == "__main__":
    """For testing run module.
    
    Because of circular imports I can't work out how to import the test suite here ....
    
    """
    # import tests.locations_tests
    

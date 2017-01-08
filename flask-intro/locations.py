"""
Author: Marlen Brunner

1. This module should provide a class for each type of location within the game.
2. These classes should use inheritance as much as possible.
3. Each class should provide a render function which uses a flask template and
can be inserted into the main website.

Basic layout should be:
Game Objects (from other module maybe?) I am just going to start with Location as "progenitor".
-Location
--Town
---Shop
----display
---Blacksmith, etc.
---display
--leave
--enter
--display
"""

try:
    #!Important!: Base can only be defined in ONE location and ONE location ONLY!
    #Well ... ok, but for simplicity sake just pretend that that is true.
    from saveable_objects import Base
    
    from sqlalchemy import Column, Integer, String, Boolean, ARRAY
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy import orm
    from sqlalchemy import CheckConstraint
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")

class Location(Base):
    __tablename__ = "location"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    location_type = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity':'location',
        'polymorphic_on':location_type
    }
    
    #Marked for restructure
    #Consider using ARRAY(Location) and just have a list of locations
    #Or ARRAY and use Location id's
    adjacent_locations = ARRAY(Integer)
    
    #Relationships
    world_map_id = Column(Integer, ForeignKey('world_map.id'))


class World_Map(Location):
    """World map database ready class.
    
    Notes:
        current_location is a location object in the all_map_locations list.
        id : initial location id, must be on the map
    """
    __tablename__ = "world_map"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'World_Map',
    }
    places_of_interest = ARRAY(String)
    current_location_id = Column(Integer, nullable=False)

    #Relationships
    all_map_locations = relationship("Location")
    # town = relationship("Town", uselist=False, back_populates="location_world")
    # cave = relationship("Cave", uselist=False, back_populates="location_world")
    heroes = relationship("Hero", back_populates="current_world")
    
    
    @orm.reconstructor
    def init_on_load(self):
        """Build derived attributes of object on database load.
        
        See: init_on_load() in SQLAlchemy
        """
        self.current_location = self.all_map_locations[int(self.current_location_id)]
        self.map_cities = [location for location in self.all_map_locations if (location == self.current_location and (location.location_type == "Town" or location.location_type == "Cave"))] # too long, but will refactor later 
        self.page_title = self.name
        self.page_heading = "You are wandering in the world"
        self.page_image = "map"
        self.paragraph = "Be safe"
        self.page_image = self.name
    

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
    # location_world = relationship("World_Map", back_populates="town")
    heroes = relationship("Hero", back_populates="current_city")
    
    @orm.reconstructor
    def init_on_load(self):
        """Build derived attributes of object on database load.
        
        See: init_on_load() in SQLAlchemy
        """
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
    # location_world = relationship("World_Map", back_populates="cave")
    
    @orm.reconstructor
    def init_on_load(self):
        self.page_title = self.name
        self.page_heading = "You are in a cave called " + self.name
        self.page_image = "cave"
        self.paragraph = "There are many scary places to die within the cave. Have a look!"
        self.places_of_interest = [("/World_Map/" + self.location_world + "/" + str(self.id), "World Map")]


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


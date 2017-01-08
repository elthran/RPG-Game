from sqlalchemy.ext.declarative import declarative_base
#Initialize SQLAlchemy base class.
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ARRAY
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

class AdjacentLocation(Base):
    __tablename__ = "adjacent_location"
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'))
    
    def __init__(self, values):
        print(values)
        if len(values) == 1:
            self.value=values[0]
        else:
            for value in values:
                self += [AdjacentLocation([value])]
                print(self)

class Location(Base):
    __tablename__ = "location"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    location_type = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity':'Location',
        'polymorphic_on':location_type
    }
    
    adjacent_locations = relationship('AdjacentLocation')
    
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
    #Should be a list of all location objects that the World_Map contains.
    all_map_locations = relationship("Location")

   
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

    
class Cave(Location):
    __tablename__ = "cave"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Cave',
    }


    
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

test_locations2[1].adjacent_locations = AdjacentLocation([2, 3, 4])
# test_locations2[2].adjacent_locations = [1, 5]
# test_locations2[3].adjacent_locations = [1, 4]
# test_locations2[4].adjacent_locations = [1, 3, 5, 7]
# test_locations2[5].adjacent_locations = [2, 4, 6, 8]
# test_locations2[6].adjacent_locations = [5, 9, 10]
# test_locations2[7].adjacent_locations = [4, 8]
# test_locations2[8].adjacent_locations = [5, 7, 9]
# test_locations2[9].adjacent_locations = [6, 8]
# test_locations2[10].adjacent_locations = [6]

game_worlds = [World_Map(name="Test_World2", current_location_id=5, all_map_locations=test_locations2)]
for location in game_worlds[0].all_map_locations:
    print(location.name, location.location_type, location.adjacent_locations)

    
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine, checkfirst=True)

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
from base_classes import Base, BaseListElement

import pdb
                        

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
     ("/WorldMap/" + self.location_world + "/" + str(self.id), "World Map")]
     
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
    
    location_id = Column(Integer, ForeignKey('location.id'))
    map_id = Column(Integer, ForeignKey('map.id'))
    
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
         
    
    def __repr__(self):
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
    map = relationship("Map", foreign_keys=[map_id], back_populates="locations")
    location_world = orm.synonym('map')
         
    display = relationship("Display", uselist=False)
        
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self.adjacent_locations = []
     
        
    __mapper_args__ = {
        'polymorphic_identity':'Location',
        'polymorphic_on':type
    }
    
    
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
        
        
    # def __str__(self):
        # try:
            # return """<{}(id={}, name='{}', type='{}', map='{}', adjacent_locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.map.name, self.adjacent_locations, self.display)
        # except AttributeError:
            # return """<{}(id={}, name='{}', type='{}', map=None, adjacent_locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, self.display)
    
    
class Town(Location):
    """Town object database ready class.
    
    Basically adds a display and identity of "Town" to the location object.
    """
    __tablename__ = "town"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)
   
    __mapper_args__ = {
        'polymorphic_identity':'Town',
    }
    

class Cave(Location):
    """Cave object database ready class.
    
    Basically adds a display and identity of "Cave" to the location object.
    """
    __tablename__ = "cave"
    
    id = Column(Integer, ForeignKey('location.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'Cave',
    }
    

class Map(Base):
    """Basically a location clone but without the mess of joins and relationship problems :P.
    
    Solves: Incest ...
    """
    __tablename__ = "map"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    location_type = orm.synonym('type')
    
    locations = relationship("Location", foreign_keys='[Location.map_id]', back_populates="map")
    all_map_locations = orm.synonym('locations')
    
    display = relationship("Display", uselist=False)
        
    __mapper_args__ = {
        'polymorphic_identity':'Map',
        'polymorphic_on':type
    }
    
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
        
        
    # def __str__(self):
        # locations = str([location.name for location in self.locations])
        # try:
            # return """<{}(id={}, name='{}', type='{}', adjacent_locations={}, locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, locations, self.display)
        # except AttributeError:
            # return """<{}(id={}, name='{}', type='{}', adjacent_locations={}, locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, locations, self.display)        
    
    
class WorldMap(Map):
    __tablename__ = "world_map"
    
    id = Column(Integer, ForeignKey('map.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'WorldMap',
    }
    
    #Marked for rebuild
    #Creates attribute map_cities. Prehaps should be a relations?
    #And map_cities should probably be map_city? Or some other name that actually explains
    #what it does??
    #This function modifes the object and returns a value. It should only do one or the other.
    def show_directions(self, current_location):
        """Return a list of directions you can go from your current_location.
        
        ALSO! modifies the attribute map_cities and places_of_interest.
        map_cities is only a single value of either a cave or a town.
        """
        assert current_location in self.locations
        
        directions = current_location.adjacent_locations
        if directions == []:
            directions = [1,2,3]
            
        self.map_cities = []    
        if current_location.type in ["Town", "Cave"]:
            self.map_cities = [current_location]
        
        if self.map_cities:
            city = self.map_cities[0]
            self.display.places_of_interest = [("/{}/{}".format(city.type, city.name), city.name)]
                
        return directions
        
        
    # temporarily location_id is the same as the index in the list of all_map_locations
    def find_location(self, location_id):
        return self.all_map_locations[location_id]

        
#Just another synonym for backwards compatability (which id don't know if it even works?)       
World_Map = WorldMap 

 
if __name__ == "__main__":
    """For testing run module.
    
    Because of circular imports I can't work out how to import the test suite here ....
    
    """
    # import tests.locations_tests
    pass
    

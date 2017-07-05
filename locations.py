"""
Author: Marlen Brunner and Elthran B.

1. This module should provide a generic location class.
2. If more specific function is required you can subclass
3. Each Location should have a Display which holds the data the HTML page
    will display.
4. -potentially- The Display class could pre-render/or hold reference to
a flask template so that it can be inserted into the main website directly.

5. !Important! The location must have a kind of grid reference that fucks up
my beautiful sibling code! Dam now I have to rebuild it.
Maybe make siblings calculated? Populated from the hex grid surrounding
this location?

Location
    Display
    
Each object should have separate data and display properties.
eg.

Location
    id
    name
    siblings = many to many relationship with self.
    children = shops, arena
    parent (a.k.a. world_map)
    url (/Town/Thornwall, e.g. /{type}/{name}.lower())
        or url = encompassing.url + /type/name
    type (e.g. town)
    display
        display_name - Specially formatted name?
        page_title - specially formatted version of 'name'
        page_heading - specially formatted version of 'name'
        page_image - derived from 'name'
        paragraph - description of location
"""
import warnings
import pdb

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property
# ###!IMPORTANT!####
# Sqlite does not implement sqlalchemy.ARRAY so don't try and use it.

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base


class Display(Base):
    """Stores data for location and map objects that is displayed in the game
    using html.

    Note: When modifying attributes ...

    places_of_interest is not implemented ... except during initialization.
    """
    __tablename__ = "display"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    page_title = orm.synonym('name')
    page_heading = Column(String)
    page_image = Column(String)
    paragraph = Column(String)

    # External relationships
    # One location -> one display (bidirectional)
    _location = relationship('Location', uselist=False,
                             back_populates='display')

    @hybrid_property
    def obj(self):
        """Returns the object that this is connected to.

        Only one type of object may be connected at a time.
        This is not enforced and should be.
        """
        return self._location or None

    @hybrid_property
    def places_of_interest(self):
        places = []
        for child in self.obj.children:
            places.append(child.url, child.name)
        places.append(self.obj.parent.url, self.obj.parent.name)
        return places

    def __init__(self, obj, page_heading=None, paragraph=None):
        """Build display object based on objects attributes.

        I think that I should add in a link to the correct HTML template
        as well? Based on location type?
        """

        self.name = obj.name
        self.page_heading = page_heading or "You are in {}".format(self.name)

        # eg. page_image = town if Town object is passed or cave if Cave
        # object is passed.
        self.page_image = obj.type.lower()
        self.paragraph = paragraph or "There are many places to visit within" \
                                      " the {}. Have a look!".format(obj.type)


class AdjacentLocation(Base):
    """Allow for locations to connect to other locations.

    This is done through a out/in path architecture and
    is horrifically complex. See:
    http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#self-referential-many-to-many-relationship
    """
    __tablename__ = 'adjacent_location'
    out_adjacent_id = Column(Integer, ForeignKey('location.id'),
                             primary_key=True)
    in_adjacent_id = Column(Integer, ForeignKey('location.id'),
                            primary_key=True)


class Location(Base):
    """A place that the hero can travel to or interact with.

    The main hierarchy is parent -> child, where to children with
    the same parent are called 'siblings'
    General order is:
    map -> town -> blacksmith
                -> marketplace
                -> gate
                -> arena
        -> cave
        -> explorable/generic location
    """

    ALL_TYPES = [
        'town', 'map', 'explorable', 'cave', 'blacksmith',
        'merchant', 'house'
    ]

    __tablename__ = 'location'
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/
    # declarative/table_config.html
    # __table_args__ = (
    #     UniqueConstraint(
    #         'parent', 'children', 'siblings', name='non_circular')
    # )
    # Need validators for children - child can't be parent or sibling
    # Need validator for parent - parent can't be child or sibling
    # Need validator for siblings - can't be parent or child, max of 6
    # Think a hex grid

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'))
    name = Column(String)
    url = Column(String)
    type = Column(String)

    children = relationship("Location", back_populates="parent",
                            foreign_keys=[parent_id])
    parent = relationship("Location", remote_side=[id],
                          back_populates="children",
                          foreign_keys=[parent_id])
    locations = orm.synonym('children')
    encompassing_location = orm.synonym('parent')

    _out_adjacent = relationship(
        "Location",
        secondary="adjacent_location",
        primaryjoin="Location.id==adjacent_location.c.out_adjacent_id",
        secondaryjoin="Location.id==adjacent_location.c.in_adjacent_id",
        backref="_in_adjacent",
        foreign_keys='[AdjacentLocation.out_adjacent_id, '
                     'AdjacentLocation.in_adjacent_id]')

    # External relationships
    # Many heroes -> one map/world. (bidirectional)
    heroes = relationship("Hero", back_populates='current_world')
    # One location -> one display (bi)
    display_id = Column(Integer, ForeignKey('display.id'))
    display = relationship("Display", back_populates='_location')

    # @orm.validates('adjacent')
    # def build_adjacency(self, key, sibling):
    #     if isinstance(sibling, int):
    #         raise Exception("Use Database method add_sibling_by_id")
    #     if sibling in self.parent.children:
    #         return sibling
    #     raise Exception("Not all of these are valid siblings.")

    @hybrid_property
    def adjacent(self):
        return set(self._out_adjacent + self._in_adjacent)

    @adjacent.setter
    def adjacent(self, values):
        self._out_adjacent = values
        # for sibling in siblings:
        #     if self not in sibling.adjacent:
        #         sibling.adjacent.append(self)

    # @orm.validates('parent', 'children')
    # def update_siblings(self, key, value):
    #     if key == 'children':
    #         value.update_sibilings()
    #     else:
    #         self.update_siblings()

    @hybrid_property
    def siblings(self):
        siblings = []
        if self.parent:
            siblings = list(self.parent.children)
            siblings.remove(self)
        return siblings

    def get_sibling_ids(self):
        return [sibling.id for sibling in self.siblings]

    @orm.validates('type')
    def validate_type(self, key, value):
        if value in Location.ALL_TYPES:
            return value
        else:
            raise Exception(
                "Location type '{}' doesn't exist. "
                "Valid types are: {}".format(
                    value,
                    Location.ALL_TYPES
                )
            )

    def __init__(self, name, location_type, parent=None, children=[],
                 siblings=[]):
        """Create a now location object that the hero can explore.

        :param location_type: e.g. map, town, store
        :param parent: the place this place is inside of
        :param children: places inside this place
        :param siblings: the places that share this places parent.

        NOTE: if you set the parent attribute ... the siblings
        attribute should be populated automatically or vice versa ...
        so generally it isn't useful to set the parent and siblings
        at the same time. Thought it can be in special cases.

        NOTE2: the url is populated automatically from the parent url
        and this location's type and name.

        NOTE3: the Display is populated automatically as well but can have
        extra information added to it.
        """
        self.name = name
        self.type = location_type
        self.parent = parent
        self.children = children
        self.url = self.build_url()
        self.display = Display(self)
        # self.init_on_load()

    # @orm.reconstructor
    # def init_on_load(self):
    #     self.siblings = self.update_siblings()

    def build_url(self):
        if self.parent is None:
            return "/{}/{}".format(self.type, self.name)
        else:
            return self.parent.url + "/{}/{}".format(
                self.type, self.name)


# # Marked for refactor
# # Consider using a grid and implementing (x,y) coordinates for each location.
# class Location(Base):
#     """A place a hero can travel to that is storable in the database.
#
#     Note: adjacent_locations is a list of integers. Note a list of locations,
#     I could figure out how to do that.
#     Maybe when I implement x,y coordinates for each location it could
#     calculate the adjacent ones
#     automatically.
#     Note: 'location_type' is now 'type'. But you can still use location_type
#     because orm.synonym! ... bam!
#
#     Use:
#     loc1 = Location(id=1, name="test")
#     loc1.adjacent_locations = [2, 3, 4]
#     """
#     __tablename__ = "location"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     type = Column(String)
#     location_type = orm.synonym('type')
#     url = Column(String)
#
#     map_id = Column(Integer, ForeignKey('map.id'))
#     map = relationship("Map", foreign_keys=[map_id], back_populates="locations")
#     location_world = orm.synonym('map')
#
#     display = relationship("Display", uselist=False)
#
#     def __init__(self, name, id=None):
#         self.id = id
#         self.name = name
#         self.adjacent_locations = []
#         self.url = "/{}/{}".format(self.type, self.name)
#
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Location',
#         'polymorphic_on':type
#     }
#
#
#     @hybrid_property
#     def adjacent_locations(self):
#         """Return a list of ids of adjacent locations.
#         """
#         return [element.value for element in self._adjacent_locations]
#
#
#     @adjacent_locations.setter
#     def adjacent_locations(self, values):
#         """Create list of BaseListElement objects.
#         """
#         self._adjacent_locations = [BaseListElement(value) for value in values]
#
#
# class Town(Location):
#     """Town object database ready class.
#
#     Basically adds a display and identity of "Town" to the location object.
#     """
#     __tablename__ = "town"
#
#     id = Column(Integer, ForeignKey('location.id'), primary_key=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Town',
#     }
#
#
# class Cave(Location):
#     """Cave object database ready class.
#
#     Basically adds a display and identity of "Cave" to the location object.
#     """
#     __tablename__ = "cave"
#
#     id = Column(Integer, ForeignKey('location.id'), primary_key=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Cave',
#     }
#
#
# class Map(Base):
#     """Basically a location clone but without the mess of joins and relationship problems :P.
#
#     Solves: Incest ...
#     """
#     __tablename__ = "map"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     type = Column(String)
#     location_type = orm.synonym('type')
#
#     locations = relationship("Location", foreign_keys='[Location.map_id]', back_populates="map")
#     all_map_locations = orm.synonym('locations')
#
#     display = relationship("Display", uselist=False)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Map',
#         'polymorphic_on':type
#     }
#
#     @hybrid_property
#     def adjacent_locations(self):
#         """Return a list of ids of adjacent locations.
#         """
#         return [element.value for element in self._adjacent_locations]
#
#
#     @adjacent_locations.setter
#     def adjacent_locations(self, values):
#         """Create list of BaseListElement objects.
#         """
#         self._adjacent_locations = [BaseListElement(value) for value in values]
#
#
#     # def __str__(self):
#         # locations = str([location.name for location in self.locations])
#         # try:
#             # return """<{}(id={}, name='{}', type='{}', adjacent_locations={}, locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, locations, self.display)
#         # except AttributeError:
#             # return """<{}(id={}, name='{}', type='{}', adjacent_locations={}, locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, locations, self.display)
#
#
# class WorldMap(Map):
#     __tablename__ = "world_map"
#
#     id = Column(Integer, ForeignKey('map.id'), primary_key=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'WorldMap',
#     }
#
#     #Marked for rebuild
#     #Creates attribute map_cities. Prehaps should be a relations?
#     #And map_cities should probably be map_city? Or some other name that actually explains
#     #what it does??
#     #This function modifes the object and returns a value. It should only do one or the other.
#     def show_directions(self, current_location):
#         """Return a list of directions you can go from your current_location.
#
#         ALSO! modifies the attribute map_cities and places_of_interest.
#         map_cities is only a single value of either a cave or a town.
#         """
#         assert current_location in self.locations
#
#         directions = current_location.adjacent_locations
#         if directions == []:
#             directions = [1,2,3]
#
#         self.map_cities = []
#         if current_location.type in ["Town", "Cave"]:
#             self.map_cities = [current_location]
#
#         if self.map_cities:
#             city = self.map_cities[0]
#             self.display.places_of_interest = [("/{}/{}".format(city.type, city.name), city.name)]
#
#         return directions
#
#
#     # temporarily location_id is the same as the index in the list of all_map_locations
#     def find_location(self, location_id):
#         return self.all_map_locations[location_id]
#
#
# #Just another synonym for backwards compatability (which id don't know if it even works?)
# World_Map = WorldMap

 
if __name__ == "__main__":
    pass



"""
Author: Marlen Brunner and Elthran B.

1. This module should provide a generic location class.
2. If more specific function is required you can subclass
3. Each Location should have a Display which holds the data the HTML page
    will display.
4. -potentially- The Display class could pre-render/or hold reference to
a flask template so that it can be inserted into the main website directly.

5. !Important! The location must have a list of adjacent locations. This
should be a kind of 'directed graph' or a many to many relationship.
If A is sibling to B, B should be sibling to A by default. Non bidirectional
can be added later.

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
        places_of_interest - generated list of urls that you can move to
            from this location.

Ideas:
    Maybe a long and short url?
    long: /map/Map_Name/town/Town_Name/store/Store_Name
    short: /store/Store_name (basically the last part)
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
    """Stores data for Location objects that is displayed in the game
    using html.
    """
    __tablename__ = "display"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    page_title = orm.synonym('name')
    page_heading = Column(String)
    page_image = Column(String)
    paragraph = Column(String)

    """
    External relationships:
    
    This is set up so that each external relationship is one to one and can be
    accessed through the generic 'self.obj' attribute using
    a list of or statements ... only one should be set at a time.
    """
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

    def __init__(self, obj, page_heading=None, paragraph=None):
        """Build display object based on objects attributes.

        I think that I should add in a link to the correct HTML template
        as well? Based on object type?

        Consider making all of these attributes property methods instead
        so that I don't have to run an update function.

        NOTE: update method overrides all attributes!
        """

        self.name = obj.name
        self.page_heading = page_heading or self.default_heading()

        # eg. page_image = town if Town object is passed or cave if Cave
        # object is passed.
        self.page_image = obj.type.lower() + '.jpg'
        self.paragraph = paragraph or self.default_paragraph()

    def default_heading(self):
        return "You are in {}".format(self.name)

    def default_paragraph(self):
        return "There are many places to visit within" \
               " the {}. Have a look!".format(self.page_image)

    def update(self):
        """Update self to reflect changes in obj properties.

        This is not automatic ... though maybe it should be.
        Currently you need to define a validator on each object
        that calls this function.

        !IMPORTANT! this could overwrite custom attributes incorrectly.
        """

        if self.page_heading == self.default_heading():
            self.page_heading = "You are in {}".format(self.obj.name)
        if self.paragraph == self.default_paragraph():
            self.paragraph = "There are many places to visit within " \
                             "the {}. Have a look!".format(self.obj.type)

        self.name = self.obj.name
        self.page_image = self.obj.type.lower() + '.jpg'


class AdjacentLocation(Base):
    """Allow for locations to connect to other locations.

    This is done through a in/out path architecture and
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

    The main hierarchy is parent -> child, where children with
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
        'merchant', 'house', 'store', 'barracks', 'marketplace',
        'tavern', 'gate', 'combat', 'spar', 'arena', 'cave_entrance', 'explore_cave'
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
    # Need validator for siblings - can't be parent or child, max of 6?
    # Think a hex grid

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'))
    name = Column(String, nullable=False, unique=True)
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
    heroes = relationship("Hero", back_populates='current_world',
                          foreign_keys='[Hero.map_id]')
    # Each current_location -> can be held by Many Heroes (bidirectional)
    heroes_by_current_location = relationship(
        "Hero", back_populates="current_location",
        foreign_keys='[Hero.current_location_id]')
    # Each current_city -> can be held by Many Heroes (bidirectional)
    # Current_city may be: (town, cave)
    heroes_by_city = relationship(
        "Hero", back_populates="current_city",
        foreign_keys='[Hero.city_id]')

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
        """A list of siblings that can be traveled to.

        This is bidirectional by default but can be changed without
        too much trouble .. I think.
        """
        return set(self._out_adjacent + self._in_adjacent)

    @adjacent.setter
    def adjacent(self, values):
        """Build a path between sibling locations.

        Raise and error if the potential adjacent locations are not siblings
        of this location.
        """
        for value in values:
            if value in self.siblings:
                self._out_adjacent = values
            else:
                raise Exception(
                    "Location.name='{}' is not a valid sibling of this "
                    "location. Try checking the parents of both objects."
                    "".format(value.name)
                )

    # @orm.validates('parent', 'children')
    # def update_siblings(self, key, value):
    #     if key == 'children':
    #         value.update_sibilings()
    #     else:
    #         self.update_siblings()

    @hybrid_property
    def siblings(self):
        """The children of the parent of this location, less this location.

        NOTE: this object is not returned.
        Definition: A sibling is an object with the same parent.
        """
        siblings = []
        if self.parent:
            siblings = list(self.parent.children)
            siblings.remove(self)
        return siblings

    def get_sibling_ids(self):
        """A list of all ids of the siblings of this object.

        """
        return [sibling.id for sibling in self.siblings]

    # @update_after_validate
    @orm.validates('type')
    # @update_after_validate
    def validate_type(self, key, value):
        """Make sure that the programmer doesn't create arbitrary types.

        If you need a new type, add it to Location attribute ALL_TYPES
        """
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

    def __init__(self, name, location_type, parent=None, children=[]):
        """Create a new location object that the hero can explore.

        :param location_type: e.g. map, town, store
        :param parent: the place this place is inside of
        :param children: places inside this place

        NOTE: if you set the parent attribute ... the siblings
        attribute should be populated automatically.

        NOTE2: the url is populated automatically from the parent url
        and this location's type and name.

        NOTE3: the Display is populated automatically as well but can have
        extra information added to it.

        NOTE4: Currently you can't set siblings!

        NOTE5: You need to run 'update' after changing name or type!
        """
        self.name = name
        self.type = location_type
        self.parent = parent
        self.children = children
        self.update()

    @orm.reconstructor
    def update(self):
        """Update the derived attributes to reflect changes to the main ones.

        !IMPORTANT! This could overwrite custom attribute values incorrectly.
        """
        self.url = self.build_url()
        if self.display is None:
            self.display = Display(self)
        else:
            self.display.update()

    def build_url(self):
        """Create a url for this object with its type and name.

        Old: Create a url for this location based on the parent's url.
        """
        url_name = self.name.replace(" ", "%20")
        if self.type == "explore_cave":
            url_name += "/False"
        return "/{}/{}".format(self.type, url_name)
        # if self.parent is None:
        #     return "/{}/{}".format(self.type, self.name)
        # else:
        #     return self.parent.url + "/{}/{}".format(
        #         self.type, self.name)

    @hybrid_property
    def places_of_interest(self):
        """The places that are directly connected to this place.

        This is a dictionary of objects lists.
        The children are those places enclosed by this place.
        The parent is the place this place encloses.
        The adjacent is the locations that you can travel to from here.
            They are on the same relative level as this place.
        """
        places = {'children': [],
                  'adjacent': [],
                  'siblings': [],
                  'parent': None}
        children = sorted(self.children, key=lambda x: x.name)
        places['children'] = sorted(children, key=lambda x: x.type)
        places['adjacent'] = sorted(self.adjacent, key=lambda x: x.name)
        places['siblings'] = sorted(self.siblings, key=lambda x: x.name)

        if self.parent:
            places['parent'] = self.parent
        return places


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



import base_classes
from base_classes import Base
from sqlalchemy import Column, Integer, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import game
import locations
import abilities
import items

#Hero relationships
#Note singular/one side of relationship should be defined first or you will get
#C:\Python35\lib\site-packages\sqlalchemy\orm\mapper.py:1654: SAWarning: 
#Property Hero.inventory on Mapper|Hero|heroes being replaced with new property Hero.inventory;
#the old property will be discarded
game.Hero.user_id = Column(Integer, ForeignKey('users.id'))
game.User.heroes = relationship("Hero", order_by='Hero.character_name', backref='user')

#Many Heroes -> one WorldMap (bidirectional)
game.Hero.world_map_id = Column(Integer, ForeignKey('world_map.id'))
locations.WorldMap.heroes = relationship("Hero", backref="current_world")

#Many Heroes -> one Location (bidirectional) (Town or Cave)
#Maybe I should have a City object that extends Location that is the Ancestor for Town and Cave?
game.Hero.city_id = Column(Integer, ForeignKey('location.id'))
locations.Location.heroes = relationship("Hero", backref="current_city")


#Many Heroes -> many known Maps? (unidirectional)
#Maybe this should be a One Hero -> Many Maps ...
known_locations_association_table = Table('known_locations_association', Base.metadata,
    Column('heroes_id', Integer, ForeignKey('heroes.id')),
    Column('map_id', Integer, ForeignKey('map.id'))
)
game.Hero.known_locations = relationship("Map", secondary=known_locations_association_table)

#One Hero -> many abilities (bidirectional)
abilities.Ability.hero_id = Column(Integer, ForeignKey("heroes.id"))
game.Hero.abilities = relationship("Ability", order_by="Ability.name", backref="myHero")

#One Hero -> many inventory items (bidirectional) Note: (inventory == items)    
#inventory is list of character's items.
items.Item.hero_id = Column(Integer, ForeignKey("heroes.id"))
game.Hero.inventory = relationship("Item", order_by="Item.name", backref="myHero")

#One Hero -> one primary_attribute dict
base_classes.BaseDict.hero_id_primary_attr = Column(Integer, ForeignKey('heroes.id'))
game.Hero.primary_attributes = relationship("BaseDict", uselist=False, 
    foreign_keys="[BaseDict.hero_id_primary_attr]")

#One Hero -> one quest list?
base_classes.BaseDict.hero_id_kill_quests = Column(Integer, ForeignKey('heroes.id'))
game.Hero.kill_quests = relationship("BaseDict", uselist=False,
    foreign_keys="[BaseDict.hero_id_kill_quests]")


#Locations -> base_classes
base_classes.BaseListElement.location_id = Column(Integer, ForeignKey('location.id'))
#relationships
    # display = etc. one to one.
    # location_world one to one with WorldMap? but each WorldMap can have many locations ...?
    #   so many to one it is!
    # adjacent_locations = one to many relationship with self.
locations.Location._adjacent_locations = relationship("BaseListElement")

base_classes.BaseListElement.map_id = Column(Integer, ForeignKey('map.id'))
locations.Map._adjacent_locations = relationship("BaseListElement")


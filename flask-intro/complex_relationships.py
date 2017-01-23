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


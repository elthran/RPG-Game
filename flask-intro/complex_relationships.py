from sqlalchemy import Column, Integer, String, Boolean
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
#Many Heroes -> one World_Map (bidirectional)
game.Hero.world_map_id = Column(Integer, ForeignKey('world_map.id'))
game.Hero.current_world = relationship("World_Map", back_populates="heroes")
locations.World_Map.heroes = relationship("Hero", back_populates="current_world")

#Many Heroes -> one Town (bidirectional)
game.Hero.town_id = Column(Integer, ForeignKey('town.id'))
game.Hero.current_city = relationship("Town", back_populates="heroes")
locations.Town.heroes = relationship("Hero", back_populates="current_city")

#One Hero -> many abilities (bidirectional)
abilities.Ability.hero_id = Column(Integer, ForeignKey("heroes.id"))
abilities.Ability.myHero = relationship("Hero", back_populates="abilities")
game.Hero.abilities = relationship("Ability", order_by="Ability.name", back_populates="myHero")

#One Hero -> many inventory items (bidirectional) Note: (inventory == items)    
#inventory is list of character's items.
items.Item.hero_id = Column(Integer, ForeignKey("heroes.id"))
items.Item.myHero = relationship("Hero", back_populates="inventory")
game.Hero.inventory = relationship("Item", order_by="Item.name", back_populates="myHero")

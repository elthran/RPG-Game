import base_classes
from base_classes import Base
from sqlalchemy import Column, Integer, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy import orm

import game
import locations
import abilities
import items
import quests

import pdb

###########
#Hero relationships
###########
#Note singular/one side of relationship should be defined first or you will get
#C:\Python35\lib\site-packages\sqlalchemy\orm\mapper.py:1654: SAWarning: 
#Property Hero.inventory on Mapper|Hero|heroes being replaced with new property Hero.inventory;
#the old property will be discarded
game.Hero.user_id = Column(Integer, ForeignKey('users.id'))
game.User.heroes = relationship("Hero", order_by='Hero.character_name', backref='user')

#Many Heroes -> one WorldMap (bidirectional)
game.Hero.world_map_id = Column(Integer, ForeignKey('world_map.id'))
locations.WorldMap.heroes = relationship("Hero", backref="current_world")

#Each current_city -> can be held by Many Heroes (bidirectional) (Town or Cave)
#Maybe I should have a City object that extends Location that is the Ancestor for Town and Cave?
#Location -> City -> (Town, Cave)
game.Hero.city_id = Column(Integer, ForeignKey('location.id'))
game.Hero.current_city = relationship("Location", foreign_keys='[Hero.city_id]', 
    back_populates='heroes_by_city')
locations.Location.heroes_by_city = relationship("Hero", foreign_keys='[Hero.city_id]',
    back_populates="current_city")

#Each current_location -> can be held by Many Heroes (bidirectional)
game.Hero.current_location_id = Column(Integer, ForeignKey('location.id'))
game.Hero.current_location = relationship("Location", foreign_keys='[Hero.current_location_id]',
    back_populates='heroes_by_current_location')
locations.Location.heroes_by_current_location = relationship("Hero", 
    foreign_keys='[Hero.current_location_id]', back_populates="current_location")


######NOT TESTED!
#Many Heroes -> many known Maps? (unidirectional)?
#Maybe this should be a One Hero -> Many Maps ...
known_locations_association_table = Table('known_locations_association', Base.metadata,
    Column('heroes_id', Integer, ForeignKey('heroes.id')),
    Column('map_id', Integer, ForeignKey('map.id'))
)
game.Hero.known_locations = relationship("Map", secondary=known_locations_association_table)
###########

abilities_association_table = Table('abilities_association', Base.metadata,
    Column('heroes_id', Integer, ForeignKey('heroes.id')),
    Column('ability_id', Integer, ForeignKey('ability.id'))
)

game.Hero.abilities = relationship("Ability", secondary=abilities_association_table, back_populates="heroes")
abilities.Ability.heroes = relationship("Hero", secondary=abilities_association_table, back_populates="abilities")

#One Hero -> many inventory items (bidirectional) Note: (inventory == items)    
#inventory is list of character's items.
items.Item.hero_id = Column(Integer, ForeignKey("heroes.id"))
game.Hero.inventory = relationship("Item", order_by="Item.name", backref="myHero")

#One Hero -> one primary_attribute dict
game.PrimaryAttribute.hero_id = Column(Integer, ForeignKey('heroes.id'))
game.Hero.primary_attributes = relationship("PrimaryAttribute", uselist=False)

#One Hero -> one quest list?
#Quest list is not quests? So like it should really be Many to Many? Each Hero can have Many Quests
#and each Quest can be held by Many Heroes.
base_classes.BaseDict.hero_id_kill_quests = Column(Integer, ForeignKey('heroes.id'))
base_classes.BaseDict.kill_quests_hero = relationship("Hero", 
    backref=backref("kill_quests", uselist=False), foreign_keys="[BaseDict.hero_id_kill_quests]")
    
    
#Heroes to Quests.
#Hero object relates to quests via active_quests and completed_quests.
#Hero quests can be either active or completed, but not both.
#
#This relationship forms through the QuestPath object.
#Which establishes a manay to many relationship between quests and heroes.
#QuestPath provides many special methods.
quests.QuestPath.hero_id = Column(Integer, ForeignKey('heroes.id'))
quests.QuestPath.quest_id = Column(Integer, ForeignKey('quest.id'))

game.Hero.quest_paths = relationship("QuestPath", backref='hero')
quests.Quest.quest_paths = relationship("QuestPath", backref='quest')


#############
#Location relationships
#############
#Locations -> base_classes
base_classes.BaseListElement.location_id = Column(Integer, ForeignKey('location.id'))
#relationships
    # display = etc. one to one.
    # location_world one to one with WorldMap? but each WorldMap can have many locations ...?
    #   so maybe to one it is!
    # adjacent_locations = one to many relationship with self.
locations.Location._adjacent_locations = relationship("BaseListElement")

############
#Map relationships
############
#One Map -> Many adjacent_locations (BaseListElements)
base_classes.BaseListElement.map_id = Column(Integer, ForeignKey('map.id'))
locations.Map._adjacent_locations = relationship("BaseListElement")


if __name__ == "__main__":
    from sqlalchemy import inspect

    def print_relations(model):
        i = inspect(model)
        for relation in i.relationships:
                print(relation.direction.name)
                print(relation.remote_side)
                print(relation._reverse_property)
                # print(dir(relation))
                
    print_relations(game.Hero)

import base_classes
from base_classes import Base
from sqlalchemy import Column, Integer, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy import orm
from sqlalchemy.ext.orderinglist import ordering_list

import game
import locations
import abilities
import items
import quests
import attributes
import inventory

import pdb
    


###########
#Hero relationships
###########
#Note singular/one side of relationship should be defined first or you will get
#C:\Python35\lib\site-packages\sqlalchemy\orm\mapper.py:1654: SAWarning: 
#Property Hero.inventory on Mapper|Hero|heroes being replaced with new property Hero.inventory;
#the old property will be discarded
game.Hero.user_id = Column(Integer, ForeignKey('user.id'))
game.User.heroes = relationship("Hero", order_by='Hero.character_name', backref='user')

##########
#Heroes and Items (and inventory).
##########
#Each Hero has One inventory. (One to One -> bidirectional)
#inventory is list of character's items. 
game.Hero.inventory_id = Column(Integer, ForeignKey('inventory.id'))
game.Hero.inventory = relationship("Inventory", backref=backref("hero", uselist=False))

#Each ItemTemplate can have many regular Items.
items.ItemTemplate.items = relationship("Item", backref='template')
items.Item.item_template_id = Column(Integer, ForeignKey('item_template.id'))

#One Hero -> one Attributes object
game.Hero.attributes_id = Column(Integer, ForeignKey('attributes.id'))
game.Hero.attributes = relationship("Attributes", uselist=False)

#One Hero -> one Proficiencies object
game.Hero.proficiencies_id = Column(Integer, ForeignKey('proficiencies.id'))
game.Hero.proficiencies = relationship("Proficiencies", uselist=False)

#Heroes to Quests.
#Hero object relates to quests via the QuestPath object.
#This path may be either active or completed, but not both. 
#Which establishes a manay to many relationship between quests and heroes.
#QuestPath provides many special methods.
quests.QuestPath.hero_id = Column(Integer, ForeignKey('hero.id'))
quests.QuestPath.quest_id = Column(Integer, ForeignKey('quest.id'))

game.Hero.quest_paths = relationship("QuestPath", backref='hero')
quests.Quest.quest_paths = relationship("QuestPath", backref='quest')


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

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
#User relationships
###########
#Each user can have one inbox. One to One (bidirectional).
game.User.inbox_id = Column(Integer, ForeignKey('inbox.id'))
game.User.inbox = relationship("Inbox", backref=backref("user", uselist=False))


###########
#Message relationships
###########
#Each user can send or receive multiple messages. One to Many (bi).
game.Message.sender_id = Column(Integer, ForeignKey('inbox.id'))
game.Message.sender = relationship("Inbox", backref="sent_messages",
    foreign_keys="[Message.sender_id]")
game.Message.receiver_id = Column(Integer, ForeignKey('inbox.id'))
game.Message.receiver = relationship("Inbox", backref="received_messages",
    foreign_keys="[Message.receiver_id]")

    
###########
#Inventory relationships
###########
#One to One
inventory.Inventory.helmet_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.helmet = relationship("Item", backref=backref("inventory_helmet",
    uselist=False), foreign_keys="[Inventory.helmet_item_id]")
inventory.Inventory.shirt_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.shirt = relationship("Item", backref=backref("inventory_shirt",
    uselist=False), foreign_keys="[Inventory.shirt_item_id]")
inventory.Inventory.left_hand_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.left_hand = relationship("Item", backref=backref("inventory_left_hand",
    uselist=False), foreign_keys="[Inventory.left_hand_item_id]")
inventory.Inventory.right_hand_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.right_hand = relationship("Item", backref=backref("inventory_right_hand",
    uselist=False), foreign_keys="[Inventory.right_hand_item_id]")
inventory.Inventory.both_hands_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.both_hands = relationship("Item", backref=backref("inventory_both_hands",
    uselist=False), foreign_keys="[Inventory.both_hands_item_id]")
inventory.Inventory.sleeves_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.sleeves = relationship("Item", backref=backref("inventory_sleeves",
    uselist=False), foreign_keys="[Inventory.sleeves_item_id]")
inventory.Inventory.gloves_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.gloves = relationship("Item", backref=backref("inventory_gloves",
    uselist=False), foreign_keys="[Inventory.gloves_item_id]")
inventory.Inventory.legs_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.legs = relationship("Item", backref=backref("inventory_legs",
    uselist=False), foreign_keys="[Inventory.legs_item_id]")
inventory.Inventory.feet_item_id = Column(Integer, ForeignKey('item.id'))
inventory.Inventory.feet = relationship("Item", backref=backref("inventory_feet",
    uselist=False), foreign_keys="[Inventory.feet_item_id]")
#One to Many
items.Item.rings_inventory_id = Column(Integer, ForeignKey('inventory.id'))
items.Item.rings_position = Column(Integer)
inventory.Inventory.rings = relationship("Item", order_by="Item.rings_position",
    collection_class=ordering_list("rings_position"),
    backref=backref("inventory_rings"), foreign_keys="[Item.rings_inventory_id]")
items.Item.unequipped_inventory_id = Column(Integer, ForeignKey('inventory.id'))
items.Item.unequipped_position = Column(Integer)
inventory.Inventory.unequipped = relationship("Item", order_by="Item.unequipped_position",
    collection_class=ordering_list("unequipped_position"),
    backref=backref("inventory_unequipped"), foreign_keys="[Item.unequipped_inventory_id]")

###########
#Hero relationships
###########
#Note singular/one side of relationship should be defined first or you will get
#C:\Python35\lib\site-packages\sqlalchemy\orm\mapper.py:1654: SAWarning: 
#Property Hero.inventory on Mapper|Hero|heroes being replaced with new property Hero.inventory;
#the old property will be discarded
game.Hero.user_id = Column(Integer, ForeignKey('user.id'))
game.User.heroes = relationship("Hero", order_by='Hero.character_name', backref='user')

######NOT TESTED!
#Many Heroes -> many known Maps? (unidirectional)?
#Maybe this should be a One Hero -> Many Maps ...
# known_locations_association_table = Table('known_locations_association', Base.metadata,
#     Column('hero_id', Integer, ForeignKey('hero.id')),
#     Column('map_id', Integer, ForeignKey('map.id'))
# )
# game.Hero.known_locations = relationship("Map", secondary=known_locations_association_table)
###########

# abilities_association_table = Table('abilities_association', Base.metadata,
#     Column('hero_id', Integer, ForeignKey('hero.id')),
#     Column('ability_id', Integer, ForeignKey('ability.id'))
# )
#
# game.Hero.abilities = relationship("Ability", secondary=abilities_association_table, back_populates="heroes")
# abilities.Ability.heroes = relationship("Hero", secondary=abilities_association_table, back_populates="abilities")

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

#Marked for restructure. Remove in favor of quest object.
#Maybe make a special "KillQuest" quest type?
#One Hero -> one quest list?
#Quest list is not quests? So like it should really be Many to Many? Each Hero can have Many Quests
#and each Quest can be held by Many Heroes.
# base_classes.BaseDict.hero_id_kill_quests = Column(Integer, ForeignKey('hero.id'))
# base_classes.BaseDict.kill_quests_hero = relationship("Hero", 
    # backref=backref("kill_quests", uselist=False), foreign_keys="[BaseDict.hero_id_kill_quests]")
    
    
#Heroes to Quests.
#Hero object relates to quests via the QuestPath object.
#This path may be either active or completed, but not both. 
#Which establishes a manay to many relationship between quests and heroes.
#QuestPath provides many special methods.
quests.QuestPath.hero_id = Column(Integer, ForeignKey('hero.id'))
quests.QuestPath.quest_id = Column(Integer, ForeignKey('quest.id'))

game.Hero.quest_paths = relationship("QuestPath", backref='hero')
quests.Quest.quest_paths = relationship("QuestPath", backref='quest')


#############
#Location relationships
#############
#Locations -> base_classes
# base_classes.BaseListElement.location_id = Column(Integer, ForeignKey('location.id'))
#relationships
    # display = etc. one to one.
    # location_world one to one with WorldMap? but each WorldMap can have many locations ...?
    #   so maybe to one it is!
    # adjacent_locations = one to many relationship with self.
# locations.Location._adjacent_locations = relationship("BaseListElement")

############
#Map relationships
############
#One Map -> Many adjacent_locations (BaseListElements)
# base_classes.BaseListElement.map_id = Column(Integer, ForeignKey('map.id'))
# locations.Map._adjacent_locations = relationship("BaseListElement")


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
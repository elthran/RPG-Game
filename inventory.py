from sqlalchemy import Column, Integer, String
from sqlalchemy import orm
from base_classes import Base

import pdb

class Inventory(Base):
    """Store a list of items for the hero.

    This is a special class that will allow me to do more natural pythonic operations
    on a list of items. In theory. Sort of a 'wrapper' I guess?
    """
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)

    #Marked for restructuring as causes conflics with multiple heroes?
    #As in if hero1 has 4 of an item then hero2 will as well?
    #Move to Inventory?
    ##amount_owned = Column(Integer)
    # Maybe I don't even need this at all?
    
    slots_used_by_item_type = {
        "Two_Handed_Weapon": ["left_hand", "right_hand", "both_hands"],
        "One_Handed_Weapon": ["right_hand"],
        "Shield": ["left_hand"],
        "Chest_Armour": ["shirt"],
        "Head_Armour": ["helmet"],
        "Leg_Armour": ["legs"],
        "Feet_Armour": ["feet"],
        "Arm_Armour": ["sleeves"],
        "Hand_Armour": ["gloves"],
        "Ring": ["rings"],
    
    }
    
    all_slot_names = [
        "helmet",
        "shirt",
        "left_hand",
        "right_hand",
        "both_hands",
        "sleeves",
        "gloves",
        "rings",
        "legs",
        "feet",
        "unequipped",
    ]
    
    single_slots = [
        "helmet",
        "shirt",
        "left_hand",
        "right_hand",
        "both_hands",
        "sleeves",
        "gloves",
        "legs",
        "feet",
    ]
    
    multiple_slots = [
        "rings",
        "unequipped",
    ]
    
    def slots(self, name, value=0):
        """Return the value of an attribute by its name.
        
        eg. self.slots("legs") -> self.legs
        """
        if value != 0:
            setattr(self, name, value)
        return getattr(self, name)


    def equip_all(self, equipped_items):
        """Equip all passed items.
        
        This is normally done on Inventory reload.
        NOTE: If there are slot conflicts they won't be resolved.
        """
        for item in equipped_items:
            self.equip(item)
            
    # @orm.validates(*single_slots)
    # def equip_one_to_one(self, key, value):
        # """When new helmet is added move old one to unequipped.

        # """
        # item = self.slots(key)
        # if item:
            # self.unequipped.append(item)
        # self.slots(key, value)
        # pdb.set_trace()
        
    # @orm.validates("rings")
    # def equip_ring(self, key, value):
        # if name == "rings" and len(self.rings) <= 10:
                # self.rings.append(item)

    def equip(self, item):
        """Equip the passed item in the correct slot.

        Unequip the item it the currently in the slot if one exists.
        For rings ... unequip the first ring equiped once 10 rings are equipped.
        
        id -> the ids of the items that are going to be unequip when a new item is equip.
        """
        slots_used = Inventory.slots_used_by_item_type[item.type]
        
        ids_of_items_unequip = self.unequip_slots(slots_used)
        
        item.equipped = True
        self.add_to_slots(slots_used, item)
        # for name in slots_used:
            # if name == "rings" and len(self.rings) >= 10:
                # id = self.unequip_slot(name)
            # elif name in Inventory.single_slots:
                # id = self.unequip_slot(name)
            # else:
                # id = self.unequip_slot(name, is_list=True)
                # self.slots(name).append(item)
            # if id:
                # yield id
                
    
    def unequip_slots(self, name, index=0, is_list=True):
        """Unequip the item located in slot name.
        
        Optional index is for rings.
        """
        try:
            if is_list:
                item = self.slots(name).pop(index)
                item.equipped = False
                return item.id
            else:
                item = self.slots(name)
                self.slots(name, None)
                item.equipped = False
        except (AttributeError, IndexError):
                pass
                
        
    def unequip(self, item):
        """Unequip the passed item and free up the slots it used.
        """
        
        slots_names = Inventory.slots_used_by_item_type[item.type]
        for name in slots_names:
            if name == "rings":
                index = self.rings.index(item)
                self.unequip_slot(name, index)
            else:
                self.unequip_slot(name)


    def add_item(self, item):
        self.unequipped.append(item)

    def __iter__(self):
        items = []
        for name in self.slot_names:
            if name in Inventory.single_slots:
                items.append(self.slots(name))
            elif name in Inventory.multiple_slots:
                items += self.slots(name)
        return items


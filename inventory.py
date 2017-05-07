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
    
    item_type_to_slots = {
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


    @orm.reconstructor
    def init_on_load(self):
        self.left_hand = []
        self.right_hand = []
        self.both_hands = []
        self.shirt = []
        self.helmet = []
        self.legs = []
        self.feet = []
        self.sleeves = []
        self.gloves = []
        self.rings = []
        
        self.slots = {
            "left_hand": self.left_hand,
            "right_hand": self.right_hand,
            "both_hands": self.both_hands,
            "shirt": self.shirt,
            "helmet": self.helmet,
            "legs": self.legs,
            "feet": self.feet,
            "sleeves": self.sleeves,
            "gloves": self.gloves,
            "rings": self.rings,
        }
        
        self.equip_all((item for item in self.items if item.equipped))

    def equip_all(self, equipped_items):
        """Equip all passed items.
        
        This is normally done on Inventory reload.
        NOTE: If there are slot conflicts they won't be resolved.
        """
        for item in equipped_items:
            self.equip(item)

    def equip(self, item):
        """Equip the passed item in the correct slot.

        Unequip the item it the currently in the slot if one exists.
        For rings ... unequip the first ring equiped once 10 rings are equipped.
        """
        item.equipped = True
        slot_names = self.item_type_to_slots[item.type]
        for name in slot_names:
            if name == "rings" and len(self.rings) <= 10:
                self.rings.append(item)
            else:
                self.unequip_slot(name)
                self.slots[name].append(item)
    
    def unequip_slot(self, name, index=0):
        """Unequip the item located in slot name.
        
        Optional index is for rings.
        """
        try:
            item = self.slots[name].pop(index)
            item.equipped = False
        except (AttributeError, IndexError):
            pass
        
        
    def unequip(self, item):
        """Unequip the passed item and free up the slots it used.
        """
        
        slots_names = self.item_type_to_slots[item.type]
        for name in slots_names:
            if name == "rings":
                index = self.rings.index(item)
                self.unequip_slot(name, index)
            else:
                self.unequip_slot(name)


    def add_item(self, item):
        self.items.append(item)

    def __iter__(self):
        return (item for item in self.items)


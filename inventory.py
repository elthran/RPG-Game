from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from base_classes import Base
from sqlalchemy.orm.session import object_session

import pdb
import warnings


class Inventory(Base):
    """Store a list of items for the hero.

    This is a special class that will allow me to do more natural pythonic operations
    on a list of items. In theory. Sort of a 'wrapper' I guess?

    Considering:
        Move "slot" implementation to HTML and just have a list of equipped and unequipped
        items in inventory?
    """
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)

    # Marked for restructuring as causes conflics with multiple heroes?
    # As in if hero1 has 4 of an item then hero2 will as well?
    # Move to Inventory?
    # amount_owned = Column(Integer)
    # Maybe I don't even need this at all?

    # Relationships
    # Each Hero has One inventory. (One to One -> bidirectional)
    # inventory is list of character's items.
    hero = relationship("Hero", back_populates='inventory', uselist=False)

    # Item relationships
    # One to One
    head = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='HeadArmour')", uselist=False)

    chest = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='ChestArmour')", uselist=False)

    left_hand = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='Shield')", uselist=False)

    right_hand = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='OneHandedWeapon')", uselist=False)

    both_hands = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='TwoHandedWeapon')", uselist=False)

    arm = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='ArmArmour')", uselist=False)

    hand = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='HandArmour')", uselist=False)

    leg = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='LegArmour')", uselist=False)

    foot = relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='FootArmour')", uselist=False)

    # One to many
    rings = relationship(
        "Item", order_by="Item.rings_position",
        collection_class=ordering_list("rings_position"),
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped,"
                    "Item.type=='Ring')")

    unequipped = relationship(
        "Item", order_by="Item.unequipped_position",
        collection_class=ordering_list("unequipped_position"),
        back_populates='inventory',
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped==False)")

    equipped = relationship(
        "Item", order_by="Item.id",
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped==True)")

    slots_used_by_item_type = {
        "TwoHandedWeapon": {"both_hands", "left_hand", "right_hand"},
        "OneHandedWeapon": {"right_hand", "both_hands"},
        "Shield": {"left_hand", "both_hands"},
        "ChestArmour": {"chest"},
        "HeadArmour": {"head"},
        "LegArmour": {"leg"},
        "FootArmour": {"foot"},
        "ArmArmour": {"arm"},
        "HandArmour": {"hand"},
        # "Ring": {"primary": "rings", "secondary": []},

    }

    single_slots = [
        "head",
        "chest",
        # "shoulder",
        # "neck",
        "arm",
        "hand",
        # rings?? left-finger, right-finger
        # "waist",
        "leg",
        "foot",
        "left_hand",
        "right_hand",
        "both_hands",
    ]

    multiple_slots = [
        "rings",
        "unequipped",
    ]

    all_slot_names = single_slots + multiple_slots
    js_single_slots = [(slot.replace('_', '-'), slot) for slot in single_slots
                       if slot != 'both_hands']

    # def equip_all(self, equipped_items):
    #     """Equip all passed items.
    #
    #     I don't know when this would be used ...
    #     NOTE: If there are slot conflicts they won't be resolved.
    #     """
    #     for item in equipped_items:
    #         self.equip(item)

    def equip(self, item, index=0):
        """Equip the an item in the correct slot -> Return ids of items replaced.

        Unequip the items in the slots used if any exist.
        NOTES:
            Max 10 rings are equipped at any given time
            Some items take up multiple slots e.g. a TwoHandedWeapon takes up 3 slots.

        I must:
            1. remove and item from a slot.
            2. commit the change (using object_session)
            3. add new item to slot.

        NOTE: Id of the passed item is not returned.
        """

        # This should never happen ... but prevent it if it does.
        if item.type == "Ring" and not 0 <= index <= 9:
            raise IndexError("'Ring' index out of range. Index must be from 0 to 9.")

        if item.type in Inventory.slots_used_by_item_type:
            slots_used = Inventory.slots_used_by_item_type[item.type]

        # Get reference to current item in this slot (if it exists).
        old_items = []
        if item.type == "Ring":
            if len(self.rings) > index:
                old_items = [self.rings[index]]
                self.unequip(old_items[0])
                item.rings_position = index
            else:
                item.rings_position = len(self.rings)
        else:
            for slot in slots_used:
                old_item = getattr(self, slot)
                if old_item:
                    old_items.append(old_item)
            for old_item in old_items:
                self.unequip(old_item)

        # Finally equip the item (or rather .. make it not unequipped :P)
        item.equipped = True
        item.unequipped_position = None  # May not be needed.
        object_session(self).commit()

        return [item.id for item in old_items]

    def unequip(self, item):
        """Move an item from its current slot to the 'unequipped' slot.

        Does commit (via add_item).
        """

        item.equipped = False  # Might not even need this.
        item.rings_position = None
        self.add_item(item)

    def add_item(self, item):
        """Add an item to the unequipped slot of this inventory.

        Does commit.
        """
        self.unequipped.append(item)
        item.equipped = False
        item.rings_position = None
        object_session(self).commit()

    def remove_item(self, item):
        """Remove a given item from this inventory."""
        item.rings_position = None
        item.equipped = None  # Might be redundant.
        item.inventory_id = None
        object_session(self).commit()

    def __iter__(self):
        """Return an iterator of _all_ items in this inventory.

        Slightly tested.

        Use:
        for item in inventory:
            print(item)
        """
        all_items = self.unequipped + self.equipped
        return (item for item in all_items)


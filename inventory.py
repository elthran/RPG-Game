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
        "Item",
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped==True)")

    slots_used_by_item_type = {
        "TwoHandedWeapon": {"primary": "both_hands", "secondary": ["left_hand", "right_hand"]},
        "OneHandedWeapon": {"primary": "right_hand", "secondary": ["both_hands"]},
        "Shield": {"primary": "left_hand", "secondary": ["both_hands"]},
        "ChestArmour": {"primary": "chest", "secondary": []},
        "HeadArmour": {"primary": "head", "secondary": []},
        "LegArmour": {"primary": "leg", "secondary": []},
        "FootArmour": {"primary": "foot", "secondary": []},
        "ArmArmour": {"primary": "arm", "secondary": []},
        "HandArmour": {"primary": "hand", "secondary": []},
        "Ring": {"primary": "rings", "secondary": []},

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

    def equip_all(self, equipped_items):
        """Equip all passed items.

        I don't know when this would be used ...
        NOTE: If there are slot conflicts they won't be resolved.
        """
        for item in equipped_items:
            self.equip(item)

    def equip(self, item, index=0):
        """Equip the an item in the correct slot -> Return ids of items manipulated.

        Unequip the item it the currently in the slot if one exists.
        NOTES:
            Max 10 rings are equipped at any given time
            Some items take up multiple slots e.g. a TwoHandedWeapon takes up 3 slots.

        Do to problems in my implementation and understanding of SQLAlchemy
        I must:
            1. remove and item from a slot.
            2. commit the change (Black magic method that I shouldn't be using)
            3. add to a new slot.
        I should be able to do a "move" command instead but can't.
        NOTE: Id of the passed item is not returned ... maybe it should be?
        """
        # pdb.set_trace()

        item.equipped = True
        item.unequipped_position = None  # May not be needed.
        session = object_session(self)
        session.commit()
        return

        if item.type == "Ring" and not 0 <= index <= 9:
            raise IndexError("'Ring' index out of range. Index must be from 0 to 9.")
        slots_used = Inventory.slots_used_by_item_type[item.type]

        # Remove item from current location (currently in unequipped)
        self.unequipped.remove(item)
        # Need commit here .. or some kind of auto-flush/update/cascade?
        self._sa_instance_state.session.commit()  # -> black magic.

        # Get reference to current item in this slot (if it exists).
        old_item = None
        if slots_used["primary"] == "rings":
            try:
                old_item = self.rings[index]
                self.rings[index] = item
            except IndexError:
                self.rings.append(item)
        else:
            old_item = getattr(self, slots_used["primary"])

            # Asign new value to slot.
            setattr(self, slots_used["primary"], item)

        # Need commit here .. or some kind of auto-flush/update/cascade?
        self._sa_instance_state.session.commit()  # -> black magic.

        # State should now read -> item in slot ... old item not in slot.
        # I need to check that the old item hasn't be deleted or overwritten.

        # This action should commit naturally.
        ids_of_items_to_be_moved = []
        if old_item:
            if self.unequipped:
                old_item.unequipped_position = self.unequipped[-1].unequipped_position + 1
            self.unequipped.append(old_item)

            ids_of_items_to_be_moved = [old_item.id]
        ids_of_items_to_be_moved += self.unequip_secondary(slots_used["secondary"])

        return ids_of_items_to_be_moved

    def unequip_secondary(self, secondary_slots):
        """Unequip the item located in slot name.

        Rings has no secondary so it should never be sent here. This allows me
        to ignore the whole index thing.
        """
        if "rings" in secondary_slots:
            warnings.warn('Inventory.equip -> unequip_secondary does not accomodate rings yet!')
        ids = []
        for slot in secondary_slots:
            item = getattr(self, slot)
            if item:
                setattr(self, slot, None)
                self._sa_instance_state.session.commit()

                self.unequipped.append(item)
                ids.append(item.id)
        return ids

    def unequip(self, item):
        """Move an item from its current slot to the 'unequipped' slot.
        """

        slot = Inventory.slots_used_by_item_type[item.type]["primary"]
        if slot == "rings":
            self.rings.remove(item)
        else:
            setattr(self, slot, None)

        if self.unequipped:
            item.unequipped_position = self.unequipped[-1].unequipped_position + 1
        self._sa_instance_state.session.commit()

        self.unequipped.append(item)

    def add_item(self, item):
        """Add an item to the unequipped slot of this inventory.
        """
        self.unequipped.append(item)
        session = object_session(self)
        session.commit()

    def __iter__(self):
        """Return an iterator of _all_ items in this inventory.

        Slightly tested.

        Use:
        for item in inventory:
            print(item)
        """

        all_items = [getattr(self, name) for name in Inventory.single_slots
                     if getattr(self, name)]

        multi_items = [getattr(self, name) for name in Inventory.multiple_slots
                       if getattr(self, name)]

        for item_list in multi_items:
            all_items += item_list

        return (item for item in all_items)


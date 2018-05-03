import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.orm.collections
import sqlalchemy.ext.orderinglist

import services
import models
from . import database


class Inventory(models.mixins.SessionHoistMixin, models.Base):
    """Store a list of items for the hero.

    This is a special class that will allow me to do more natural pythonic operations
    on a list of items. In theory. Sort of a 'wrapper' I guess?

    Considering:
        Move "slot" implementation to HTML and just have a list of equipped and unequipped
        items in inventory?

    Items can have have 4 states.
    1. Unequipped:
        item.equipped = False
        item.inventory_id = inventory.id
        item.unequipped_position = x
        item.ring_position = None
    2. Equipped:
        item.equipped = True
        item.inventory_id = inventory.id
        item.unequipped_position = None
        (possibly) item.ring_position = x
    3. Limbo (for items transitioning from one state to the next):
        item.equipped = None
        item.inventory_id = inventory.id
        item.unequipped_position = x or None?
        (possibly) item.ring_position = x or None
    4. Not in an inventory:
        item.equipped = None
        item.inventory_id = None
        item.unequipped_position = None
        item.ring_position = None
    """
    __tablename__ = 'inventory'

    id = sa.Column(sa.Integer, primary_key=True)

    # Marked for restructuring as causes conflics with multiple heroes?
    # As in if hero1 has 4 of an item then hero2 will as well?
    # Move to Inventory?
    # amount_owned = Column(Integer)
    # Maybe I don't even need this at all?

    # Relationships
    # Each Hero has One inventory. (One to One -> bidirectional)
    # inventory is list of character's items.
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship("Hero", back_populates='inventory')

    # Item relationships
    # One to One
    head = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='HeadArmour')", uselist=False)

    chest = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='ChestArmour')", uselist=False)

    left_hand = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='Shield')", uselist=False)

    right_hand = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='OneHandedWeapon')", uselist=False)

    both_hands = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='TwoHandedWeapon')", uselist=False)

    arm = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='ArmArmour')", uselist=False)

    hand = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='HandArmour')", uselist=False)

    leg = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='LegArmour')", uselist=False)

    foot = sa.orm.relationship(
        "Item", primaryjoin="and_(Inventory.id==Item.inventory_id, "
                            "Item.equipped, "
                            "Item.type=='FootArmour')", uselist=False)

    # One to many
    rings = sa.orm.relationship(
        "Item", order_by="Item.ring_position",
        collection_class=sa.orm.collections.attribute_mapped_collection('ring_position'),
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped,"
                    "Item.type=='Ring')")

    unequipped = sa.orm.relationship(
        "Item", order_by="Item.unequipped_position",
        collection_class=sa.ext.orderinglist.ordering_list("unequipped_position"),
        back_populates='inventory',
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped==False)",
        cascade="all, delete-orphan")

    equipped = sa.orm.relationship(
        "Item", order_by="Item.id",
        back_populates='inventory',
        primaryjoin="and_(Inventory.id==Item.inventory_id, "
                    "Item.equipped==True)",
        cascade="all, delete-orphan")

    # !Important! Put primary slot used as the first in the list!
    # I should hav just left it as is with "primary" and "secondary" :P
    slots_used_by_item_type = {
        "TwoHandedWeapon": ["both_hands", "left_hand", "right_hand"],
        "OneHandedWeapon": ["right_hand", "both_hands"],
        "Shield": ["left_hand", "both_hands"],
        "ChestArmour": ["chest"],
        "HeadArmour": ["head"],
        "LegArmour": ["leg"],
        "FootArmour": ["foot"],
        "ArmArmour": ["arm"],
        "HandArmour": ["hand"],
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
    js_single_slots = [(slot.replace('_', '-'), slot) for slot in single_slots]
    js_slots_used_by_item_type = {k: [v.replace('_', '-') for v in l]
                                  for k, l in slots_used_by_item_type.items()}

    def equip_all(self, items):
        """Equip all passed items.

        I don't know when this would be used ...
        NOTE: If there are slot conflicts The last item passed will take
        precedence.
        """
        for item in items:
            self.equip(item)

    @database.sessions.safe_commit_session
    def equip(self, item, index=None):
        """Equip the an item in the correct slot -> Return ids of items replaced.

        Unequip the items in the slots used if any exist.
        NOTES:
            Max 10 rings are equippable at any given time
            Some items take up multiple slots e.g. a TwoHandedWeapon takes
            up 3 slots.

        I must:
            1. remove and item from a slot.
            2. commit the change (using @safe_commit_session)
            3. add new item to slot.

        NOTE: Id of the passed item is not returned.
        NOTE2: if you equip an item ... that item is automatically added to
        this inventory! You can equip without adding the item first.

        Commits changes!
        """

        # This should never happen ... but prevent it if it does.
        if item.type == "Ring" and index and not 0 <= index <= 9:
            self.unequip(item)  # Fail -> send ring to unequipped items.
            raise IndexError("'Ring' index out of range. Index must be from 0 to 9.")

        # Use the 3rd item state. Not equipped and not unequipped.
        # a.k.a. the 'limbo' state!
        # This also allows you to equip an item that has not been added yet.
        self.session.add(item)
        item.inventory_id = self.id
        item.equipped = None
        item.unequipped_position = None
        self.session.commit()

        # TODO understand/refactor slots_used variable.
        if item.type in Inventory.slots_used_by_item_type:
            slots_used = Inventory.slots_used_by_item_type[item.type]

        # Get reference to current item in this slot (if it exists).
        old_items = []
        old_item = None
        if item.type == "Ring":
            # Get lowest empty slot.
            if not index:
                index = self.get_lowest_empty_ring_pos()
            old_item = self.get_ring_at_pos(index)
            if old_item:
                old_items = [old_item]
                self.unequip(old_item)
            # Both of these operations are necessary for the synchronicity of
            # the sacred attribute_mapped_collection to work properly
            item.ring_position = index
            self.rings[index] = item
        else:
            for slot in slots_used:
                old_item = getattr(self, slot)
                if old_item:
                    old_items.append(old_item)
            for old_item in old_items:
                self.unequip(old_item)

        # Finally move the item from Limbo to Equip state.
        item.equipped = True
        self.session.commit()

        return [item.id for item in old_items]

    def unequip(self, item):
        """Move an item from its current slot to the 'unequipped' slot.

        Basically re-add this item as though it was never in this inventory.
        Fixes lots of bugs even though the efficiencies might be poor.

        Commits changes (via add_item).
        """

        self.add_item(item)

    @ database.sessions.safe_commit_session
    def add_item(self, item):
        """Add an item to the unequipped slot of this inventory.

        Adds item to the end of the unequipped list.
        Commits changes.
        """

        # First remove the current item from any inventories it might be in.
        # And reset it to totally unequipped.
        # Then commit, otherwise it might still have a handler in another
        # location.
        self.session.add(item)
        self.remove_item(item)

        self.unequipped.reorder()  # Reorder might do a commit?
        self.unequipped.append(item)
        item.equipped = False  # Required to add this to the unequipped list.

    @ database.sessions.safe_commit_session
    def remove_item(self, item):
        """Remove a given item from any inventory it might be in."""
        item.ring_position = None
        item.equipped = None
        item.unequipped_position = None
        item.inventory_id = None

    def get_ring_at_pos(self, n):
        """Return the ring on this finger or None if none there.

        This is just an error handled version of:
            self.rings[n] (rings is now a dictionary)
        """
        try:
            return self.rings[n]
        except KeyError:
            return None

    def get_lowest_empty_ring_pos(self):
        """If there is an empty slot in the ring dictionary return it.

        Returns the first position from 0-9 that has no ring in it.
        Returns last position if there are no gaps.
        """

        for n in range(len(self.rings)):
            try:
                self.rings[n]
            except KeyError:
                return n
        return 9  # The highest ring.

    def _clear_inventory(self):
        """Disconnect all items from this inventory.

        Internal method for running tests.
        """
        for item in self:
            self.remove_item(item)

    def __iter__(self):
        """Return an iterator of _all_ items in this inventory.

        Slightly tested.

        Use:
        for item in inventory:
            print(item)
        """
        all_items = self.unequipped + self.equipped
        return (item for item in all_items)

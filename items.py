# for testing
from pprint import pprint
import pdb

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from factories import TemplateMixin
import proficiencies
from sqlalchemy.orm.collections import attribute_mapped_collection
from session_helpers import SessionHoistMixin, safe_commit_session
from base_classes import Base
"""
Item Specification:
    All hero specific attributes must be moved from the Template classes.
    Or maybe InventoryItem which relates to Hero by inventory.
    Hero.inventory = relations 1 to many with InventoryItem.
    Item.inventory = relation many to many with inventoryItem.
    Things like:
        -durability (item)
        -amount_owned (inventory)
        -broken (item)
        -consumed (unless consumable just removes the item) 
            (item, may cause two columns in inventory)
        -equipped true/false
"""


class Item(TemplateMixin, SessionHoistMixin, Base):
    """Represent an unique version of an item or the template to create one.

    Each item exists in only one place.
    Each item can be placed in an inventory to belong to a hero.
    Each item is built from a template of the same name.

    How to use:
    name : Name of the Item, e.x. "power bracelet"
    hero : The Hero who owns the item
    buy_price : Price to buy the item
    level_req : level requirement
    """
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    image = Column(String(50))
    buy_price = Column(Integer)
    type = Column(String(50))

    broken = Column(Boolean)
    consumable = Column(Boolean)
    consumed = Column(Boolean)
    item_rating = Column(Integer)
    garment = Column(Boolean)
    weapon = Column(Boolean)
    jewelry = Column(Boolean)
    max_durability = Column(Integer)
    wearable = Column(Boolean)

    # Relationships
    # Each Item can have only one Inventory
    inventory_id = Column(Integer, ForeignKey('inventory.id',
                                              ondelete="CASCADE"))
    inventory = relationship(
        "Inventory", foreign_keys="[Item.inventory_id]")

    # Item to Proficiency is One to Many
    proficiencies = relationship(
        "Proficiency",
        collection_class=attribute_mapped_collection('name'),
        back_populates='items',
        cascade="all, delete-orphan")

    equipped = Column(Boolean)
    ring_position = Column(Integer)
    unequipped_position = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': "Item",
        'polymorphic_on': type
    }

    def __init__(self, name, buy_price, proficiency_data=[], template=False):
        self.name = name
        self.buy_price = buy_price

        # Initialize proficiencies
        for class_name, arg_dict in proficiency_data:
            Class = getattr(proficiencies, class_name)
            # pdb.set_trace()
            obj = Class(**arg_dict, template=template)
            self.proficiencies[obj.name] = obj

        self.template = template

    @safe_commit_session
    def build_new_from_template(self):
        if not self.template:
            raise Exception("Only use this method if obj.template == True.")
        keys = self.__class__.__table__.columns.keys()
        keys.remove('id')
        keys.remove('template')

        # I don't think these should have any value? So copying them
        # shouldn't do anything ...
        # relationship_keys = [
        #     'ring_position',
        #     'unequipped_position'
        # ]
        # for relationship_key in relationship_keys:
        #     keys.remove(relationship_key)
        item = self.__class__(self.name, self.buy_price, template=False)
        for key in keys:
            try:
                setattr(item, key, getattr(self, key))
            except AttributeError:
                pass
        for key, prof in self.proficiencies.items():
            item.proficiencies[key] = prof.build_new_from_template()
        return item

    @property
    def armour_value(self):
        try:
            return self.proficiencies['defence'].get_final()
        except KeyError:
            return 0

    def is_equipped(self):
        # Untested!
        return (self.unequipped_position is None
                and self.inventory_id is not None)

    def update_stats(self, hero):
        """Update hero to reflect stat values with item equiped.

        Will fail and will need to be in Inventory?
        """
        if self.broken:
            return None
        hero.refresh_proficiencies()

    # Both of these need to be modified. I am not sure how to make
    # Each item in an inventory set the correct inventory id ... while
    # having and individual slot.
    # def check_if_improvement(self):
    #     # warnings.warn("Not implemented yet!", RuntimeWarning)
    #     # return # Do nothing
    #     self.improvement = True
    #     for equipped_item in self.inventory.hero.equipped_items:
    #         if equipped_item.type is self.type:
    #             if equipped_item.item_rating > self.item_rating:
    #                 self.improvement = False
    #             break
    #
    # def update_owner(self, hero):
    #     self.inventory.hero = hero


# Subclass of Item
class Wearable(Item):
    style = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': "Wearable",
    }

    def __init__(self, *args, max_durability=3, item_rating=10,
                 style="leather", **kwargs):
        super().__init__(*args, **kwargs)
        self.wearable = True
        self.broken = False
        self.garment = False
        self.weapon = False
        self.jewelry = False
        self.style = style
        self.max_durability = max_durability
        self.item_rating = item_rating


# Subclass of Item
class Weapon(Wearable):
    one_handed_weapon = Column(Boolean)
    shield = Column(Boolean)
    two_handed_weapon = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "Weapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weapon = True
        self.one_handed_weapon = True
        self.shield = False
        self.two_handed_weapon = False


class OneHandedWeapon(Weapon):
    __mapper_args__ = {
        'polymorphic_identity': "OneHandedWeapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Shield(Weapon):
    __mapper_args__ = {
        'polymorphic_identity': "Shield",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shield = True


class TwoHandedWeapon(Weapon):
    __mapper_args__ = {
        'polymorphic_identity': "TwoHandedWeapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.one_handed_weapon = False
        self.two_handed_weapon = True


class Garment(Wearable):
    __mapper_args__ = {
        'polymorphic_identity': "Garment",
    }

    def __init__(self, *args, armour_value=1, **kwargs):
        """Create a new garment template.

        Alternate possible armour syntax:
            [("Defence", {'base': 25})]
        """
        super().__init__(*args, **kwargs)
        self.garment = True
        self.proficiencies['defence'] = proficiencies.Defence(
            base=armour_value, template=True)


class HeadArmour(Garment):
    head_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "HeadArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_armour = True


class ShoulderArmour(Garment):
    shoulder_armour = Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity': "ShoulderArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shoulder_armour = True


class ChestArmour(Garment):
    chest_armour = Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity': "ChestArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chest_armour = True


class LegArmour(Garment):
    leg_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "LegArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leg_armour = True


class FootArmour(Garment):
    foot_armour = Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity': "FootArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.foot_armour = True


class ArmArmour(Garment):
    arm_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "ArmArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arm_armour = True


class HandArmour(Garment):
    hand_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "HandArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_armour = True


# New Class
class Jewelry(Wearable):
    __mapper_args__ = {
        'polymorphic_identity': "Jewelry",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jewelry = True


class Ring(Jewelry):
    ring = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "Ring",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ring = True

    def update_stats(self, hero):
        pass


# Subclass of Item
class Consumable(Item):
    healing_amount = Column(Integer)
    sanctity_amount = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': "Consumable",
    }

    def __init__(self, *args, healing_amount=0, sanctity_amount=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.healing_amount = healing_amount
        self.sanctity_amount = sanctity_amount
        self.consumable = True
        self.consumed = False

    def apply_effect(self, hero):
        # hero.health += self.healing_amount
        # hero.sanctity += self.sanctity_amount
        # if hero.health > hero.health_maximum:
        # hero.health = hero.health_maximum
        # if hero.sanctity > hero.max_sanctity:
        # hero.sanctity = hero.max_sanctity
        print("Applied item effect. But not really.")


# New Class
class QuestItem(Item):
    quest_item = Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity': "QuestItem",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quest_item = True

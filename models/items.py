# for testing

import sqlalchemy as sa
import sqlalchemy.orm
import flask
# from flask import render_template_string

import models.mixins
from . import database

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


class Item(models.mixins.TemplateMixin, models.Base):
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
    name = sa.Column(sa.String(50))
    image = sa.Column(sa.String(50))
    buy_price = sa.Column(sa.Integer)
    type = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))

    broken = sa.Column(sa.Boolean)
    consumable = sa.Column(sa.Boolean)
    consumed = sa.Column(sa.Boolean)
    item_rating = sa.Column(sa.Integer)
    garment = sa.Column(sa.Boolean)
    weapon = sa.Column(sa.Boolean)
    jewelry = sa.Column(sa.Boolean)
    max_durability = sa.Column(sa.Integer)
    wearable = sa.Column(sa.Boolean)
    damage_type = sa.Column(sa.String(50))

    # extra special :P
    affinity = sa.Column(sa.Integer, default=0)

    # Relationships
    # Each Item can have only one Inventory
    inventory_id = sa.Column(sa.Integer, sa.ForeignKey('inventory.id', ondelete="CASCADE"))
    inventory = sa.orm.relationship(
        "Inventory", foreign_keys="[Item.inventory_id]")

    # Item to Proficiency is One to Many
    proficiencies = sa.orm.relationship(
        "Proficiency",
        collection_class=models.attribute_mapped_dict_hybrid('name'),
        back_populates='items',
        cascade="all, delete-orphan")

    equipped = sa.Column(sa.Boolean)
    ring_position = sa.Column(sa.Integer)
    unequipped_position = sa.Column(sa.Integer)

    __mapper_args__ = {
        'polymorphic_identity': "Item",
        'polymorphic_on': type
    }

    def __init__(self, name, buy_price, description="A small item.", proficiency_data=(), template=False):
        self.name = name
        self.buy_price = buy_price
        self.description = description

        # Initialize proficiencies
        for class_name, arg_dict in proficiency_data:
            class_ = getattr(models.proficiencies, class_name)
            # pdb.set_trace()
            obj = class_(**arg_dict, template=template)
            self.proficiencies[obj.name] = obj

        self.template = template

    @database.sessions.safe_commit_session
    def clone(self):
        if not self.template:
            raise Exception("Only use this method if obj.template == True.")
        # noinspection PyUnresolvedReferences
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
            item.proficiencies[key] = prof.clone()
        return item

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
        # hero.refresh_proficiencies()

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

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """

        temp = """<h2>{{ item.name }}</h2><p>{{ item.description }}</p><ul>
        {% for prof in item.proficiencies %}
        {% if prof.base != 0 %}<li> - {{ prof.display_name }}: +{{ prof.base }}</li>{% endif %}
        {% if prof.modifier != 0 %}<li> - {{ prof.display_name }}: +{{ prof.modifier }}%</li>{% endif %}
        {% endfor %}</ul>"""
        return flask.render_template_string(temp, item=self)


# Subclass of Item
class Wearable(Item):
    style = sa.Column(sa.String(50))

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "Wearable",
    }

    def __init__(self, *args, max_durability=3, item_rating=10, damage_type="Unarmed",
                 style="leather", **kwargs):
        super().__init__(*args, **kwargs)
        self.wearable = True
        self.broken = False
        self.garment = False
        self.weapon = False
        self.jewelry = False
        self.style = style  # Used to determine the display image. It's a prefix added to the item.
        self.max_durability = max_durability
        self.item_rating = item_rating
        self.damage_type = damage_type


# Subclass of Item
class Weapon(Wearable):
    one_handed_weapon = sa.Column(sa.Boolean)
    shield = sa.Column(sa.Boolean)
    two_handed_weapon = sa.Column(sa.Boolean)

    __tablename__ = None
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
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "OneHandedWeapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Shield(Weapon):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "Shield",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shield = True


class TwoHandedWeapon(Weapon):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "TwoHandedWeapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.one_handed_weapon = False
        self.two_handed_weapon = True


class Garment(Wearable):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "Garment",
    }

    def __init__(self, *args, **kwargs):
        """Create a new garment template.

        Alternate possible armour syntax:
            [("Defence", {'base': 25})]
        """
        super().__init__(*args, **kwargs)
        self.garment = True


class HeadArmour(Garment):
    head_armour = sa.Column(sa.Boolean)

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "HeadArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_armour = True


class ShoulderArmour(Garment):
    shoulder_armour = sa.Column(sa.Boolean)
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "ShoulderArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shoulder_armour = True


class ChestArmour(Garment):
    chest_armour = sa.Column(sa.Boolean)
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "ChestArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chest_armour = True


class LegArmour(Garment):
    leg_armour = sa.Column(sa.Boolean)

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "LegArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leg_armour = True


class FootArmour(Garment):
    foot_armour = sa.Column(sa.Boolean)
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "FootArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.foot_armour = True


class ArmArmour(Garment):
    arm_armour = sa.Column(sa.Boolean)

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "ArmArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arm_armour = True


class HandArmour(Garment):
    hand_armour = sa.Column(sa.Boolean)

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "HandArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_armour = True


# New Class
class Jewelry(Wearable):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "Jewelry",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jewelry = True


class Ring(Jewelry):
    ring = sa.Column(sa.Boolean)

    __tablename__ = None
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
    healing_amount = sa.Column(sa.Integer)
    sanctity_amount = sa.Column(sa.Integer)

    __tablename__ = None
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
    quest_item = sa.Column(sa.Boolean)
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "QuestItem",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quest_item = True

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base
from factories import TemplateMixin

import warnings
import pdb

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
        -consumed (unless consumable just removes the item) (item, may cause two columns in inventory)
        -equipped true/false
"""


class Item(TemplateMixin, Base):
    """Represent an unique version of an item.

    Each item exists in only one place. Each item can be place in an inventory to belong
    to a hero.

    Each item has a template that it links to. Templates are not modifiable.

    All attributes of a item should be item specific. Such as durability
    or whether the item is broken. All generic attributes will mearly link to the
    items template.
    """
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)

    # template = relationship(ItemTemplate) -> One to Many
    durability = Column(Integer)
    broken = Column(Boolean)
    consumed = Column(Boolean)
    name = Column(String)

    # Relationships
    # Inventory
    # One to Many
    rings_inventory_id = Column(Integer, ForeignKey('inventory.id'))
    rings_position = Column(Integer)

    unequipped_inventory_id = Column(Integer, ForeignKey('inventory.id'))
    unequipped_position = Column(Integer)

    # ItemTemplate
    # Each ItemTemplate can have many regular Items.
    item_template_id = Column(Integer, ForeignKey('item_template.id'))
    template = relationship("ItemTemplate", back_populates='items')

    def __init__(self, template):
        """Build a new item from a given template.

        Set initial values for item attributes. of
        """
        self.template = template
        self.name = template.name

        # Should be a current_durability value as well?
        try:
            self.durability = template.max_durability
        except AttributeError:
            pass
        self.broken = False
        self.consumed = False

        self.load_template()

    @orm.reconstructor
    def load_template(self):
        """Load all the attributes of a given template into this item.

        This loads all keys for each object in the method resolution order (MRO)
        of the template and then removes things like relationships, ids and
        all keys already in this item. All private/internal variables are removed as well.

        Perhaps this should only occur once? instead of during load?
        """

        template_keys = set()

        # All non-base objects in inheritance path.
        # Remove <class 'sqlalchemy.ext.declarative.api.Base'>, <class 'object'> as these are
        # the last two objects in the MRO
        hierarchy = type(self.template).__mro__
        max_index = hierarchy.index(Base)
        hierarchy = hierarchy[:max_index]

        for obj in hierarchy:
            template_keys |= set(vars(obj).keys()) - set(obj.__mapper__.relationships.keys())

        template_keys -= set([key for key in template_keys if key.startswith('_')])
        template_keys -= {'id'}
        template_keys -= set(vars(self).keys())

        for key in template_keys:
            setattr(self, key, getattr(self.template, key))

    def is_equipped(self):
        # Untested!
        return self not in (self.inventory_unequipped or [])

    def update_stats(self, hero):
        """Update hero to reflect stat values with item equiped.

        Will fail and will need to be in Inventory?
        """
        if self.broken:
            return None
        self.template.update_stats(hero)

    def check_if_improvement(self):
        # warnings.warn("Not implemented yet!", RuntimeWarning)
        # return # Do nothing
        self.improvement = True
        for equipped_item in self.inventory.hero.equipped_items:
            if equipped_item.type is self.type:
                if equipped_item.item_rating > self.item_rating:
                    self.improvement = False
                break

    def update_owner(self, hero):
        self.inventory.hero = hero


class ItemTemplate(Base):
    """Item object base class.

    A list of all items, the relationship to the Hero class is many to many.
    Each hero can have many items and each item can be assigned multiple heroes.
    I think this is a good idea?

    How to use:
    name : Name of the Item, e.x. "power bracelet"
    hero : The Hero who owns the item
    buy_price : Price to buy the item
    level_req : level requirement
    """
    __tablename__ = "item_template"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    image = Column(String)
    inventory_icon = Column(String)

    # Marked for restructure/removal.
    # I believe that this should be part of a Display class or be built into
    # the HTML code.
    buy_name = Column(String)

    buy_price = Column(Integer)
    wearable = Column(Boolean)
    consumable = Column(Boolean)

    type = Column(String)

    # Relationships
    # Each ItemTemplate can have many regular Items.
    items = relationship("Item", back_populates='template')

    __mapper_args__ = {
        'polymorphic_identity': "ItemTemplate",
        'polymorphic_on': type
    }

    def __init__(self, name, buy_price):
        self.name = name
        self.buy_name = self.name + "_buy"
        self.buy_price = buy_price
        self.wearable = False
        self.consumable = False

    def update_stats(self, hero):
        hero.refresh_proficiencies()


# Subclass of ItemTemplate
class Wearable(ItemTemplate):
    max_durability = Column(Integer)
    item_rating = Column(Integer)
    garment = Column(Boolean)
    weapon = Column(Boolean)
    jewelry = Column(Boolean)

    # Modifiable proficiencies
    health_maximum = Column(Integer)
    regeneration_speed = Column(Integer)
    recovery_efficiency = Column(Integer)
    climbing_ability = Column(Integer)
    storage_maximum = Column(Integer)
    encumbrance_amount = Column(Integer)
    endurance_maximum = Column(Integer)
    damage_minimum = Column(Integer)
    damage_maximum = Column(Integer)
    damage_modifier = Column(Integer)
    speed_speed = Column(Integer)
    accuracy_accuracy = Column(Integer)
    first_strike_chance = Column(Integer)
    killshot_chance = Column(Integer)
    killshot_modifier = Column(Integer)
    defence_modifier = Column(Integer)
    evade_chance = Column(Integer)
    parry_chance = Column(Integer)
    flee_chance = Column(Integer)
    riposte_chance = Column(Integer)
    fatigue_maximum = Column(Integer)
    block_chance = Column(Integer)
    block_modifier = Column(Integer)
    stealth_chance = Column(Integer)
    pickpocketing_chance = Column(Integer)
    faith_modifier = Column(Integer)
    sanctity_maximum = Column(Integer)
    resist_holy_modifier = Column(Integer)
    bartering_modifier = Column(Integer)
    oration_modifier = Column(Integer)
    charm_modifier = Column(Integer)
    trustworthiness_modifier = Column(Integer)
    renown_modifier = Column(Integer)
    knowledge_modifier = Column(Integer)
    literacy_modifier = Column(Integer)
    understanding_modifier = Column(Integer)
    luckiness_chance = Column(Integer)
    adventuring_chance = Column(Integer)
    logistics_modifier = Column(Integer)
    mountaineering_modifier = Column(Integer)
    woodsman_modifier = Column(Integer)
    navigator_modifier = Column(Integer)
    detection_chance = Column(Integer)
    caution_ability = Column(Integer)
    explorer_ability = Column(Integer)
    huntsman_ability = Column(Integer)
    survivalist_ability = Column(Integer)
    resist_frost_modifier = Column(Integer)
    resist_flame_modifier = Column(Integer)
    resist_shadow_modifier = Column(Integer)
    resist_poison_modifier = Column(Integer)
    resist_blunt_modifier = Column(Integer)
    resist_slashing_modifier = Column(Integer)
    resist_piercing_modifier = Column(Integer)
    courage_skill = Column(Integer)
    sanity_skill = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': "Wearable",
    }

    def __init__(self, *args, max_durability=3, item_rating=10,
                 health_maximum=0,
                 regeneration_speed=0,
                 recovery_efficiency=0,
                 climbing_ability=0,
                 storage_maximum=0,
                 encumbrance_amount=0,
                 endurance_maximum=0,
                 damage_minimum=0, damage_maximum=0, damage_modifier=0,
                 speed_speed=0,
                 accuracy_accuracy=0,
                 first_strike_chance=0,
                 killshot_chance=0, killshot_modifier=0,
                 defence_modifier=0,
                 evade_chance=0,
                 parry_chance=0,
                 flee_chance=0,
                 riposte_chance=0,
                 fatigue_maximum=0,
                 block_chance=0, block_modifier=0,
                 stealth_chance=0,
                 pickpocketing_chance=0,
                 faith_modifier=0,
                 sanctity_maximum=0,
                 resist_holy_modifier=0,
                 bartering_modifier=0,
                 oration_modifier=0,
                 charm_modifier=0,
                 trustworthiness_modifier=0,
                 renown_modifier=0,
                 knowledge_modifier=0,
                 literacy_modifier=0,
                 understanding_modifier=0,
                 luckiness_chance=0,
                 adventuring_chance=0,
                 logistics_modifier=0,
                 mountaineering_modifier=0,
                 woodsman_modifier=0,
                 navigator_modifier=0,
                 detection_chance=0,
                 caution_ability=0,
                 explorer_ability=0,
                 huntsman_ability=0,
                 survivalist_ability=0,
                 resist_frost_modifier=0,
                 resist_flame_modifier=0,
                 resist_shadow_modifier=0,
                 resist_poison_modifier=0,
                 resist_blunt_modifier=0,
                 resist_slashing_modifier=0,
                 resist_piercing_modifier=0,
                 courage_skill=0,
                 sanity_skill=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.wearable = True
        self.broken = False
        self.garment = False
        self.weapon = False
        self.jewelry = False
        self.inventory_icon = "default_inventory_icon"

        self.max_durability = max_durability
        self.item_rating = item_rating

        # Modifiable proficiencies
        self.health_maximum = health_maximum
        self.regeneration_speed = regeneration_speed
        self.recovery_efficiency = recovery_efficiency
        self.climbing_ability = climbing_ability
        self.storage_maximum = storage_maximum
        self.encumbrance_amount = encumbrance_amount
        self.endurance_maximum = endurance_maximum
        self.damage_minimum = damage_minimum
        self.damage_maximum = damage_maximum
        self.damage_modifier= damage_modifier
        self.speed_speed = speed_speed
        self.accuracy_accuracy = accuracy_accuracy
        self.first_strike_chance = first_strike_chance
        self.killshot_chance = killshot_chance
        self.killshot_modifier = killshot_modifier
        self.defence_modifier = defence_modifier
        self.evade_chance = evade_chance
        self.parry_chance = parry_chance
        self.flee_chance = flee_chance
        self.riposte_chance = riposte_chance
        self.fatigue_maximum = fatigue_maximum
        self.block_chance = block_chance
        self.block_modifier = block_modifier
        self.stealth_chance = stealth_chance
        self.pickpocketing_chance = pickpocketing_chance
        self.faith_modifier = faith_modifier
        self.sanctity_maximum = sanctity_maximum
        self.resist_holy_modifier = resist_holy_modifier
        self.bartering_modifier = bartering_modifier
        self.oration_modifier = oration_modifier
        self.charm_modifier = charm_modifier
        self.trustworthiness_modifier = trustworthiness_modifier
        self.renown_modifier = renown_modifier
        self.knowledge_modifier = knowledge_modifier
        self.literacy_modifier = literacy_modifier
        self.understanding_modifier = understanding_modifier
        self.luckiness_chance = luckiness_chance
        self.adventuring_chance = adventuring_chance
        self.logistics_modifier = logistics_modifier
        self.mountaineering_modifier = mountaineering_modifier
        self.woodsman_modifier = woodsman_modifier
        self.navigator_modifier = navigator_modifier
        self.detection_chance = detection_chance
        self.caution_ability = caution_ability
        self.explorer_ability = explorer_ability
        self.huntsman_ability = huntsman_ability
        self.survivalist_ability = survivalist_ability
        self.resist_frost_modifier = resist_frost_modifier
        self.resist_flame_modifier = resist_flame_modifier
        self.resist_shadow_modifier = resist_shadow_modifier
        self.resist_poison_modifier = resist_poison_modifier
        self.resist_blunt_modifier = resist_blunt_modifier
        self.resist_slashing_modifier = resist_slashing_modifier
        self.resist_piercing_modifier = resist_piercing_modifier
        self.courage_skill = courage_skill
        self.sanity_skill = sanity_skill


# Subclass of ItemTemplate
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
        self.one_handed_weapon = False
        self.shield = False
        self.two_handed_weapon = False


class OneHandedWeapon(Weapon):
    __mapper_args__ = {
        'polymorphic_identity': "OneHandedWeapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.one_handed_weapon = True
        self.image = "sword"
        self.inventory_icon = "default_inventory_icon"


class Shield(Weapon):
    __mapper_args__ = {
        'polymorphic_identity': "Shield",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shield = True
        self.weapon = False
        self.image = "shield"
        self.inventory_icon = "shield"


class TwoHandedWeapon(Weapon):
    __mapper_args__ = {
        'polymorphic_identity': "TwoHandedWeapon",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.two_handed_weapon = True


# New Class
class Garment(Wearable):
    armour_value = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': "Garment",
    }

    def __init__(self, *args, armour_value=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.garment = True
        self.armour_value = armour_value


class ChestArmour(Garment):
    chest_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "ChestArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chest_armour = True
        self.image = "chest"
        self.inventory_icon = "chest"


class HeadArmour(Garment):
    head_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "HeadArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_armour = True
        self.image = "helmet"
        self.inventory_icon = "helmet"


class LegArmour(Garment):
    leg_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "LegArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leg_armour = True
        self.image = "legs"
        self.inventory_icon = "legs"


class FeetArmour(Garment):
    feet_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "FeetArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feet_armour = True
        self.image = "feet"
        self.inventory_icon = "feet"


class ArmArmour(Garment):
    arm_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "ArmArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arm_armour = True
        self.image = "arms"
        self.inventory_icon = "arms"


class HandArmour(Garment):
    hand_armour = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': "HandArmour",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_armour = True
        self.image = "gloves"
        self.inventory_icon = "gloves"


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


# Subclass of ItemTemplate
class Consumable(ItemTemplate):
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

    def apply_effect(self, hero):
        # hero.health += self.healing_amount
        # hero.sanctity += self.sanctity_amount
        # if hero.health > hero.health_maximum:
        # hero.health = hero.health_maximum
        # if hero.sanctity > hero.max_sanctity:
        # hero.sanctity = hero.max_sanctity
        print("Applied item effect. But not really.")


# New Class
class QuestItem(ItemTemplate):
    quest_item = Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity': "QuestItem",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quest_item = True

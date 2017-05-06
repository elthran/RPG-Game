try:
    from sqlalchemy import Column, Integer, String, Boolean
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy import orm
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")
    
#!Important!: Base can only be defined in ONE location and ONE location ONLY!
#Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base

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
"""


class Item(Base):
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
    
    #template = relationship(ItemTemplate) -> One to Many
    durability = Column(Integer)
    broken = Column(Boolean)
    consumed = Column(Boolean)
    name = Column(String)
    equipped = Column(Boolean)
    
    def __init__(self, template):
        """Build a new item from a given template.
        
        Set initial values for item attributes. of  
        """
        self.template = template
        self.name = template.name
        
        #Should be a current_durability value as well?
        try:
            self.durability = template.max_durability
        except AttributeError:
            pass
        self.broken = False
        self.consumed = False
        self.equipped = False
        
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
        hierarchy = type(self.template).__mro__[:-2]
        
        for obj in hierarchy:
            template_keys |= set(vars(obj).keys()) - set(obj.__mapper__.relationships.keys())
            
        template_keys -= set([key for key in template_keys if key.startswith('_')])
        template_keys -= {'id'}
        template_keys -= set(vars(self).keys())
        
        for key in template_keys:
            setattr(self, key, getattr(self.template, key))

    
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
	level_req : level requirment
    """
    __tablename__ = "item_template"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    #Marked for restructure/removal.
    #I believe that this should be part of a Display class or be built into the HTML code.
    buy_name = Column(String)
    
    buy_price = Column(Integer)
    
    wearable = Column(Boolean)
    consumable = Column(Boolean)
 
    type = Column(String)
    __mapper_args__ = {
        'polymorphic_identity':"ItemTemplate",
        'polymorphic_on':type
    }
    
    def __init__(self, name, buy_price):
        self.name = name
        self.buy_name = self.name + "_buy"
        self.buy_price = buy_price
        self.wearable = False
        self.consumable = False
        
    def update_stats(self, hero):
        pass
        

# Subclass of ItemTemplate
class Wearable(ItemTemplate):
    __tablename__ = 'wearable'
    
    id = Column(Integer, ForeignKey("item_template.id"), primary_key=True)
    
    max_durability = Column(Integer)
    item_rating = Column(Integer)
    garment = Column(Boolean)
    weapon = Column(Boolean)
    jewelry = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity':"Wearable",
    }
    
    def __init__(self, name, buy_price, max_durability=3, item_rating=10):
        super().__init__(name, buy_price)
        self.wearable = True
        self.broken = False
        self.max_durability = max_durability
        self.item_rating = item_rating
        garment = False
        weapon = False
        jewelry = False


# Subclass of ItemTemplate
class Weapon(Wearable):
    __tablename__ = 'weapon'
    
    id = Column(Integer, ForeignKey("wearable.id"), primary_key=True)
    
    min_damage = Column(Integer)
    max_damage = Column(Integer)
    attack_speed = Column(Integer)
    
    one_handed_weapon = Column(Boolean)
    shield = Column(Boolean)
    two_handed_weapon = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Weapon",
    }
    def __init__(self, name, buy_price, min_damage=0, max_damage=0, attack_speed=0):
        super().__init__(name, buy_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attack_speed = attack_speed
        
        #Marked for restructure
        #If self.type == "Weapon" should do the same thing.
        #In fact all of these should be taken care of inside of the relavant
        #subclass. i.e. if self.type == one_handed_weapon etc.
        self.weapon = True
        self.one_handed_weapon = False
        self.shield = False
        self.two_handed_weapon = False
    
    def update_stats(self, hero):
        hero.minimum_damage += self.min_damage
        hero.maximum_damage += self.max_damage
        hero.attack_speed += self.attack_speed
		
class One_Handed_Weapon(Weapon):
    __tablename__ = 'one_handed_weapon'
    
    id = Column(Integer, ForeignKey("weapon.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"One_Handed_Weapon",
    }
    
    def __init__(self, name, buy_price, min_damage, max_damage, attack_speed):
        super().__init__(name, buy_price, min_damage, max_damage, attack_speed)
        self.one_handed_weapon = True

class Shield(Weapon):
    __tablename__ = 'shield'
    
    id = Column(Integer, ForeignKey("weapon.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Shield",
    }
    
    def __init__(self, name, buy_price):
        super().__init__(name, buy_price)
        self.shield = True
        self.weapon = False

class Two_Handed_Weapon(Weapon):
    __tablename__ = 'two_handed_weapon'
    
    id = Column(Integer, ForeignKey("weapon.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Two_Handed_Weapon",
    }
    
    def __init__(self, name, buy_price, min_damage, max_damage, attack_speed):
        super().__init__(name, buy_price, min_damage, max_damage, attack_speed)
        self.two_handed_weapon = True

# New Class		
class Garment(Wearable):
    __tablename__ = 'garment'
    
    id = Column(Integer, ForeignKey("wearable.id"), primary_key=True)
    
    health_modifier = Column(Integer)
    
    __mapper_args__ = {
        'polymorphic_identity':"Garment",
    }
    
    def __init__(self, name, buy_price, health_modifier):
        super().__init__(name, buy_price)
        self.health_modifier = health_modifier
        self.garment = True

    def update_stats(self, hero):
        hero.health_maximum += self.health_modifier

class Chest_Armour(Garment):
    __tablename__ = 'chest_armour'
    
    id = Column(Integer, ForeignKey("garment.id"), primary_key=True)
    
    chest_armour = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Chest_Armour",
    }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chest_armour = True

class Head_Armour(Garment):
    __tablename__ = 'head_armour'
    
    id = Column(Integer, ForeignKey("garment.id"), primary_key=True)
    
    head_armour = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Head_Armour",
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head_armour = True

class Leg_Armour(Garment):
    __tablename__ = 'leg_armour'
    
    id = Column(Integer, ForeignKey("garment.id"), primary_key=True)
    
    leg_armour = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Leg_Armour",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leg_armour = True

class Feet_Armour(Garment):
    __tablename__ = 'feet_armour'
    
    id = Column(Integer, ForeignKey("garment.id"), primary_key=True)
    
    feet_armour = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Feet_Armour",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feet_armour = True

class Arm_Armour(Garment):
    __tablename__ = 'Arm_Armour'
    
    id = Column(Integer, ForeignKey("garment.id"), primary_key=True)
    
    arm_armour = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Arm_Armour",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arm_armour = True

class Hand_Armour(Garment):
    __tablename__ = 'hand_armour'
    
    id = Column(Integer, ForeignKey("garment.id"), primary_key=True)
    
    hand_armour = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Hand_Armour",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_armour = True

# New Class
class Jewelry(Wearable):
    __tablename__ = 'jewelry'
    
    id = Column(Integer, ForeignKey("wearable.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Jewelry",
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jewelry = True

class Ring(Jewelry):
    __tablename__ = 'ring'
    
    id = Column(Integer, ForeignKey("jewelry.id"), primary_key=True)
    
    ring = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Ring",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ring = True
        
    def update_stats(self, hero):
        pass

# Subclass of ItemTemplate
class Consumable(ItemTemplate):
    __tablename__ = 'consumable'
    
    id = Column(Integer, ForeignKey("item_template.id"), primary_key=True)
    
    healing_amount = Column(Integer)
    sanctity_amount = Column(Integer)
    
    __mapper_args__ = {
        'polymorphic_identity':"Consumable",
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
class Quest_Item(ItemTemplate):
    __tablename__ = 'quest_item'
    
    id = Column(Integer, ForeignKey("item_template.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Quest_Item",
    }
    def __init__(self, name, buy_price):
        super().__init__(name, buy_price)

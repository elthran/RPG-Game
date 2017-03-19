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

"""
Item Specification:
    All hero specific attributes must be moved from the Template classes.
    Or maybe InventoryItem which relates to Hero by inventory.
    Hero.inventory = relations 1 to many with InventoryItem.
    Item.inventory = relation many to many with inventoryItem.
    Things like:
        -durability
        -amount_owned
        -broken
        -consumed (unless consumable just removes the item)
"""

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)


class TemplateItem(Base):
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
    __tablename__ = "template_item"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    #Marked for restructure/removal.
    #I believe that this should be part of a Display class or be built into the HTML code.
    buy_name = Column(String)
    
    buy_price = Column(Integer)
    
    #Marked for restructuring as causes conflics with multiple heroes?
    #As in if hero1 has 4 of an item then hero2 will as well?
    #Move to Inventory?
    amount_owned = Column(Integer)
    
    wearable = Column(Boolean)
    consumable = Column(Boolean)
 
    type = Column(String)
    __mapper_args__ = {
        'polymorphic_identity':"TemplateItem",
        'polymorphic_on':type
    }
    
    def __init__(self, name, myHero, buy_price, amount_owned=1):
        self.name = name
        self.buy_name = self.name + "_buy"
        self.myHero = myHero
        self.buy_price = buy_price
        self.amount_owned = amount_owned
        self.wearable = False
        self.consumable = False

    def update_owner(self, myHero):
        self.myHero = myHero
        

# Subclass of TemplateItem
class Wearable(TemplateItem):
    __tablename__ = 'wearable'
    
    id = Column(Integer, ForeignKey("template_item.id"), primary_key=True)
    
    broken = Column(Boolean)
    durability = Column(Integer)
    max_durability = Column(Integer)
    item_rating = Column(Integer)
    garment = Column(Boolean)
    weapon = Column(Boolean)
    jewelry = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity':"Wearable",
    }
    
    def __init__(self, name, myHero, buy_price, max_durability=3, item_rating=10):
        super().__init__(name, myHero, buy_price)
        self.wearable = True
        self.broken = False
        self.max_durability = max_durability
        self.durability = self.max_durability
        self.item_rating = item_rating
        garment = False
        weapon = False
        jewelry = False

    def check_if_improvement(self):
        self.improvement = True
        for equipped_item in self.myHero.equipped_items:
            if type(equipped_item) is type(self):
                if equipped_item.item_rating > self.item_rating:
                    self.improvement = False
                break

# Subclass of TemplateItem
class Weapon(Wearable):
    __tablename__ = 'weapon'
    
    id = Column(Integer, ForeignKey("wearable.id"), primary_key=True)
    
    min_damage = Column(Integer)
    max_damage = Column(Integer)
    
    one_handed_weapon = Column(Boolean)
    shield = Column(Boolean)
    two_handed_weapon = Column(Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':"Weapon",
    }
    def __init__(self, name, myHero, buy_price, min_damage=0, max_damage=0, attack_speed=0):
        super().__init__(name, myHero, buy_price)
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
        
    def update_stats(self):
        if self.broken:
            return None
        self.myHero.minimum_damage += self.min_damage
        self.myHero.maximum_damage += self.max_damage
        self.myHero.attack_speed += self.attack_speed
		
class One_Handed_Weapon(Weapon):
    __tablename__ = 'one_handed_weapon'
    
    id = Column(Integer, ForeignKey("weapon.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"One_Handed_Weapon",
    }
    
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super().__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.one_handed_weapon = True

class Shield(Weapon):
    __tablename__ = 'shield'
    
    id = Column(Integer, ForeignKey("weapon.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Shield",
    }
    
    def __init__(self, name, myHero, buy_price):
        super().__init__(name, myHero, buy_price)
        self.shield = True
        self.weapon = False

class Two_Handed_Weapon(Weapon):
    __tablename__ = 'two_handed_weapon'
    
    id = Column(Integer, ForeignKey("weapon.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Two_Handed_Weapon",
    }
    
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super().__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.two_handed_weapon = True

# New Class		
class Garment(Wearable):
    __tablename__ = 'garment'
    
    id = Column(Integer, ForeignKey("wearable.id"), primary_key=True)
    
    health_modifier = Column(Integer)
    
    __mapper_args__ = {
        'polymorphic_identity':"Garment",
    }
    
    def __init__(self, name, myHero, buy_price, health_modifier):
        super().__init__(name, myHero, buy_price)
        self.health_modifier = health_modifier
        self.garment = True

    def update_stats(self):
        if self.broken:
            return None
        self.myHero.max_health += self.health_modifier

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

# Subclass of TemplateItem
class Consumable(TemplateItem):
    __tablename__ = 'consumable'
    
    id = Column(Integer, ForeignKey("template_item.id"), primary_key=True)
    
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
		
    def apply_effect(self):
        self.myHero.current_health += self.healing_amount
        self.myHero.current_sanctity += self.sanctity_amount
        if self.myHero.current_health > self.myHero.max_health:
            self.myHero.current_health = self.myHero.max_health
        if self.myHero.current_sanctity > self.myHero.max_sanctity:
            self.myHero.current_sanctity = self.myHero.max_sanctity

# New Class
class Quest_Item(TemplateItem):
    __tablename__ = 'quest_item'
    
    id = Column(Integer, ForeignKey("template_item.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"Quest_Item",
    }
    def __init__(self, name, myHero, buy_price):
        super().__init__(name, myHero, buy_price)

class Item(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, myHero, buy_price, amount_owned=1):
        self.name = name
        self.buy_name = self.name + "_buy"
        self.myHero = myHero
        self.buy_price = buy_price
        self.amount_owned = amount_owned
        self.equippable = False
        self.consumable = False

    def update_owner(self, myHero):
        self.myHero = myHero

# Subclass of Item
class Equippable(Item):
    def __init__(self, name, myHero, buy_price, max_durability=3, item_rating=10):
        super().__init__(name, myHero, buy_price)
        self.equippable = True
        self.broken = False
        self.max_durability = max_durability
        self.durability = self.max_durability
        self.item_rating = item_rating

    def check_if_improvement(self):
        self.improvement = True
        for equipped_item in self.myHero.equipped_items:
            if type(equipped_item) is type(self):
                if equipped_item.item_rating > self.item_rating:
                    self.improvement = False
                break

# Subclass of Item
class Weapon(Equippable):
    def __init__(self, name, myHero, buy_price, min_damage=0, max_damage=0, attack_speed=0):
        super().__init__(name, myHero, buy_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attack_speed = attack_speed
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
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super().__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.one_handed_weapon = True

class Shield(Weapon):
    def __init__(self, name, myHero, buy_price):
        super().__init__(name, myHero, buy_price)
        self.shield = True
        self.weapon = False

class Two_Handed_Weapon(Weapon):
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super().__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.two_handed_weapon = True

# New Class		
class Garment(Equippable):
    def __init__(self, name, myHero, buy_price, health_modifier):
        super().__init__(name, myHero, buy_price)
        self.health_modifier = health_modifier

    def update_stats(self):
        if self.broken:
            return None
        self.myHero.max_health += self.health_modifier

class Chest_Armour(Garment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.chest_armour = True

class Head_Armour(Garment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.head_armour = True

class Leg_Armour(Garment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.leg_armour = True

class Feet_Armour(Garment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.feet_armour = True

class Arm_Armour(Garment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.arm_armour = True

class Hand_Armour(Garment):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.hand_armour = True

# New Class
class Jewelry(Equippable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Ring(Jewelry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ring = True

# Subclass of Item
class Consumable(Item):
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
class Quest_Item(Item):
    def __init__(self, name, myHero, buy_price):
        super().__init__(name, myHero, buy_price)

all_store_items = [One_Handed_Weapon("Small Dagger", "Temporary", buy_price=5, min_damage=30, max_damage=60, attack_speed=1),
                   One_Handed_Weapon("Big Dagger", "Temporary", buy_price=10, min_damage=300, max_damage=600, attack_speed=2),
                   Shield("Small Shield", "Temporary", buy_price=10),
                   Two_Handed_Weapon("Small Polearm", "Temporary", buy_price=5, min_damage=30, max_damage=60, attack_speed=1),
                   Two_Handed_Weapon("Medium Polearm", "Temporary", buy_price=5, min_damage=30, max_damage=60, attack_speed=1),
                   Leg_Armour("Medium Pants", "Temporary", 7, 25),
                   Chest_Armour("Medium Tunic", "Temporary", 2, 25),
                   Chest_Armour("Strong Tunic", "Temporary", 5, 250),
                   Head_Armour("Weak Helmet", "Temporary", 2, 1),
                   Head_Armour("Medium Helmet", "Temporary", 4, 3),
                   Feet_Armour("Test Boots", "Temporary", 3, 3),
                   Arm_Armour("Test Sleeves", "Temporary", 4, 5),
                   Hand_Armour("Test Gloves", "Temporary", 5, 7),
                   Ring("Test Ring", "Temporary", 8)]

all_marketplace_items = [Consumable("Minor Health Potion", "Temporary", 3, healing_amount=10),
                         Consumable("Major Health Potion", "Temporary", 6, healing_amount=50),
                         Consumable("Major Faith Potion", "Temporary", 6, sanctity_amount=50),
                         Consumable("Major Awesome Max Potion", "Temporary", 6000, sanctity_amount=50)]

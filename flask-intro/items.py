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
    def __init__(self, name, myHero, buy_price, durability=10):
        super(Equippable, self).__init__(name, myHero, buy_price)
        self.equippable = True
        self.durability = durability

    def update_stats(self):
        self.myHero.min_damage += self.min_damage
        self.myHero.max_damage += self.max_damage
        self.myHero.attack_speed += self.attack_speed
        self.myHero.max_health += self.health_modifier

    def check_if_improvement(self):
        self.improvement = True
        for equipped_item in self.myHero.equipped_items:
            if type(equipped_item) is type(self):
                if equipped_item.health_modifier > self.health_modifier:
                    self.improvement = False
                break

# Subclass of Item
class Weapon(Equippable):
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super(Weapon, self).__init__(name, myHero, buy_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attack_speed = attack_speed
		
class Right_Handed(Weapon):
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super(Right_Handed, self).__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.right_handed = True

class Left_Handed(Weapon):
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super(Left_Handed, self).__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.left_handed = True

class Two_Handed(Weapon):
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super(Two_Handed, self).__init__(name, myHero, buy_price, min_damage, max_damage, attack_speed)
        self.two_handed = True

# New Class		
class Garment(Equippable):
    def __init__(self, name, myHero, buy_price, health_modifier):
        super(Garment, self).__init__(name, myHero, buy_price)
        self.health_modifier = health_modifier

class Chest_Armour(Garment):
        def __init__(self, name, myHero, buy_price, health_modifier):
            super(Chest_Armour, self).__init__(name, myHero, buy_price, health_modifier)
            self.chest_armour = True

class Head_Armour(Garment):
        def __init__(self, name, myHero, buy_price, health_modifier):
            super(Head_Armour, self).__init__(name, myHero, buy_price, health_modifier)
            self.head_armour = True

class Leg_Armour(Garment):
        def __init__(self, name, myHero, buy_price, health_modifier):
            super(Leg_Armour, self).__init__(name, myHero, buy_price, health_modifier)
            self.leg_armour = True

class Feet_Armour(Garment):
        def __init__(self, name, myHero, buy_price, health_modifier):
            super(Feet_Armour, self).__init__(name, myHero, buy_price, health_modifier)
            self.feet_armour = True

class Arm_Armour(Garment):
        def __init__(self, name, myHero, buy_price, health_modifier):
            super(Arm_Armour, self).__init__(name, myHero, buy_price, health_modifier)
            self.arm_armour = True

class Hand_Armour(Garment):
        def __init__(self, name, myHero, buy_price, health_modifier):
            super(Hand_Armour, self).__init__(name, myHero, buy_price, health_modifier)
            self.hand_armour = True

# New Class
class Jewelry(Equippable):
    def __init__(self, name, myHero, buy_price):
        super(Jewelry, self).__init__(name, myHero, buy_price)

class Ring(Jewelry):
        def __init__(self, name, myHero, buy_price):
            super(Ring, self).__init__(name, myHero, buy_price)
            self.ring = True

# Subclass of Item
class Consumable(Item):
    def __init__(self, name, myHero, buy_price, healing_amount=0, sanctity_amount=0):
        super(Consumable, self).__init__(name, myHero, buy_price)
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
        super(Quest_Item, self).__init__(name, myHero, buy_price)

all_store_items = [Right_Handed("Small Dagger", "Temporary", 5, 30, 60, 1),
                   Right_Handed("Big Dagger", "Temporary", 10, 300, 600, 2),
                   Left_Handed("Small Shield", "Temporary", 10, 300, 600, 2),
                   Two_Handed("Small Polearm", "Temporary", 5, 30, 60, 1),
                   Two_Handed("Medium Polearm", "Temporary", 5, 30, 60, 1),
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
                         Consumable("Major Faith Potion", "Temporary", 6, sanctity_amount=50)]



class Item(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, myHero, buy_price):
        self.name = name
        self.myHero = myHero
        self.buy_price = buy_price
        self.equippable = False

    def update_owner(self, myHero):
        self.myHero = myHero


# Subclass of Item
# (Other comments about it)
class Weapon(Item):
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super(Weapon, self).__init__(name, myHero, buy_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attack_speed = attack_speed
        self.equippable = True
		
    def update_stats(self):
        self.myHero.min_damage += self.min_damage
        self.myHero.max_damage += self.max_damage
        self.myHero.attack_speed += self.attack_speed

    def check_if_improvement(self):
            self.improvement = True
            for equipped_item in self.myHero.equipped_items:
                if type(equipped_item) is type(self):
                    if equipped_item.attack_speed > self.attack_speed:
                        self.improvement = False
                    break
		
class Garment(Item):
    def __init__(self, name, myHero, buy_price, health_modifier):
        super(Garment, self).__init__(name, myHero, buy_price)
        self.health_modifier = health_modifier
        self.equippable = True

    def update_stats(self):
        self.myHero.max_health += self.health_modifier

    def check_if_improvement(self):
            self.improvement = True
            for equipped_item in self.myHero.equipped_items:
                if type(equipped_item) is type(self):
                    if equipped_item.health_modifier > self.health_modifier:
                        self.improvement = False
                    break

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

class Quest_Item(Item):
    def __init__(self, name, myHero, buy_price):
        super(Quest_Item, self).__init__(name, myHero, buy_price)
        self.amount_owned = 1
        self.equippable = False

    def update_stats(self):
        pass

all_store_items = [Weapon("Medium Axe", "Temporary", 5, 30, 60, 1), Weapon("Strong Axe", "Temporary", 60, 300, 600, 2), Leg_Armour("Medium Pants", "Temporary", 7, 25), Chest_Armour("Medium Tunic", "Temporary", 2, 25), Chest_Armour("Strong Tunic", "Temporary", 5, 250), Head_Armour("Test Helmet", "Temporary", 1, 1)]

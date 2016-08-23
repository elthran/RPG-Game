from game import *

class Item(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, myHero, buy_price):
        self.name = name
        self.myHero = myHero
        self.buy_price = buy_price


# Subclass of Item
# (Other comments about it)
class Weapon(Item):
    def __init__(self, name, myHero, buy_price, damage):
        super(Weapon, self).__init__(name, myHero, buy_price)
        self.damage = damage
		
    def update_stats(self):
        if self.name == "Broken Axe":
            print("correct name")
            self.myHero.max_damage += 20

        if self.name == "Medium Axe":
            print("correct name")
            self.myHero.max_damage += 30

        if self.name == "Strong Axe":
            print("correct name")
            self.myHero.max_damage += 40

		
class Garment(Item):
    def __init__(self, name, myHero, buy_price, hp_modifier):
        super(Garment, self).__init__(name, myHero, buy_price)
        self.hp_modifier = hp_modifier

    def update_stats(self):
        if self.name == "Ripped Tunic":
            self.myHero.max_hp += 50

        if self.name == "Medium Tunic":
            self.myHero.max_hp += 80

        if self.name == "Strong Tunic":
            self.myHero.max_hp += 110


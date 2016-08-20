from game import *

class Item(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, hero):
        self.name = name
        self.hero = hero
		
    def set_hero(self, hero):
        self.hero = hero

    def set_name(self, name):
        self.name = name
		
    def set_buy_price(self, buy_price):
        self.buy_price = buy_price
		
    def set_level_req(self, level_req):
        self.level_req = level_req

    # call when hero equips the item	
    def equip(self):	
        self.is_equiped = True
        return
    # call when hero takes off the item	
    def dequip(self):
        self.is_equiped = False
        return
		
    def __repr__(self):
        return "\nName: %s\nHero: %s" % (self.name, self.hero)

# Subclass of Item
# (Other comments about it)
class Weapon(Item):
    def __init__(self, name, hero, damage):
        super().__init__(self,name,hero)
        self.damage = damage
		
    def set_damage(self, damage):
        self.damage = damage
		
    def equip(self):
        super(Weapon, self).equip()
        return
        #self.hero...
		
    def dequip(self):
        super(Weapon, self).dequip()
        return
	#...

		
class Garment(Item):
			
    def equip(self):
        super(Garment, self).equip()
        if self.name == "ripped tunic":
            self.hero.max_hp += 10
        if self.name == "torn tunic":
            self.hero.max_hp += 16
			
    def dequip(self):
        super(Garment, self).dequip()
        if self.name == "ripped tunic":
            self.hero.max_hp -= 5
        if self.name == "torn tunic":
            self.hero.max_hp -= 10
        if self.hero.max_hp <= 0:
            self.hero.max_hp = 1


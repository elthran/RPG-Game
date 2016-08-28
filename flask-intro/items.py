

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
    def __init__(self, name, myHero, buy_price, min_damage, max_damage, attack_speed):
        super(Weapon, self).__init__(name, myHero, buy_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attack_speed = attack_speed
		
    def update_stats(self):
        self.myHero.min_damage += self.min_damage
        self.myHero.max_damage += self.max_damage
        self.myHero.attack_speed += self.attack_speed
		
class Garment(Item):
    def __init__(self, name, myHero, buy_price, health_modifier):
        super(Garment, self).__init__(name, myHero, buy_price)
        self.health_modifier = health_modifier

    def update_stats(self):
        self.myHero.max_health += self.health_modifier


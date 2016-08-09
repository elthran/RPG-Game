class Ability(object):
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

    def __repr__(self):
        return "\nName: %s\nHero: %s" % (self.name, self.hero)

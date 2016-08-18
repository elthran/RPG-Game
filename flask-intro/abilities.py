skin_adjective = ["Tough","Iron","Stone","Diamond"]

class Ability(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, hero, adjectives):
        self.name = name
        self.hero = hero
        self.level = 1
        self.adjectives = adjectives
        self.display_name = self.adjectives[self.level - 1]
        self.requirements = []

    def update_stats(self):
        if self.name == "Stone Skin":
            self.hero.max_hp += 500 * self.level

    def __repr__(self):
        return "\nName: %s\nHero: %s" % (self.name, self.hero)
    

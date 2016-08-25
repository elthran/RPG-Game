#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

skin_adjective = ["Tough","Iron","Stone","Diamond"]

class Ability(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, myHero, adjectives):
        self.name = name
        self.myHero = myHero
        self.level = 1
        self.adjectives = adjectives
        self.display_name = self.adjectives[self.level - 1]
        self.requirements = []

    def update_stats(self):
        if self.name == "Stone Skin":
            self.myHero.max_hp += 15 * self.level
    

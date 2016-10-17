#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

class Ability(object):
    # name : Name of the Item, e.x. "power bracelet"
    # hero : The Hero who owns the item
	# buy_price : Price to buy the item
	# level_req : level requirment
    def __init__(self, name, myHero, max_level):
        self.name = name
        self.myHero = myHero
        self.level = 1
        self.max_level = max_level
        self.adjective = ["I","II","III","IV", "V"]
        self.display_name = self.adjective[self.level - 1]
        self.requirements = []

    def update_stats(self):
        if self.name == "Stone Skin":
            self.myHero.max_health += 15 * self.level
        if self.name == "Arcane Intellect":
            self.myHero.max_sanctity += 50 * self.level
        if self.name == "Giant Strength":
            self.myHero.max_damage += 15 * self.level

all_abilities = [Ability("Arcane Intellect", "Null", 0),
                 Ability("Stone Skin", "Null", 0),
                 Ability("Giant Strength", "Null", 0),]

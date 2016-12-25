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
    def __init__(self, name, myHero, max_level, description):
        self.name = name
        self.myHero = myHero
        self.level = 1
        self.max_level = max_level
        self.description = description
        self.adjective = ["I","II","III","IV", "V", "VI"]
        self.display_name = self.adjective[self.level - 1]
        self.learn_name = self.adjective[self.level]
        self.requirements = []

    def update_stats(self):
        if self.name == "Stone Skin":
            self.myHero.max_health += 15 * self.level
        if self.name == "Arcane Intellect":
            self.myHero.max_sanctity += 50 * self.level
        if self.name == "Giant Strength":
            self.myHero.max_damage += 15 * self.level
        if self.name == "Sage":
            self.myHero.experience_gain_modifier += 0.05 * self.level
        if self.name == "The Donkey":
            self.myHero.max_carrying_capacity += 5 * self.level

    def update_display(self):
        self.display_name = self.adjective[self.level - 1]
        if self.level < self.max_level:
            self.learn_name = self.adjective[self.level]

all_abilities = [Ability("Arcane Intellect", "Null", 5, "Increases Sanctity by 50 for each level."),
                 Ability("Stone Skin", "Null", 5, "Increases Health by 15 for each level."),
                 Ability("Giant Strength", "Null", 5, "Increases Strength by 15 for each level."),
                 Ability("Sage", "Null", 5, "Increases Experience Gain by 5% for each level."),
                 Ability("The Donkey", "Null", 3, "Increases carrying capacity by 5 for each level.")]

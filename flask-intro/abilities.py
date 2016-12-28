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
        self.ability_type = "Unknown"

    def update_stats(self):
        if self.name == "Determination":
            self.myHero.max_endurance += 3 * self.level
        if self.name == "Salubrity":
            self.myHero.max_health += 4 * self.level

    def update_display(self):
        self.display_name = self.adjective[self.level - 1]
        if self.level < self.max_level:
            self.learn_name = self.adjective[self.level]

    def update_owner(self, myHero):
        self.myHero = myHero

class Basic_Ability(Ability):
    def __init__(self, name, myHero, max_level, description):
        super(Basic_Ability, self).__init__(name, myHero, max_level, description)
        self.ability_type = "basic"

class Archetype_Ability(Ability):
    def __init__(self, name, myHero, max_level, description):
        super(Archetype_Ability, self).__init__(name, myHero, max_level, description)
        self.ability_type = "archetype"

class Class_Ability(Ability):
    def __init__(self, name, myHero, max_level, description):
        super(Class_Ability, self).__init__(name, myHero, max_level, description)
        self.ability_type = "class"

class Religious_Ability(Ability):
    def __init__(self, name, myHero, max_level, description):
        super(Religious_Ability, self).__init__(name, myHero, max_level, description)
        self.ability_type = "religious"
    

all_abilities = [Basic_Ability("Determination", "Null", 5, "Increases Endurance by 3 for each level."),
                 Basic_Ability("Salubrity", "Null", 5, "Increases Health by 4 for each level.")]

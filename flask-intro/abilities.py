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
    def __init__(self, name, myHero, max_level, description, activated=False, cost=0):
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
        self.activated = activated
        self.cost = cost

    def update_stats(self):
        if self.name == "Determination":
            self.myHero.max_endurance += 3 * self.level
        if self.name == "Salubrity":
            self.myHero.max_health += 4 * self.level

    def activate(self):
        if self.myHero.current_sanctity < self.cost:
            return
        else:
            self.myHero.current_sanctity -= self.cost
        if self.name == "Gain Gold to Test":
            self.myHero.gold += 3 * self.level

    def update_display(self):
        self.display_name = self.adjective[self.level - 1]
        if self.level < self.max_level:
            self.learn_name = self.adjective[self.level]

    def update_owner(self, myHero):
        self.myHero = myHero

class Basic_Ability(Ability):
    def __init__(self, name, myHero, max_level, description, activated, cost):
        super(Basic_Ability, self).__init__(name, myHero, max_level, description, activated, cost)
        self.ability_type = "basic"

class Archetype_Ability(Ability):
    def __init__(self, name, myHero, max_level, description, activated, archetype="All"):
        super(Archetype_Ability, self).__init__(name, myHero, max_level, description, activated)
        self.ability_type = "archetype"
        self.archetype = archetype

class Class_Ability(Ability):
    def __init__(self, name, myHero, max_level, description, activated, specialization="All"):
        super(Class_Ability, self).__init__(name, myHero, max_level, description, activated)
        self.ability_type = "class"
        self.specialization = specialization

class Religious_Ability(Ability):
    def __init__(self, name, myHero, max_level, description, activated, religion="All"):
        super(Religious_Ability, self).__init__(name, myHero, max_level, description, activated)
        self.ability_type = "religious"
        self.religion = religion


all_abilities = [Basic_Ability("Determination", "Null", 5, "Increases Endurance by 3 for each level.", False, 0),
                 Basic_Ability("Salubrity", "Null", 5, "Increases Health by 4 for each level.", False, 0),
                 Basic_Ability("Gain Gold to Test", "Null", 5, "Gain 3 gold for each level, every time you actvate this ability.", True, 2),
                 Archetype_Ability("Survivalism", "Null", 10, "Increases survivalism by 1 for each level.", "Woodsman", False),
                 Archetype_Ability("Piety", "Null", 10, "Increases divinity by 1 for each level.", "Priest", False),
                 Archetype_Ability("Sagacious", "Null", 10, "Increases experience gained by 5% for each level.", False),
                 Class_Ability("Panther Aspect", "Null", 10, "Increases evade chance by 1% for each level.", "Hunter", False),
                 Class_Ability("Camouflage", "Null", 10, "Increases stealth by 1% for each level.", "Trapper", False),
                 Class_Ability("Luck", "Null", 10, "Increases luck by 2 for each level.", False),
                 Religious_Ability("Iron Bark", "Null", 10, "Increases defence by 2% for each level.", "Dryarch", False),
                 Religious_Ability("Wreath of Flames", "Null", 10, "Increases fire damage by 3 for each level.", "Forgoth", False),
                 Religious_Ability("Blessed", "Null", 10, "Increases devotion by 5 for each level.", False)]

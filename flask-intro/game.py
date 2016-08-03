class Hero(object):
    def __init__(self, name, level, strength, agility, wisdom, vitality, hp, maxhp, wins, spec):
        self.name = name
        self.level = level
        self.strength = strength
        self.agility = agility
        self.wisdom = wisdom
        self.vitality = vitality
        self.hp = hp
        self.maxhp = maxhp
        self.wins = wins
        self.spec = spec

    def __repr__(self):
        return "Name: %s \n Class: Brute \n Level: %s \n Strength: %s \n Agility: %s \n Wisdom: %s \n Vitality: %s \n HP: %s/%s \n" % (self.name, self.level, self.strength, self.agility, self.wisdom, self.vitality, self.hp, self.maxhp) 

myHero = Hero("Unknown", 1, 3, 4, 2, 3, 50, 50, 1, "")
enemy = Hero("Goblin", 1, 2, 2, 2, 2, 7, 7, 0, "")

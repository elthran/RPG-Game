import math

class Hero(object):
    def __init__(self, name, level, attribute_points, current_exp, max_exp, starting_class, strength, speed, damage, vitality, hp, max_hp, wisdom, faith, affinity, wins):
        self.name = name
        self.level = level
        self.attribute_points = attribute_points
        self.current_exp = current_exp
        self.max_exp = max_exp
        self.starting_class = starting_class
        
        self.strength = strength
        self.speed = speed
        self.damage = damage
        
        self.vitality = vitality
        self.hp = hp
        self.max_hp = max_hp

        self.wisdom = wisdom
        self.faith = faith
        self.affinity = affinity
        
        self.wins = wins

    def update_attributes(self, strength, speed, vitality, wisdom, faith):
        self.damage = strength * speed
        self.max_hp = vitality * 10
        self.affinity = wisdom + faith

    def update_health(self, max_hp):
        self.hp = max_hp

    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return
        self.current_exp = 0
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.level += 1

    def __repr__(self):
        return "\nName: %s\nDamage: %s" % (self.name, self.damage)

myHero = Hero("Unknown", 1, 0, 0, 10, "", 3, 3, 0, 3, 0, 0, 3, 3, 0, 0)

myHero.update_attributes(myHero.strength, myHero.speed, myHero.vitality, myHero.wisdom, myHero.faith)
myHero.update_health(myHero.max_hp)



class Hero(object):
    def __init__(self, name, level, starting_class, strength, speed, damage, vitality, hp, max_hp, wisdom, faith, affinity, wins):
        self.name = name
        self.level = level
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

    def update_stats(self, strength, speed, vitality, wisdom, faith):
        self.damage = strength * speed
        self.max_hp = vitality * 10
        self.affinity = wisdom + faith

    def update_health(self, max_hp):
        self.hp = max_hp

    def __repr__(self):
        return "Name: %s\nDamage: %s" % (self.name, self.damage) 

myHero = Hero("Unknown", 1, "", 3, 3, 0, 3, 0, 0, 3, 3, 0, 0)
enemy = Hero("Goblin", 1, "", 2, 2, 0, 2, 0, 0, 2, 2, 0, 0)

myHero.update_stats(myHero.strength, myHero.speed, myHero.vitality, myHero.wisdom, myHero.faith)
myHero.update_health(myHero.max_hp)
enemy.update_stats(enemy.strength, enemy.speed, enemy.vitality, enemy.wisdom, enemy.faith)
enemy.update_health(enemy.max_hp)


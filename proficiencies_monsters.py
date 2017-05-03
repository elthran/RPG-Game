class MonsterProficiencies():
    def __init__(self):
        self.attack_damage = MonsterProficiency("Attack damage")
        self.health_maximum = MonsterProficiency("Health maximum")

class MonsterProficiency():
    def __init__(self, name):
        self.name = name
        self.value = 1

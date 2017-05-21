from math import floor, sin

MONSTER_PROFICIENCY_INFORMATION = [
    "Health",
    "Attack damage",
    "Attack speed",
    "Attack accuracy",
    "First strike",
    "Critical hit",
    "Defence",
    "Evade",
    "Parry",
    "Riposte",
    "Block"]


MONSTER_ALL_PROFICIENCIES = [attrib.lower().replace(" ", "_") for attrib in MONSTER_PROFICIENCY_INFORMATION]

class MonsterProficiencies():
    def __init__(self):
        self.health = MonsterHealth("Health maximum")
        self.attack_damage = MonsterAttackDamage("Attack damage")
        self.attack_speed = MonsterAttackSpeed("Attack speed")
        self.attack_accuracy = MonsterAttackAccuracy("Attack accuracy")
        self.first_strike = MonsterFirstStrike("First strike")
        self.critical_hit = MonsterCriticalHit("Critical hit")
        self.defence = MonsterDefence("Defence")
        self.evade = MonsterEvade("Evade")
        self.parry = MonsterParry("Parry")
        self.riposte = MonsterRiposte("Riposte")
        self.block = MonsterBlock("Block")

    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like ([(key, value), (key, value), ...])
        """
        return ((key, getattr(self, key)) for key in MONSTER_ALL_PROFICIENCIES)
        
        
    def __iter__(self):
        return (getattr(self, key) for key in MONSTER_ALL_PROFICIENCIES)

class MonsterProficiency():
    def __init__(self, name):
        self.name = name

    def update(self, monster):
        pass

class MonsterHealth(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.maximum = 10

    def update(self, monster):
        self.maximum = floor(4*monster.primary_attributes["Vitality"] + 0)
        
class MonsterAttackDamage(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.minimum = 1
        self.maximum = 2

    def update(self, monster):
        self.minimum = floor(floor(3 * (0.5*sin(0.1*monster.primary_attributes["Strength"]) + 0.1*monster.primary_attributes["Strength"])) + 0)
        self.maximum = floor(floor(3 * (0.5*sin(0.1*monster.primary_attributes["Strength"]) + 0.2*monster.primary_attributes["Strength"])) + 1)

class MonsterAttackSpeed(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.speed = 1.5

class MonsterAttackAccuracy(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.accuracy = 15

class MonsterFirstStrike(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.chance = 5

class MonsterCriticalHit(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.chance = 5
        self.modifier = 1.5

class MonsterDefence(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.modifier = 15

class MonsterEvade(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.chance = 5

class MonsterParry(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.chance = 5

class MonsterRiposte(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.chance = 5

class MonsterBlock(MonsterProficiency):
    def __init__(self, name):
        super().__init__(name)
        self.chance = 0
        self.modifier = 25

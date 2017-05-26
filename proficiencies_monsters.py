from math import floor, sin
from random import randint

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
    def __init__(self, monster_attributes):
        self.health = MonsterHealth("Health maximum", monster_attributes.vitality.level)
        self.attack_damage = MonsterAttackDamage("Attack damage", monster_attributes.strength.level)
        self.attack_speed = MonsterAttackSpeed("Attack speed", monster_attributes.agility.level)
        self.attack_accuracy = MonsterAttackAccuracy("Attack accuracy", monster_attributes.reflexes.level)
        self.first_strike = MonsterFirstStrike("First strike", monster_attributes.reflexes.level)
        self.critical_hit = MonsterCriticalHit("Critical hit", monster_attributes.agility.level)
        self.defence = MonsterDefence("Defence", monster_attributes.fortitude.level)
        self.evade = MonsterEvade("Evade", monster_attributes.reflexes.level)
        self.parry = MonsterParry("Parry", monster_attributes.reflexes.level)
        self.riposte = MonsterRiposte("Riposte", monster_attributes.reflexes.level)
        self.block = MonsterBlock("Block", monster_attributes.fortitude.level)

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

class MonsterHealth(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.maximum = floor(modifier*randint(275,325)*0.01)
        
class MonsterAttackDamage(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.minimum = floor(3 * (0.5*sin(0.1*modifier) + 0.1*modifier))
        self.maximum = floor(3 * (0.5*sin(0.1*modifier) + 0.2*modifier)) + 1

class MonsterAttackSpeed(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.speed = round((2.5 * (0.05*sin(0.3*modifier) + 0.08*modifier)) + 1, 2)

class MonsterAttackAccuracy(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.accuracy = floor((- (50*5)/((2 * modifier) + 50) + 5))

class MonsterFirstStrike(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (5*50)/((0.5 * modifier) + 5) + 50))

class MonsterCriticalHit(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (5*50)/((0.3 * modifier) + 5) + 50))
        self.modifier = floor((- (1*0.5)/((0.5 * modifier) + 1) + 0.5))

class MonsterDefence(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.modifier = floor((- (7*35)/((0.1 * modifier) + 7) + 35) * 5)

class MonsterEvade(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (10*15)/((0.1 * modifier) + 10) + 15) * 5)

class MonsterParry(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (15*15)/((0.2 * modifier) + 15) + 15) * 5)

class MonsterRiposte(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (20*15)/((0.3 * modifier) + 20) + 15) * 5)

class MonsterBlock(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (25*60)/((0.25 * modifier) + 25) + 60) * 5)
        self.modifier = floor((- (80*100)/((2.5 * modifier) + 80) + 100) * 5)

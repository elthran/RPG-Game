from math import floor, sin
from random import randint

MONSTER_PROFICIENCY_INFORMATION = [
    "Health",
    "Damage",
    "Speed",
    "Accuracy",
    "Killshot",
    "First Strike",
    "Defence",
    "Evade",
    "Parry",
    "Riposte",
    "Block"]


MONSTER_ALL_PROFICIENCIES = [attrib.lower().replace(" ", "_") for attrib in MONSTER_PROFICIENCY_INFORMATION]

class MonsterProficiencies():
    def __init__(self, monster_attributes):
        self.health = MonsterHealth("Health", monster_attributes.vitality.level)
        self.damage = MonsterDamage("Damage", monster_attributes.brawn.level)
        self.speed = MonsterSpeed("Speed", monster_attributes.agility.level)
        self.accuracy = MonsterAccuracy("Accuracy", monster_attributes.quickness.level)
        self.killshot = MonsterKillshot("Killshot", monster_attributes.quickness.level)
        self.first_strike = MonsterFirstStrike("First strike", monster_attributes.agility.level)
        self.defence = MonsterDefence("Defence", monster_attributes.resilience.level)
        self.evade = MonsterEvade("Evade", monster_attributes.quickness.level)
        self.parry = MonsterParry("Parry", monster_attributes.quickness.level)
        self.riposte = MonsterRiposte("Riposte", monster_attributes.quickness.level)
        self.fatigue = MonsterFatigue("Fatigue", monster_attributes.resilience.level)
        self.block = MonsterBlock("Block", monster_attributes.resilience.level)

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
        self.current = self.maximum
        
class MonsterDamage(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.minimum = floor(3 * (0.5*sin(0.1*modifier) + 0.1*modifier))
        self.maximum = floor(3 * (0.5*sin(0.1*modifier) + 0.2*modifier)) + 1

class MonsterSpeed(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.speed = round((2.5 * (0.05*sin(0.3*modifier) + 0.08*modifier)) + 1, 2)

class MonsterAccuracy(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.accuracy = floor((- (50*5)/((2 * modifier) + 50) + 5))

class MonsterKillshot(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (5*50)/((0.5 * modifier) + 5) + 50))
        self.modifier = floor((- (1*0.5)/((0.5 * modifier) + 1) + 0.5))

class MonsterFirstStrike(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (5*50)/((0.3 * modifier) + 5) + 50))

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

class MonsterFatigue(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.maximum = floor(modifier) + randint(1,3)
        self.current = self.maximum

class MonsterBlock(MonsterProficiency):
    def __init__(self, name, modifier):
        super().__init__(name)
        self.chance = floor((- (25*60)/((0.25 * modifier) + 25) + 60) * 5)
        self.modifier = floor((- (80*100)/((2.5 * modifier) + 80) + 100) * 5)

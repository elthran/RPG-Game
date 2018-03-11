"""
Test combat simulator.
"""

from combat_simulator import battle_logic, determine_attacker
from hero import Hero

"""
Inventory: work in progress
Useful: 

python3 -m pytest -x -vv -l -s rpg_game_tests/test_combat_simulator.py

PS> clear;pytest -x -vv -l -s
$ cls && pytest -x -vv -l -s

s - no output capture (shows print statement output)
x - exit after first failed test
v - verbose
vv - show full length output
l - show local vars during traceback (when a test fails)
"""

class TestCombat:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls, delete=True):
        pass

    def setup(self):
        print("Setup is running.")
        self.hero1 = Hero(name="sample1")
        # self.hero1.base_proficiencies['speed'].level += 1
        self.hero2 = Hero(name="sample2")

    def teardown(self):
        print("Teardown is running.")
        pass

    def precision_gauge(self, checked, correct, desired_percent):
        precision = (desired_percent / 100) * checked
        return correct - precision < checked < correct + precision


    def test_stop_when_death(self):
        results = battle_logic(self.hero1,self.hero2)
        assert self.hero1.base_proficiencies['health'].current == 0 or self.hero2.base_proficiencies['health'].current == 0

    def test_no_negative_health(self):
        results = battle_logic(self.hero1, self.hero2)
        assert self.hero1.base_proficiencies['health'].current >= 0 or self.hero2.base_proficiencies['health'].current >= 0

    def test_determine_attacker_distribution(self):
        number_of_battle_tests = 10000
        hero1count = 0
        hero2count = 0
        for i in range(number_of_battle_tests):
            attacker,defender = determine_attacker(self.hero1, self.hero2)
            if attacker.name == self.hero1.name:
                hero1count += 1
            if attacker.name == self.hero2.name:
                hero2count += 1
            # self.setup() would recreate the two heros from scratch
        print(hero1count,hero2count)
        assert self.precision_gauge(hero1count, number_of_battle_tests/2, 5) == True




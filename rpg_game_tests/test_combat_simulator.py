"""
Test combat simulator.
"""
import pytest
from combat_simulator.combat_simulator import battle_logic, determine_attacker, determine_if_hits, determine_if_critical_hit, calculate_damage, add_killshot_multiplier
from models.hero import Hero

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


@pytest.mark.slow
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
        self.hero1.base_proficiencies['killshot'].level += 5
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
        print("Hero1 attacks vs. hero2 attacks:", hero1count,hero2count)
        assert self.precision_gauge(hero1count, number_of_battle_tests/2, 5) == True

    def test_determine_if_attacker_hits(self):
        number_of_battle_tests = 10000
        hits = 0
        misses = 0
        for i in range(number_of_battle_tests):
            if determine_if_hits(self.hero1, self.hero2):
                hits += 1
            else:
                misses += 1
        print("Hits vs. misses:", hits, misses)
        assert self.precision_gauge(hits, number_of_battle_tests * 0.75, 5) == True

    def test_determine_if_attacker_critical_hits(self):
        number_of_battle_tests = 50000
        critical_hits = 0
        critical_misses = 0
        for i in range(number_of_battle_tests):
            if determine_if_critical_hit(self.hero1):
                critical_hits += 1
            else:
                critical_misses += 1
        print("Critical hits vs. misses:", critical_hits, critical_misses)
        assert self.precision_gauge(critical_hits, number_of_battle_tests * 0.01, 5) == True

    def test_determine_damage(self):
        number_of_battle_tests = 10000
        lowest_damage = 99999
        highest_damage = -10
        total_damage = 0
        for i in range(number_of_battle_tests):
            damage = calculate_damage(self.hero1, self.hero2)
            if damage < lowest_damage:
                lowest_damage = damage
            elif damage > highest_damage:
                highest_damage = damage
            total_damage += damage
        average_damage = total_damage / number_of_battle_tests
        print("Average damage:", average_damage)
        assert average_damage >= 0
        assert 0 <= lowest_damage < average_damage
        assert lowest_damage < highest_damage < 100

    def test_determine_damage_multiplier(self):
        number_of_battle_tests = 10000
        old_damage = 0
        multiplied_damage = 0
        for i in range(number_of_battle_tests):
            damage = calculate_damage(self.hero1, self.hero2)
            new_damage = add_killshot_multiplier(self.hero1, damage)
            old_damage += damage
            multiplied_damage += new_damage
        old_average_damage = old_damage / number_of_battle_tests
        multiplied_average_damage = multiplied_damage / number_of_battle_tests
        print("Old vs. multiplied average damage:", old_average_damage, multiplied_average_damage)
        assert 0 < old_average_damage < multiplied_average_damage



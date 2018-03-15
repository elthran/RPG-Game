from events import Condition
from locations import Location


class TestCondition:
    def test_init(self):
        blacksmith = Location('Blacksmith', 'store')
        blacksmith_condition = Condition('current_location', '==', blacksmith)

        assert blacksmith_condition.code == 'self.trigger.hero.current_location.id == self.location.id'

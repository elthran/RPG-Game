from events import Condition
from locations import Location


class TestCondition:
    def setup(self):
        self.blacksmith = Location('Blacksmith', 'store')
        self.blacksmith_condition = Condition('current_location', '==', self.blacksmith)

    def test_init(self):
        assert self.blacksmith_condition.code == 'self.trigger.hero.current_location.id == self.location.id'

        blacksmith_is_parent_of_current_location_condition = Condition('current_location.parent', '==', self.blacksmith)

        assert blacksmith_is_parent_of_current_location_condition.code == 'self.trigger.hero.current_location.parent.id == self.location.id'

    def test_clone(self):
        blacksmith_condition_clone = self.blacksmith_condition.clone()

        assert blacksmith_condition_clone.code == self.blacksmith_condition.code and blacksmith_condition_clone is not self.blacksmith_condition

if __name__ == "__main__":
    import os
    os.system("python3 -m pytest -vv {}".format(__file__))
    exit()  # prevents code from trying to run file afterwards.

import pdb

from events import Condition
from locations import Location
from . import Mock


class TestCondition:
    def setup(self):
        self.blacksmith = Location('Blacksmith', 'store')
        self.blacksmith_condition = Condition('current_location', '==', self.blacksmith)

    def test_init(self):
        assert self.blacksmith_condition.code == 'hero.current_location.id == self.location.id'

        blacksmith_is_parent_of_current_location_condition = Condition('current_location.parent', '==', self.blacksmith)

        assert blacksmith_is_parent_of_current_location_condition.code == 'hero.current_location.parent.id == self.location.id'

    def test_eval(self):
        condition = self.blacksmith_condition
        mock_hero = Mock('current_location.id', 5)
        condition.location.id = 5
        assert eval(condition.code, {'self': condition, 'hero': mock_hero}) is True

        condition.location.id = 4
        assert eval(condition.code, {'self': condition, 'hero': mock_hero}) is False

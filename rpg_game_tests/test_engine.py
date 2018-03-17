if __name__ == "__main__":
    import os
    os.system("python3 -m pytest -vv {}".format(__file__))
    exit()  # prevents code from trying to run file afterwards.

import pdb

from . import GenericTestCase, Mock, db_execute_script
from engine import Engine
from locations import Location
from events import Condition, Trigger
from hero import Hero


class TestEngine(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        # Might be better for testing? To allow post mortem analysis.
        db.engine.execute("DROP TABLE `event`;")
        db_execute_script("static/drop_hero_table.sql", db)
        db = super().setup_class()

        equip_item_trigger = Trigger(
            'equip_event',
            conditions=[],
            extra_info_for_humans="Should activate when equip_event spawns."
        )
        hero = Hero(name="Haldon")
        hero.triggers.append(equip_item_trigger)
        db.session.add(hero)
        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)

    def test_spawn(self):
        engine = Engine(self.db)

        hero = self.db.session.query(Hero).get(1)

        mock_item = Mock("name", 'Blade')
        engine.spawn(
                'equip_event',
                hero,
                description="{} equips a/an {}.".format(hero.name, mock_item.name)
        )

        assert hero.triggers[0].completed is True

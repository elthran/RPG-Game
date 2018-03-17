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
from quests import QuestPath, Quest


class TestEngine(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        # Might be better for testing? To allow post mortem analysis.
        db.engine.execute("DROP TABLE IF EXISTS `event`;")
        db_execute_script("static/drop_hero_table.sql", db)
        db.engine.execute("DROP TABLE IF EXISTS `display`;")
        db.engine.execute("DROP TABLE IF EXISTS `adjacent_location_association`;")
        db.engine.execute("DROP TABLE IF EXISTS `location`;")
        db = super().setup_class()

        # Locations
        blacksmith = Location('Blacksmith', 'store')

        #########
        # Conditions
        #########
        blacksmith_condition = Condition('current_location', '==', blacksmith)
        blacksmith_is_parent_of_current_location_condition \
            = Condition('current_location.parent', '==', blacksmith)


        ##########
        # Triggers
        ##########
        visit_blacksmith_trigger = Trigger(
            'move_event', conditions=[blacksmith_condition],
            extra_info_for_humans='Should activate when '
                                  'the hero.current_location.id == the id of the '
                                  'blacksmith object.')

        buy_item_from_blacksmith_trigger = Trigger(
            'buy_event',
            conditions=[blacksmith_is_parent_of_current_location_condition],
            extra_info_for_humans='Should activate when buy code runs and '
                                  'hero.current_location.id == id of the blacksmith.'
        )

        equip_item_trigger = Trigger(
            'equip_event',
            conditions=[],
            extra_info_for_humans="Should activate when equip_event spawns."
        )

        unequip_item_trigger = Trigger(
            'unequip_event',
            conditions=[],
            extra_info_for_humans="Should activate when unequip_event spawns."
        )

        ###########
        # Quests
        ##########
        blacksmith_quest_stage1 = Quest(
            "Go talk to the blacksmith",
            "Find the blacksmith in Thornwall and enter his shop.",
            trigger=visit_blacksmith_trigger
        )

        blacksmith_quest_stage2 = Quest(
            "Buy your first item",
            "Buy any item from the blacksmith.",
            reward_experience=4,
            trigger=buy_item_from_blacksmith_trigger
        )

        inventory_quest_stage1 = Quest(
            "Equip an item",
            "Equip any item in your inventory.",
            trigger=equip_item_trigger
        )

        inventory_quest_stage2 = Quest(
            "Unequip an item",
            "Unequip any item in your inventory.",
            trigger=unequip_item_trigger
        )

        ###########
        # QuestPaths
        ###########
        meet_the_blacksmith_path = QuestPath(
            "Get Acquainted with the Blacksmith",
            "Find the blacksmith and buy something from him.",
            quests=[blacksmith_quest_stage1, blacksmith_quest_stage2]
        )

        learn_about_your_inventory_path = QuestPath(
            "Learn how your inventory works",
            "Practice equipping an unequipping.",
            quests=[inventory_quest_stage1, inventory_quest_stage2],
            is_default=True
        )

        hero = Hero(name="Haldon")
        hero.journal.quest_paths = [learn_about_your_inventory_path]
        db.session.add(hero)
        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)

    def setup(self):
        super().setup()
        self.hero = self.db.session.query(Hero).filter_by(name="Haldon").one()
        self.inventory_path = self.db.session.query(QuestPath).filter_by(name="Learn how your inventory works", template=True).one()

    def test_spawn(self):
        engine = Engine(self.db)

        trigger_id = self.hero.triggers[0].id
        current_quest_id = self.inventory_path.current_quest.id

        mock_item = Mock("name", 'Blade')
        engine.spawn(
                'equip_event',
                self.hero,
                description="{} equips a/an {}.".format(self.hero.name, mock_item.name)
        )

        self.rebuild_instance()

        assert trigger_id not in [t.id for t in self.hero.triggers]
        assert current_quest_id != [qp.current_quest.id for qp in hero.journal.quest_paths if qp.name == "Learn how your inventory works"]

        # Check if deactive triggers get garbage collected.
        self.rebuild_instance()

        assert self.db.session.query(Trigger).filter_by(event_name="Deactivated").count() == 0


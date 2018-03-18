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
            conditions=[blacksmith_condition],
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
        db.session.add(meet_the_blacksmith_path)
        db.session.add(hero)
        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)

    def setup(self):
        super().setup()
        self.hero = self.db.session.query(Hero).filter_by(name="Haldon").one()
        self.inventory_path = self.db.session.query(QuestPath).filter_by(name="Learn how your inventory works", template=True).one()
        self.meet_the_blacksmith_path = self.db.session.query(QuestPath).filter_by(name="Get Acquainted with the Blacksmith", template=True).one()
        self.blacksmith = self.db.session.query(Location).filter_by(name="Blacksmith").one()

    def test_spawn(self):
        engine = Engine(self.db)

        # assert len(self.hero.triggers) == 1
        # trigger_id = self.hero.triggers[0].id
        current_quest_id = self.inventory_path.current_quest.id

        mock_item = Mock("name", 'Blade')
        engine.spawn(
                'equip_event',
                self.hero,
                description="{} equips a/an {}.".format(self.hero.name, mock_item.name)
        )

        self.rebuild_instance()

        # assert len(self.hero.triggers) == 1
        # assert trigger_id in [t.id for t in self.hero.triggers]
        assert current_quest_id != [qp.current_quest.id for qp in self.hero.journal.quest_paths if qp.name == "Learn how your inventory works"]

    def test_blacksmith_quest(self):
        self.hero.journal.quest_paths.append(self.meet_the_blacksmith_path)
        self.hero.current_location = self.blacksmith
        self.db.session.commit()
        trigger_id = self.hero.handlers[0].trigger.id
        handler_id = self.hero.handlers[0].id
        # assert len(self.hero.triggers) == 1

        assert self.hero.journal.current_quest_paths[0].id != self.meet_the_blacksmith_path.id
        # Now for the Engine.
        engine = Engine(self.db)
        engine.spawn(
            'move_event',
            self.hero,
            description="{} visits {}.".format(self.hero.name, self.blacksmith.url)
        )

        self.rebuild_instance()
        assert handler_id != self.hero.handlers[0].id
        assert len(self.hero.handlers) == 1
        assert trigger_id != self.hero.handlers[0].trigger.id
        # assert len(self.hero.triggers) == 1

        engine.spawn(
                'buy_event',
                self.hero,
                description="{} buys a/an {}.".format(self.hero.name, "Sword.")
            )

        self.rebuild_instance()
        assert self.hero.handlers == []
        # assert self.hero.triggers == []

    def test_only_correct_event_triggers_handler(self):
        hero = Hero(name="Elthran")
        hero.journal.quest_paths.append(self.inventory_path)
        hero.journal.notification = None
        self.db.session.add(hero)
        self.db.session.commit()

        engine = Engine(self.db)
        engine.spawn(
                'buy_event',
                self.hero,
                description="{} buys a/an {}.".format(self.hero.name, "Sword")
            )

        hero = self.db.session.query(Hero).filter_by(name="Elthran").one()
        assert len(hero.journal.current_quest_paths) == 1
        assert hero.journal.quest_paths[0].stage == 0

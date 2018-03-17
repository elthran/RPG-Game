import pdb

import pytest

from database import EZDB
from hero import Hero
from quests import Quest, QuestPath
from locations import Location
from events import Condition, Trigger
from . import GenericTestCase, db_execute_script, Mock


@pytest.mark.incremental
class TestQuestPath(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        db_execute_script("static/drop_hero_table.sql", db)
        db = super().setup_class()  # Rebuild schema.


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

        learn_about_your_inventory_path = QuestPath(
            "Learn how your inventory works",
            "Practice equipping an unequipping.",
            quests=[inventory_quest_stage1, inventory_quest_stage2],
            is_default=True
        )

        hero = Hero(name="Haldon")
        db.session.add_all([learn_about_your_inventory_path, hero])
        db.update()

    @classmethod
    def teardown_class(cls, delete=False):
        super().teardown_class(delete=delete)

    def setup(self):
        super().setup()
        self.inventory_path = self.db.session.query(QuestPath).filter_by(name="Learn how your inventory works", template=True).one()
        self.hero = self.db.session.query(Hero).filter_by(name="Haldon").one()

    def test_current_quest(self):
        str_current_quest = self.inventory_path.current_quest.pretty
        self.inventory_path.stage += 1

        self.rebuild_instance()
        assert str_current_quest != self.inventory_path.current_quest.pretty

    def test_activate(self):
        current_quest_trigger_id = self.inventory_path.current_quest.trigger.id
        hero_id = self.hero.id
        self.inventory_path.activate_handler(self.hero)

        self.rebuild_instance()

        assert current_quest_trigger_id == self.inventory_path.current_quest.trigger.id
        assert current_quest_trigger_id != self.hero.triggers[0].id
        assert self.inventory_path._hero_id == hero_id

    def test_path_advance(self):
        self.inventory_path.journal = self.hero.journal

        initial_completed = self.inventory_path.completed
        current_quest_id = self.inventory_path.current_quest.id
        active_trigger_id = self.hero.triggers[0].id
        next_quest_trigger_id = self.inventory_path.current_quest.trigger.id

        self.inventory_path.advance()
        self.rebuild_instance()

        assert initial_completed is False
        assert self.inventory_path.completed is True
        # Since path is completed current quest remains the same.
        assert current_quest_id == self.inventory_path.current_quest.id
        assert self.hero.triggers == []
        assert self.inventory_path._hero_id is None
        assert self.inventory_path.trigger is None
        # Make sure advance hasn't build a bunch blank triggers behind.
        assert self.db.session.query(Trigger).filter_by(template=False).count() == 0

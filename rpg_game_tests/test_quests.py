import pdb

import pytest

from hero import Hero
from quests import Quest, QuestPath
from events import Handler, Trigger
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
        self.hero = self.db.session.query(Hero).filter_by(name="Haldon").one()

    def test_current_quest(self):
        inventory_path = self.db.session.query(QuestPath).filter_by(name="Learn how your inventory works", template=True).one()
        str_current_quest = inventory_path.current_quest.pretty
        inventory_path.stage += 1

        self.rebuild_instance()

        inventory_path = self.db.session.query(QuestPath).filter_by(name="Learn how your inventory works", template=True).one()
        assert str_current_quest != inventory_path.current_quest.pretty

    def test_activate(self):
        inventory_path = self.db.session.query(QuestPath).filter_by(name="Learn how your inventory works", template=True).one()
        current_quest_trigger_id = inventory_path.current_quest.trigger.id
        hero_id = self.hero.id
        self.hero.journal.quest_paths.append(inventory_path)
        assert self.hero.journal.quest_paths[0].journal is not None

        self.rebuild_instance()

        inventory_path = self.hero.journal.quest_paths[0]
        assert current_quest_trigger_id == inventory_path.current_quest.trigger.id
        # assert current_quest_trigger_id == self.hero.triggers[0].id
        assert self.hero.handlers != []
        assert self.hero.handlers[0].hero.id == hero_id

    def test_path_advance_complete(self):
        inventory_path = self.hero.journal.quest_paths[0]
        initial_completed = inventory_path.completed
        current_quest_id = inventory_path.current_quest.id
        # active_trigger_id = self.hero.triggers[0].id
        next_quest_trigger_id = inventory_path.current_quest.trigger.id

        assert self.hero.journal.quest_paths is not []
        assert inventory_path.journal is not None

        inventory_path.advance()
        self.rebuild_instance()

        inventory_path = self.hero.journal.quest_paths[0]
        assert initial_completed is False
        assert inventory_path.completed is True
        # Since path is completed current quest remains the same.
        assert current_quest_id == inventory_path.current_quest.id
        # assert self.hero.triggers == []
        assert self.hero.handlers == []
        # Make sure no triggers have been deleted.
        assert self.db.session.query(Trigger).count() == 2
        # Make sure advance hasn't build a bunch blank handlers behind.
        assert self.db.session.query(Handler).count() == 0

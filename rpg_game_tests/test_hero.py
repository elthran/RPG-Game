import pdb

from . import GenericTestCase, db_execute_script

from hero import Hero
from items import Ring
from events import Condition, Trigger
from locations import Location
from quests import Quest, QuestPath
from engine import Engine


class TestHero(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        # Might be better for testing? To allow post mortem analysis.
        db_execute_script("static/drop_hero_table.sql", db)
        db = super().setup_class()

        hero = Hero()
        db.session.add(hero)
        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)

    def setup(self):
        super().setup()
        self.hero = self.db.session.query(Hero).get(1)

    def test_init(self):
        """See if a basic hero can be created and doesn't crash."""
        hero = self.hero
        str_hero = hero.pretty

        self.rebuild_instance()
        hero2 = self.hero
        assert str_hero == hero2.pretty is not None

    def test_modify_max_health(self):
        """Check if the hero's max health can be modified.

        It can be raised by:
            -adding points to the Health Proficiency
            -by equipping Items
            -by using Abilities.

        Does your character have a max health?
        Can he raise it by adding points into the health proficiency or by
        equipping items/abilities that add max health?
        """
        health = self.hero.get_summed_proficiencies('health')

        assert health.final == 5
        max_health = health.final
        self.hero.base_proficiencies.health.level += 10

        self.rebuild_instance()
        max_health2 = self.hero.get_summed_proficiencies('health').final
        assert max_health < max_health2

        item = Ring("Silver Ring", 8, style="silver",
                    proficiency_data=[('Health', {'base': 50})])
        self.db.session.add(item)
        self.db.session.commit()
        self.hero.inventory.equip(item)
        self.rebuild_instance()

        assert max_health2 < self.hero.get_summed_proficiencies('health').final

    def test_blacksmith_quest(self):
        """

        hero
        trigger
        condition
        quest
        questpath?
        """
        blacksmith = Location('Blacksmith', 'store')
        blacksmith_condition = Condition('current_location', '==', blacksmith)
        visit_blacksmith_trigger = Trigger('move_event', conditions=[blacksmith_condition], extra_info_for_humans='Should activate when the hero.current_location.id == the id of the blacksmith object.')
        buy_item_from_blacksmith_trigger = Trigger(
            'buy_event',
            conditions=[blacksmith_condition],
            extra_info_for_humans='Should activate when buy code runs and '
                                  'hero.current_location.id == id of the blacksmith.'
        )
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
        meet_the_blacksmith_path = QuestPath(
            "Get Acquainted with the Blacksmith",
            "Find the blacksmith and buy something from him.",
            quests=[blacksmith_quest_stage1, blacksmith_quest_stage2]
        )

        # Ok that is all the setup. I wish it were simpler.
        self.hero.journal.quest_paths.append(meet_the_blacksmith_path)
        # self.db.session.add(blacksmith_condition)
        self.db.session.commit()

        assert [obj.id for obj in self.hero.journal.current_quest_paths] == [1]
        # Now for the Engine.
        engine = Engine(self.db)

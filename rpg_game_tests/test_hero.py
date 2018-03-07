from . import GenericTestCase, db_execute_script

from hero import Hero
from items import Ring


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

        like does your character have a max health? can he raise it by adding points into the health proficiency or by equipping items/abilities that add max health?
        """
        print()
        print(self.hero.proficiencies.health.maximum)
        health = self.hero.proficiencies.health

        max_health = health.maximum
        health.level += 10

        self.rebuild_instance()
        max_health2 = self.hero.proficiencies.health.maximum
        assert max_health < max_health2

        item = Ring("Silver Ring", 8, style="silver", health_maximum=50)
        self.db.session.add(item)
        self.db.session.commit()
        self.hero.inventory.equip(item)
        self.rebuild_instance()

        assert max_health2 < self.hero.proficiencies.health.maximum

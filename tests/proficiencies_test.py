import pytest

from database import EZDB
from game import Hero

from proficiencies import Proficiencies, Health


class TestProficiency:
    def setup(self):
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)

    def teardown(self, delete=False):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()

    def rebuild_instance(self):
        """Tidy up and rebuild database instance.

        ... otherwise you may not be retrieving the actual data
        from the database only from memory.
        """

        self.db.session.commit()
        self.teardown(delete=False)
        self.setup()

    def test_Health_init(self):
        """Check if object is created, storeable and retrievable.
        """

        proficiencies = Proficiencies()
        proficiencies.pprint()
        self.db.session.add(proficiencies)
        self.db.session.commit()

        id = proficiencies.id
        health = proficiencies.health
        str_health = health.pretty

        self.rebuild_instance()
        health2 = self.db.session.query(
            Health).filter_by(name="Health", proficiencies_id=id).first()
        print("health", str_health)
        print(health2.pretty)
        assert str_health == health2.pretty != ''

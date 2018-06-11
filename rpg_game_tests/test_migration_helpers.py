
"""
To add current directory to sys.path run like this:
NOTE: cls is an alias in .bash_alias cls="clear && printf '\033[3J'"

$ cls;python3 -m pytest -x -vv -l -s rpg_game_tests/test_migration_helpers.py

s - no output capture (shows print statement output)
x - exit after first failed test
v - verbose
vv - show full length output
l - show local vars during traceback (when a test fails)
"""


import rpg_game_tests.test_helpers
import sqlalchemy as sa
import sqlalchemy.orm
import migrations.migration_helpers


class TestMigrationHelpers:
    @classmethod
    def setup_class(cls):
        # Might be better for testing? To allow post mortem analysis.
        cls.Session = sa.orm.sessionmaker()

        # Connect to the old database (the one I'm migrating data from).
        cls.engine = sa.create_engine("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database" + "?charset=utf8mb4", pool_recycle=3600)
        # using the session.
        cls.meta = sa.MetaData(bind=cls.engine)
        cls.meta.reflect()

        cls.session = cls.Session(bind=cls.engine)
        cls.table_query = migrations.migration_helpers.TableQuery(cls.session, cls.meta)

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        pass

    def test_query(self):
        """Check if object is created, storeable and retrievable.
        """
        # testing
        for thread in self.table_query('thread').filter_by(board_id=1).all():
            print(thread.board)
        exit(0)
        # assert

    def test_query_relationships(self):
        """Check if object is created, storeable and retrievable.
        """
        pass
        # assert

    def test_query_filter(self):
        pass

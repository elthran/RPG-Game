
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
import pdb

import pytest
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
        cls.engine.dispose()
        cls.session.close()

    def setup(self):
        pass

    def test_query(self):
        """Check basic query and attribute access works normally.
        """
        account = self.table_query('account').first()
        assert account.username is not None and isinstance(account.username, str)

    def test_query_relationships(self):
        """Check if inferred relationships work.

        Check that repeated relationship access works while still allowing
        normal attribute access.
        """
        account = self.table_query('account').first()
        assert account.hero is not None
        assert isinstance(account.hero, list)
        hero = self.table_query('hero').first()
        assert hero.account is not None
        assert isinstance(hero.account, migrations.migration_helpers.SmartResult)
        assert len(hero.account) == 1
        assert isinstance(hero.account.hero, list)
        assert isinstance(hero.account.hero[0].name, str)

    def test_query_filter(self):
        """Check that you can do multi-layered queries.

        Make sure that repeated calls still return viable magic results.
        """
        thread_query = self.table_query('thread')
        filtered_query = thread_query.filter_by(board_id=1)
        thread = filtered_query.first()
        assert thread.board is not None

        for thread in self.table_query('thread').filter_by(board_id=thread.board.id).all():
            assert thread is not None
            assert isinstance(thread.name, str)

    def test_sensible_errors(self):
        with pytest.raises(KeyError) as exc_info:
            self.table_query('no_table')
        assert "No table named 'no_table' exists." in str(exc_info.value)

        account = self.table_query('account').first()
        with pytest.raises(AttributeError) as exc_info:
            raise account.name
        assert "'result' object has no attribute 'name'" in str(exc_info.value)

        with pytest.raises(AttributeError) as exc_info:
            # pdb.set_trace()
            raise account.journal
        assert "'result' object has no attribute 'journal'" in str(exc_info.value)

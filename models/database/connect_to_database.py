# import importlib
import pdb
import socket
import datetime

import sqlalchemy as sa
import sqlalchemy.orm

import models
# from session_helpers import scoped_session, safe_commit_session
import services

import private_config

# Constants#
Session = sa.orm.sessionmaker()


class EZDB:
    """Basic frontend for SQLAlchemy.

    This class allows you to use the old game methods with modern SQLAlchemy.
    At some point it may be worth using SQLAlchemy directly.

    All add_* methods should end with a commit!
    """
    def __init__(self, database="sqlite:///:memory:", debug=True,
                 testing=False):
        """Create a basic SQLAlchemy engine and session.

        Attribute "file_name" is used to find location of database for python.

        Hidden method: _delete_database is for testing and does what it
        sounds like it does :).
        """
        first_run = False
        server = database[0:database.rindex('/')]
        name = database.split('/').pop()
        self.filename = name

        engine = sa.create_engine(
            server + "/?charset=utf8mb4", pool_recycle=3600, echo=debug)

        # Build a new database if this one doesn't exist.
        # Also set first_run variable!
        if not engine.execute("SHOW DATABASES LIKE '{}';".format(name)).first():
            print("Building database for first time!")
            first_run = True
            engine.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(name))

        # Select the database ... not sure if I need this.
        # Or if I should create a new engine instead ..
        engine = sa.create_engine(
            database + "?charset=utf8mb4", pool_recycle=3600, echo=debug)

        models.Base.metadata.create_all(engine, checkfirst=True)
        models.Base.metadata.bind = engine

        # Set up Session for this engine.
        Session.configure(bind=engine)
        self.Session = Session
        models.Base.Session = Session

        self.engine = engine
        self.session = self.Session()
        if first_run and not testing:
            self.add_prebuilt_objects()

    def add_prebuilt_objects(self):
        """Add all the predefined object into the database.

        If one is already there then ignore and continue.
        Note: each prebuilt_object must be a list.
        NOTE2: users must come first as it somehow gets built before it gets
        built if it doesn't?
        Maybe because .. it has a hero which has a current_world? So when
        current_world gets
        built then the user gets built too? Which may mean most of my code
        here is redundant
        and I only really need to build the users list?
        """

        # global prebuilt_objects
        # I can't remember why I need to reload this ...
        import prebuilt_objects
        # importlib.reload(prebuilt_objects)

        for obj_list in [
                prebuilt_objects.users,
                prebuilt_objects.game_worlds,
                # prebuilt_objects.all_abilities,
                prebuilt_objects.all_store_items,
                prebuilt_objects.all_marketplace_items,
                prebuilt_objects.all_quests,
                prebuilt_objects.all_specializations,
                prebuilt_objects.all_forums,
                prebuilt_objects.all_monsters]:
            for obj in obj_list:
                self.session.add(obj)
                if isinstance(obj, models.Account):
                    obj.password = services.secrets.encrypt(obj.password)
                    obj.timestamp = datetime.datetime.utcnow()
                self.update()
        default_quest_paths = self.get_default_quest_paths()
        for hero in self.session.query(models.Hero).all():
            hero.journal.quest_paths = default_quest_paths
        self.update()

    def update(self):
        """Commit, handle errors, close the session, open a new one.

        Provide a context manager type behavior for the session.
        See:
        http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
        """
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            self.session = self.Session()

    def get_default_quest_paths(self):
        """Return the quest that are applied to starting heroes.

        NOTE: This is a placeholder! The implementation should probably have
        a "is_default" flag for QuestPath objects.
        """
        return self.session.query(
            models.quests.QuestPath).filter_by(
            is_default=True, template=True).all()


# INIT AND LOGIN FUNCTIONS
if 'liveweb' not in socket.gethostname():  # Running on local machine.
    database_url = private_config.LOCAL_DATABASE_URL
else:  # Running on server which runs dotenv from WSGI file.
    database_url = private_config.SERVER_DATABASE_URL


ezdb = EZDB(database_url, debug=False)

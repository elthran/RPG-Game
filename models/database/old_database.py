"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at:
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import services.readability
import models
from . import sessions


# Constants#
# UPDATE_INTERVAL = 3600  # One endurance per hour.
UPDATE_INTERVAL = 30  # One endurance per 30 seconds
PASSWORD_HASH_COST = 10
Session = sessionmaker()


class EZDB:
    """Basic frontend for SQLAlchemy.

    This class allows you to use the old game methods with modern SQLAlchemy.
    At some point it may be worth using SQLAlchemy directly.

    All add_* methods should end with a commit!
    """
    def __init__(self, database="sqlite:///:memory:", debug=True):
        """Create a basic SQLAlchemy engine and session.

        Attribute "file_name" is used to find location of database for python.

        Hidden method: _delete_database is for testing and does what it
        sounds like it does :).
        """
        server = database[0:database.rindex('/')]
        name = database.split('/').pop()
        self.filename = name

        engine = create_engine(
            server + "/?charset=utf8mb4", pool_recycle=3600, echo=debug)

        # Build a new database if this one doesn't exist.
        # Also set first_run variable!
        if not engine.execute("SHOW DATABASES LIKE '{}';".format(name)).first():
            print("Building database for first time!")
            engine.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(name))

        # Select the database ... not sure if I need this.
        # Or if I should create a new engine instead ..
        engine = create_engine(
            database + "?charset=utf8mb4", pool_recycle=3600, echo=debug)

        models.Base.metadata.create_all(engine, checkfirst=True)

        # Set up Session for this engine.
        Session.configure(bind=engine)
        self.Session = Session

        self.engine = engine
        self.session = self.Session()

    def update_time_all_heroes(self):
        """Run update_time on all hero objects.

        Consider moving the While True: + sleep somewhere else?
        Seems a little out of place here.
        """

        for hero in models.Hero.query.all():
            self.update_time(hero)

    # Marked for renaming as it effects Hero endurance as well as time.
    # Consider update_endurance_and_time()
    # Or update_game_clock
    # Or update_hero_clock
    @sessions.safe_commit_session
    def update_time(self, hero):
        """Update the game time clock of a specific Hero and endurance values.

        This increases the hero's endurance by the difference between past
        timestamp and current time.
        NOTE: Updates current timestamp in character table but only if has
        been incremented.
        Which may not be a good idea but ...

        Suggestion: Currently only affects the passed Hero, perhaps it
        should update all heroes?
        """

        endurance = hero.base_proficiencies['endurance']
        summed_endurance = hero.get_summed_proficiencies('endurance')
        stamina = hero.get_summed_proficiencies('stamina')
        stamina = services.readability.round_number_intelligently(stamina.final)
        endurance.current = min(endurance.current + stamina, summed_endurance.final)

        health = hero.base_proficiencies['health']
        summed_health = hero.get_summed_proficiencies('health')
        regeneration = hero.get_summed_proficiencies('regeneration')
        regeneration = services.readability.round_number_intelligently(regeneration.final)
        health.current = min(health.current + regeneration, summed_health.final)

        sanctity = hero.base_proficiencies['sanctity']
        summed_sanctity = hero.get_summed_proficiencies('sanctity')
        redemption = hero.get_summed_proficiencies('redemption')
        redemption = services.readability.round_number_intelligently(redemption.final)
        sanctity.current = min(sanctity.current + redemption, summed_sanctity.final)

        for item in hero.equipped_items():
            item.affinity += 1

        # print("Hero {} updated on schedule.".format(hero.id))

    def _delete_database(self):
        """Deletes current database file.

        Use with caution, mainly for testing.
        """
        self.engine.execute(
            "DROP DATABASE IF EXISTS {};".format(self.filename))

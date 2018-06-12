import os
import sys
import pdb
import inspect

import sqlalchemy as sa

# Get the name of the current directory for this file and split it.
old_path = os.path.dirname(__file__).split(os.sep)
new_path = os.sep.join(old_path[:-1])
# -1 refers to how many levels of directory to go up
sys.path.insert(0, new_path)
from __init__ import *

import database as db
from services.naming import normalize_attrib_name, normalize_class_name
from rpg_game_tests.test_helpers import db_execute_script
from migrations import migration_helpers

os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
database = db.EZDB("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database", debug=False)
sys.path.pop(0)

Session = sa.orm.sessionmaker()

old_engine = sa.create_engine("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/old_rpg_database" + "?charset=utf8mb4", pool_recycle=3600)
# using the session.
old_meta = sa.MetaData(bind=old_engine)
old_meta.reflect()

old_session = Session(bind=old_engine)

# Should empty database of prebuilt user related objects.
# Hopefully not locations?
# Make sure quest_path_to_quest_association get clean up properly.
# I still need to reset the increment values of every table in the database.
database.session.query(db.User).delete()
database.update()
new_meta = sa.MetaData(bind=database.engine)
new_meta.reflect()
database.engine.execute("SET FOREIGN_KEY_CHECKS=0;")
for table in new_meta.tables:
    migration_helpers.reset_table_ids_and_autoincrement(table, database.engine)
database.engine.execute("SET FOREIGN_KEY_CHECKS=1;")


# Most important is to migrate the user!
# create a new user with data from old user.
def migrate_users():
    """Migrate the user data by creating new user accounts.

    NOTE: posts aren't migrated user by user but wholesale as they are unmodified.
    I haven't finished the hero migration part of the user migration yet.
    NOTE2: heroes are migrated separately as well.
    """
    old_user_table = old_meta.tables['user']
    for old_user in old_session.query(old_user_table).all():
        user = database.add_new_user(old_user.username, old_user.password, email=old_user.email)
        migration_helpers.set_all(old_user, user)
        # Not doing migrate_inbox(user, old_user) because it is being done
        # in the forum migration code.
    database.update()


def migrate_forum():
    """Migrate all the forum content in the game.

    After analysis of the Post table (then subsequent forum, board and thread tables)
    this should be cloned in wholesale rather than user by user.
    """

    db_execute_script("migrations/replace_forum_data_v1.sql", database)


def migrate_heroes():
    old_hero_table = old_meta.tables['hero']
    for old_hero in old_session.query(db.Hero).all():
        # don't add in the default users [user.username for user in db.prebuilt_objects.users]
        # I could also just drop the first 2 user objects?

        # should ignore prebuilt heroes ... not built
        user = database.get_object_by_id("User", old_hero.user_id)
        hero = database.add_new_hero_to_user(user)
        # pdb.set_trace()
        migration_helpers.set_all(old_session.query(old_hero_table).filter_by(id=old_hero.id).one(), hero)
        migrate_items(old_hero, hero)  # Currently mostly gives hero gold instead.
        migrate_abilities(old_hero, hero)
        migrate_attributes(old_hero, hero)
        migrate_skill(old_hero, hero, 'proficiency', hero_attrib='base_proficiencies')
        # Ignoring because no new data -> migrate_specializations(old_hero, hero)

    database.update()


def migrate_items(old_hero, hero):
    old_items_table = old_meta.tables['item']
    old_items = old_session.query(old_items_table).filter_by(inventory_id=old_hero.inventory.id).all()
    for old_item in old_items:
        template_item = database.session.query(db.Item).filter_by(name=old_item.name, template=True).first()
        if template_item:
            item = database.create_item(template_item.id)
            hero.inventory.add_item(item)
            migration_helpers.set_all(old_item, item, except_=['id'])
        else:
            # Give Player gold instead of migrating items. Lame :P
            hero.gold += old_item.buy_price
        database.session.commit()


def migrate_abilities(old_hero, hero):
    old_ability_table = old_meta.tables['ability']
    old_abilities = old_session.query(old_ability_table).filter_by(hero_id=old_hero.id).filter(old_ability_table.c.level > 0).all()
    for old_ability in old_abilities:
        try:
            hero.abilities[normalize_attrib_name(old_ability.name)].level = old_ability.level
        except KeyError:
            hero.basic_ability_points += old_ability.level
    database.session.commit()


def migrate_attributes(old_hero, hero):
    old_attrib_table = old_meta.tables['attribute']
    old_attribs = old_session.query(old_attrib_table).filter_by(hero_id=old_hero.id).filter(old_attrib_table.c.level > 1).all()
    for old_attrib in old_attribs:
        try:
            hero.attributes[normalize_attrib_name(old_attrib.name)].level = old_attrib.level
        except KeyError:
            hero.attribute_points += old_attrib.level - 1  # -1, Accommodate base level of 1.
    database.session.commit()


def migrate_skill(old_hero, hero, table_name, base=0, hero_attrib="", points_var=""):
    container_table = old_meta.tables[table_name]
    old_skills = old_session.query(container_table).filter_by(hero_id=old_hero.id).filter(container_table.c.level > base).all()

    for old_skill in old_skills:
        container = hero_attrib or table_name
        try:
            getattr(hero, container)[normalize_attrib_name(old_skill.type_)].level = old_skill.level
        except KeyError:
            # If points_var is passed use it.
            points_var = points_var or table_name + "_points"
            setattr(hero, points_var, getattr(hero, points_var) + old_skill.level - base)
    database.session.commit()


def migrate_specializations(old_hero, hero):
    pass


if __name__ == "__main__":
    migrate_users()
    migrate_forum()
    migrate_heroes()
    exit("It didn't crash!")

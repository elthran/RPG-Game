import os
import sys
import pdb

import sqlalchemy as sa
import sqlalchemy.orm

import models
import controller.setup_account
import controller.forum
import controller.questing
import services.time
import services.generators
import services.naming  # import normalize_attrib_name, normalize_class_name
import migrations.migration_helpers

# Make a new version of the current database each time.
# Each time I run the script it starts from the same point.
# This will help me to additively create a migration script.
# As in ... I add some code and run it and try and make my migration more
# and more complete.
os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
os.system('python3 -c "import models.database.populate_database as pd; pd.create_all(); pd.add_prebuilt_objects()"')


Session = sa.orm.sessionmaker()

# Connect to the old database (the one I'm migrating data from).
old_engine = sa.create_engine("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/old_rpg_database" + "?charset=utf8mb4", pool_recycle=3600)
# using the session.
old_meta = sa.MetaData(bind=old_engine)
old_meta.reflect()

old_session = Session(bind=old_engine)
old_table_query = migrations.migration_helpers.TableQuery(old_session, old_meta)

# Beginning of actual migration code!
print("Beginning actual migration.")


def migrate_users_to_account():
    """Migrate user data by creating new accounts from old data.

    If account already exists just clone in the old data.
    NOTE: id's may change but username remains the same!
    """
    for old_user in old_table_query('user').all():
        account = models.Account.filter_by(username=old_user.username).one_or_none()
        if account is None:
            account = controller.setup_account.add_new_account(old_user.username, old_user.password, email=old_user.email)
        migrations.migration_helpers.set_all(old_user, account, except_=('id',))
        # I don't need to migrate inbox or messages because there are none.
        # models.Base.quick_save()
        # migrate_inbox(account, old_user)
    models.Base.save()


# def migrate_inbox(account, old_user):
#     """Migrate each account's inbox."""
#     for old_inbox in old_session.query(old_meta.tables['inbox']).filter_by(user_id=old_user.id).all():
#         pass


def migrate_forum():
    """Migrate the forum and all related tables.

    Cascade Migrate: forum, board, thread, post.
    NOTE: I needed to migrate the User/Account tables first.
    """
    forum = models.Forum.first()
    migrate_boards(forum)


def migrate_boards(forum):
    """Migrate forum boards.

    Change title to name, set timestamp.
    NOTE: only migrate the boards for the passed forum.
    """
    for old_board in old_table_query('board').all():
        board = models.Board.filter_by(name=old_board.title).one_or_none()
        if board is None:
            board = controller.forum.create_board(forum, old_board.title)
            models.Base.session.add(board)
        board.timestamp = board.timestamp or services.time.now()
        models.Board.quick_save()
        migrate_threads(board, old_board)
    models.Base.save()


def migrate_threads(board, old_board):
    """Migrate all threads.

    Pass in migrated board to send data to correctly.
    NOTE: only migrate the threads for the passed board.
    """
    # with magic methods: for old_thread in old_board.thread:
    for old_thread in old_table_query('thread').filter_by(board_id=old_board.id).all():
        thread = controller.forum.create_thread(board, old_thread.title, old_thread.description, old_thread.creator)
        models.Base.quick_save()
        migrate_posts(thread, old_thread)


def migrate_posts(thread, old_thread):
    """Migrate all posts.

    Note: I need to query in the correct Account data.
    NOTE: only migrate the posts for the passed thread.
    """
    for old_post in old_table_query('post').filter_by(thread_id=old_thread.id).all():
        # With magic methods: old_post.user
        old_user = old_table_query('user').filter_by(id=old_post.user_id).one()
        account = models.Account.filter_by(username=old_user.username).one()
        post = controller.forum.create_post(thread, old_post.content, account)
        migrations.migration_helpers.set_all(old_post, post, except_=('id', 'thread_id', 'user_id', 'content'))
        models.Base.quick_save()


def migrate_heroes():
    """Migrate hero data.

    This will probably have to be a cascade as well.
    """
    for old_hero in old_table_query('hero').all():
        old_user = old_table_query('user').filter_by(id=old_hero.user_id).one()
        account = models.Account.filter_by(username=old_user.username).one()
        hero = models.Hero.filter_by(name=old_hero.name).one_or_none()
        if hero is None:
            hero = controller.setup_account.add_new_hero_to_account(account)
            models.Base.session.add(hero)
        migrations.migration_helpers.set_all(old_hero, hero, except_=('id', 'user_id'))
        models.Base.quick_save()
        migrate_items(old_hero, hero)
        migrate_skill(old_hero, hero, 'ability', base=0, hero_attrib='abilities', points_var='basic_ability_points')
        migrate_skill(old_hero, hero, 'attribute', base=1, hero_attrib='attributes')
        migrate_skill(old_hero, hero, 'proficiency', hero_attrib='base_proficiencies')
        # Not bothering to migrate specializations as nobody has any.
        migrate_achievements(old_hero, hero)
        migrate_quest_paths(old_hero, hero)


def migrate_items(old_hero, hero):
    """Migrate items from old hero's inventory.

    Give gold if item has been removed from the game.
    """

    old_inventory = old_table_query.join_to_hero(old_hero, 'inventory')

    for old_item in old_table_query('item').filter_by(inventory_id=old_inventory.id).all():
        template_item = models.Item.filter_by(name=old_item.name, template=True).one_or_none()
        if template_item is not None:
            item = services.generators.create_item(template_item.id)
            hero.inventory.add_item(item)
            migrations.migration_helpers.set_all(old_item, item, except_=['id', 'inventory_id'])
        else:
            # Give Player gold instead of migrating items. Lame :P
            hero.gold += old_item.buy_price
        models.Base.quick_save()


def migrate_skill(old_hero, hero, table_name, base=0, hero_attrib="", points_var=""):
    """Very generic method for migrating any skill class.

    This can be used to migrate abilities, attributes or proficiencies ...
    possibly even specializations.
    """
    container_table = old_meta.tables[table_name]
    old_skills = old_session.query(container_table).filter_by(hero_id=old_hero.id).filter(container_table.c.level > base).all()

    for old_skill in old_skills:
        container = hero_attrib or table_name
        try:
            try:
                getattr(hero, container)[services.naming.normalize_attrib_name(old_skill.type_)].level = old_skill.level

            # All my tables except 'ability' use 'type_', it uses 'type'.
            # I modified the latest ability table so now it should use 'type_'.
            # I should be able to remove this try in the next migration.
            except AttributeError:
                getattr(hero, container)[services.naming.normalize_attrib_name(old_skill.type)].level = old_skill.level
        except KeyError:
            # If points_var is passed use it.
            points_var = points_var or table_name + "_points"
            setattr(hero, points_var, getattr(hero, points_var) + old_skill.level - base)
    models.Base.quick_save()


def migrate_achievements(old_hero, hero):
    """Migrate hero achievements.

    Accommodates change of achievements.current_dungeon_floor_progress -> achievements.current_floor_progress
    """

    old_journal = old_table_query.join_to_hero(old_hero, 'journal')
    for old_achievements in old_table_query('achievements').filter_by(journal_id=old_journal.id).all():
        migrations.migration_helpers.set_all(old_achievements, hero.journal.achievements, except_=('id', 'journal_id'))
        hero.journal.achievements.current_floor_progress = old_achievements.current_dungeon_floor_progress
    models.Base.quick_save()


def migrate_quest_paths(old_hero, hero):
    old_journal = old_table_query.join_to_hero(old_hero, 'journal')
    for old_quest_path in old_table_query('quest_path').filter_by(journal_id=old_journal.id).all():
        controller.questing.add_quest_path_to_hero(hero, old_quest_path.name)
    models.Base.quick_save()


if __name__ == "__main__":
    migrate_users_to_account()
    migrate_forum()
    migrate_heroes()
    exit("It didn't crash!")

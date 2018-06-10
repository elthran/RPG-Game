import os
import sys
import pdb
import inspect

import sqlalchemy as sa
import sqlalchemy.orm

# Patch the import path to 1 directory above this one.
old_path = os.path.dirname(__file__).split(os.sep)
new_path = os.sep.join(old_path[:-1])
# -1 refers to how many levels of directory to go up
sys.path.insert(0, new_path)

# Make a new version of the current database each time.
# Each time I run the script it starts from the same point.
# This will help me to additively create a migration script.
# As in ... I add some code and run it and try and make my migration more
# and more complete.
os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
os.system('python3 -c "import models.database.populate_database as pd; pd.create_all(); pd.add_prebuilt_objects()"')

import models
import controller.setup_account
import controller.forum
import services.time
# from services.naming import normalize_attrib_name, normalize_class_name
# from rpg_game_tests.test_helpers import db_execute_script
import migrations.migration_helpers
sys.path.pop(0)

Session = sa.orm.sessionmaker()

# Connect to the old database (the one I'm migrating data from).
old_engine = sa.create_engine("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/old_rpg_database" + "?charset=utf8mb4", pool_recycle=3600)
# using the session.
old_meta = sa.MetaData(bind=old_engine)
old_meta.reflect()

old_session = Session(bind=old_engine)


# Beginning of actual migration code!
print("Beginning actual migration.")


def migrate_users_to_account():
    """Migrate user data by creating new accounts from old data.

    If account already exists just clone in the old data.
    NOTE: id's may change but username remains the same!
    """
    old_user_table = old_meta.tables['user']
    for old_user in old_session.query(old_user_table).all():
        account = models.Account.filter_by(username=old_user.username).one_or_none()
        if account is None:
            account = controller.setup_account.add_new_account(old_user.username, old_user.password, email=old_user.email)
        migrations.migration_helpers.set_all(old_user, account, except_=('id',))
    models.Base.save()


def migrate_forum():
    """Migrate the forum and all related tables.

    Cascade Migrate: forum, board, thread, post.
    NOTE: I needed to migrate the User/Account tables first.
    """
    forum = models.Forum.first()
    migrate_boards(forum)


def migrate_boards(old_forum):
    """Migrate forum boards.

    Change title to name, set timestamp.
    NOTE: only migrate the boards for the passed forum.
    """
    for old_board in old_session.query(old_meta.tables['board']).filter_by(forum_id=old_forum.id).all():
        board = models.Board.filter_by(name=old_board.title).one_or_none()
        if board is None:
            board = controller.forum.create_board(old_forum, old_board.title)
        board.timestamp = board.timestamp or services.time.now()
        models.Board.quick_save()
        migrate_threads(board)
    models.Base.save()


def migrate_threads(old_board):
    """Migrate all threads.

    Pass in migrated board to send data to correctly.
    NOTE: only migrate the threads for the passed board.
    """
    for old_thread in old_session.query(old_meta.tables['thread']).filter_by(board_id=old_board.id).all():
        thread = controller.forum.create_thread(old_board, old_thread.title, old_thread.description, old_thread.creator)
        models.Base.quick_save()
        migrate_posts(thread)


def migrate_posts(old_thread):
    """Migrate all posts.

    Note: I need to query in the correct Account data.
    NOTE: only migrate the posts for the passed thread.
    """
    for old_post in old_session.query(old_meta.tables['post']).filter_by(thread_id=old_thread.id).all():
        old_user = old_session.query(old_meta.tables['user']).filter_by(id=old_post.user_id).one()
        account = models.Account.filter_by(username=old_user.username).one()
        post = controller.forum.create_post(old_thread, old_post.content, account)
        migrations.migration_helpers.set_all(old_post, post, except_=('id', 'thread_id', 'user_id', 'content'))
        models.Base.quick_save()


def migrate_heroes():
    pass


if __name__ == "__main__":
    migrate_users_to_account()
    migrate_forum()
    # migrate_heroes()
    exit("It didn't crash!")

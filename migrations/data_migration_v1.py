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
from build_code import normalize_class_name
sys.path.pop(0)

Session = sa.orm.sessionmaker()

old_engine = sa.create_engine("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/old_rpg_database" + "?charset=utf8mb4", pool_recycle=3600)
# using the session.
old_meta = sa.MetaData(bind=old_engine)
old_meta.reflect()

old_session = Session(bind=old_engine)

database = db.EZDB("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database", debug=False)


# Most important is to migrate the user!
# create a new user with data from old user.
def migrate_users():
    old_user_table = old_meta['user']
    for old_user in old_session.query(old_user_table).all():
        # don't add in the default users [user.username for user in db.prebuilt_objects.users]
        # I could also just drop the first 2 user objects?
        if old_user.username not in [user.username for user in database.get_all_users()]:
            user = database.add_new_user(old_user.username, old_user.password, email=old_user.email_address)
            user.timestamp = old_user.timstamp
            user.prestige = old_user.prestige
            user.is_admin = old_user.is_admin
            migrate_inbox(user, old_user)
            migrate_posts(user, old_user)

            database.add_new_hero_to_user(user)
    """
    # upgrade
    op.add_column('inbox', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_inbox_user_id_user'), 'inbox', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('fk_post_user_id_user', 'post', type_='foreignkey')
    op.create_foreign_key(op.f('fk_post_thread_id_thread'), 'post', 'thread', ['thread_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(op.f('fk_post_user_id_user'), 'post', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('user', sa.Column('reset_key', sa.Unicode(length=200), nullable=True))
    op.drop_constraint('fk_user_inbox_id_inbox', 'user', type_='foreignkey')
    op.drop_column('user', 'inbox_id')
    
    # downgrade
    op.add_column('user', sa.Column('inbox_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_user_inbox_id_inbox', 'user', 'inbox', ['inbox_id'], ['id'])
    op.drop_column('user', 'reset_key')
    op.drop_constraint(op.f('fk_post_user_id_user'), 'post', type_='foreignkey')
    op.drop_constraint(op.f('fk_post_thread_id_thread'), 'post', type_='foreignkey')
    op.create_foreign_key('fk_post_user_id_user', 'post', 'user', ['user_id'], ['id'])
    op.drop_constraint(op.f('fk_inbox_user_id_user'), 'inbox', type_='foreignkey')
    op.drop_column('inbox', 'user_id')
    """


def migrate_inbox(user, old_user):
    pass


def migrate_posts(user, old_user):
    pass


if __name__ == "__main__":
    migrate_users()
    exit("It didn't crash!")

# # generic one.
# # pdb.set_trace()
# # Iterate through all the table objects in the old database's schema.
# for name, table in old_meta.tables.items():
#     # Get class name from table name for dummy object creation.
#     cls_name = normalize_class_name(name)
#     # Return each row in each table. (all the data in the database one row at a time).
#     for old_obj in old_session.query(table).all():
#         try:
#             obj = db.get_object_by_id(cls_name, old_obj.id)
#         except IndexError:
#             obj = None
#             # Need to create a new object as there isn't one to overwrite.
#             # These objects should have been all imported into the database module.
#             try:
#                 Class = getattr(database, cls_name)
#             except KeyError:
#                 Class = None
#                 print("'{}' class not found in database module. Import it there.".format(cls_name))
#             # Make a new dummy object that is then going to be replaced with new fields.
#             # Get the signature of the objects constructor. This will allow me
#             # to create a new object using default arguments.
#             if Class:
#                 sig = inspect.signature(Class)
#                 # Get some appropriately typed values for the constructor signature.
#                 # Should return a list of arguments to pass to the dummy class
#                 # constructor.
#                 args = [getattr(old_obj, key) if key in old_obj else sig.parameters[key].default if sig.parameters[key].default != sig.empty else None for key in sig.parameters.keys() if key != 'kwargs']
#                 print(args)
#                 try:
#                     obj = Class(*args)
#                 except:
#                     pdb.set_trace()
#                 db.session.add(obj)
#         except KeyError:
#             obj = None
#             print("'{}' class not found in database module. Import it there.".format(cls_name))
#         except AttributeError:
#             # This is some kind of association object.
#             # I haven't worked out how to clone the variables safely.
#             # If I could query the new objects by row id?
#             obj = None
#             print(old_obj)
#             if name in ("adjacent_location", "quest_path_to_quest"):
#                 continue  # ignore the tables listed above.
#             pdb.set_trace()
#         # Update dummy object with migrated data.
#         if obj:
#             for key in old_obj.keys():
#                 value = getattr(old_obj, key)
#                 if key == 'polymorphic_identity':
#                     pdb.set_trace()
#                 try:
#                     setattr(obj, key, value)
#                 except AttributeError:
#                     print("'{}' has no attribute '{}'".format(cls_name, key))
#             db.update()


# user_table = old_meta.tables['user']
# for old_obj in old_session.query(user_table).all():
#     try:
#         obj = db.get_object_by_id("User", old_obj.id)
#     except IndexError:
#         obj = None
#         # get default args ....
#         # pass them to constructor
#         # This should create a new dummy object which should have the appropriate default arguments.
#         try:
#             Class = getattr(database, "User")
#         except KeyError:
#             Class = None
#             print("User object not found")
#         # pdb.set_trace()
#         # Make a new dummy object that is then going to be replaced with new fields.
#         # Get the signature of the objects constructor
#         if Class:
#             sig = inspect.signature(Class)
#             # Get some appropriately typed values for the constructor signature.
#             args = (getattr(old_obj, key) for key in sig.parameters.keys())
#             obj = Class(*args)
#             db.session.add(obj)
#     # pdb.set_trace()
#     # Update dummy object with migrated data.
#     if obj:
#         for key in old_obj.keys():
#             try:
#                 setattr(obj, key, getattr(old_obj, key))
#             except KeyError:
#                 pass
#         db.update()

# ability_table = old_meta.tables['hero']
#
# AbilitiesTemp = type("AbilitiesTemp", (), {})
# sa.orm.mapper(AbilitiesTemp, abilities_table)
# Temp = type('Temp', (object,), {})
# sa.orm.mapper(Temp, ability_table)
#
#     ability_query = session.query(ability_table).all()
#
#     for obj in ability_query:
#         abilities_id = getattr(obj, "abilities_id")
#         if abilities_id:
#             abilities_obj = session.query(AbilitiesTemp).get(abilities_id)  # Allows get with temp object.
#             obj = session.query(Temp).get(obj.id)  # get modifiable version of object.
#             setattr(obj, 'hero_id', abilities_obj.hero_id)
#             # print(abilities_id, abilities_obj.id, abilities_obj.hero_id, obj.hero_id)
#             session.commit()
#     exit()

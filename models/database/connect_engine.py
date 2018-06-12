import socket

import sqlalchemy as sa

import private_config

# Check location of code whether server or local
if 'liveweb' not in socket.gethostname():  # Running on local machine.
    database_url = private_config.LOCAL_DATABASE_URL
else:  # Running on server
    database_url = private_config.SERVER_DATABASE_URL


# def __init__(self, database="sqlite:///:memory:", debug=True,
#                  testing=False):
#         """Create a basic SQLAlchemy engine and session.
#
#         Attribute "file_name" is used to find location of database for python.
#
#         Hidden method: _delete_database is for testing and does what it
#         sounds like it does :).
#         """

debug = False
testing = True
first_run = False
server = database_url[0:database_url.rindex('/')]
name = database_url.split('/').pop()


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
engine = sa.create_engine(database_url + "?charset=utf8mb4", pool_recycle=3600, echo=debug)

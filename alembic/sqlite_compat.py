from functools import wraps

# Import all the SQLAlchemy junk.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

# Import alembic basics
from alembic import op, context
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table

import pdb

# Set up basic sqlalchemy classes.
Session = sessionmaker()
Base = declarative_base()


def session_scope(f):
    """Provide a transactional scope around a series of operations."""

    @wraps(f)
    def wrap_session_scope(*args, **kwargs):
        self = args[0]
        self.session = Session(bind=self.engine)
        retval = f(*args, **kwargs)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return retval

    return wrap_session_scope


class SQLiteCompat:
    def __init__(self):
        # create engine and reflect all tables
        url = context.config.get_main_option("sqlalchemy.url")
        self.engine = create_engine(url)
        self.metadata = MetaData(bind=self.engine)
        # raise "gets here"
        # op.create_table(
        #     'forum',
        #     sa.Column('id', sa.Integer, primary_key=True),
        # )  # For testing
        self.metadata.reflect(self.engine)
        self.session = Session(bind=self.engine)

    def copy_schema(self, source, dest, without_columns=[], force=False):
        """Copy the schema from an existing table to a new one.

        Deletes table if it exists (requires force).
        Creates new table at end.
        """
        # Start from a clean slate.
        if self.metadata.tables[dest] is not None and force:
            op.drop_table(dest)
        elif self.metadata.tables[dest] is not None and not force:
            raise Exception("You are trying to delete an existing table (the '{}' table). If you meant to do that set the force parameter to force=True".format(dest))

        # get old table metadata
        source_table = self.metadata.tables[source]

        # create new table
        dest_table = Table(dest, self.metadata)

        # copy schema and create temp_table from source_table
        for column in source_table.columns:
            if column.name not in without_columns:
                dest_table.append_column(column.copy())

        # Create a Table from the cloned Metadata.
        dest_table.create()

        return dest_table

    @session_scope
    def clone_data(self, source_table, dest_table):
        """Copy the data from one table to another.

        This is the actual row data. The schema must already exist.
        If it doesn't use the 'copy_schema' method.
        """
        # Create all dummy classes and  mappers.
        class Temp(object):
            pass

        mapper(Temp, dest_table)

        for source in self.session.query(source_table):
            temp_object = Temp()
            for name in dest_table.columns.keys():
                setattr(temp_object, name, getattr(source, name))
            self.session.add(temp_object)

        return Temp

    def drop_column(self, table_name, column_name):
        """Replicate op.drop_column('forum', 'title') in SQLite!

        Use table reflection hopefully this will work?
        """

        # Consider using a more complex error checking and name
        # choosing for temp table
        temporary_table_name = 'temp'
        source_table = self.metadata.tables[table_name]
        temp_table = self.copy_schema(table_name, temporary_table_name,
                                      force=True)
        self.clone_data(source_table, temp_table)

        # Then immediately recreate it without the offending 'title' column.
        # All that work just to replicate
        # op.drop_column('forum', 'title') in SQLite!
        temp_table = self.metadata.tables[temporary_table_name]  # For testing ...

        dest_table = self.copy_schema(temporary_table_name, table_name,
                                      without_columns=[column_name], force=True)
        self.clone_data(temp_table, dest_table)

        # # Finally drop the Temp table
        op.drop_table('temp')

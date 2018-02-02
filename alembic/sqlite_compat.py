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


class SQLiteCompat:
    def __init__(self):
        # create engine and reflect all tables
        url = context.config.get_main_option("sqlalchemy.url")
        self.engine = create_engine(url)
        self.metadata = MetaData(bind=self.engine)
        self.metadata.reflect(self.engine)
        self.session = Session(bind=self.engine)

    def copy_schema(self, source, dest, without_columns=[]):
        """Copy the schema from an existing table to a new one.

        This does't create the new table.
        """
        # get old table metadata
        source_table = self.metadata.tables[source]

        # create new table
        dest_table = Table(dest, self.metadata)

        # copy schema and create temp_table from source_table
        for column in source_table.columns:
            if column.name not in without_columns:
                dest_table.append_column(column.copy())
        return dest_table

    def drop_column(self, table_name, column_name):
        """Replicate op.drop_column('forum', 'title') in SQLite!

        Use table reflection hopefully this will work?
        """
        #Start from a clean slate.
        op.drop_table('temp')

        source_table = self.metadata.tables[table_name]
        temp_table = self.copy_schema(table_name, 'temp')
        print(temp_table.columns)
        # exit("Testing temptable columns.")
        temp_table.create()

        # Create all dummy classes and  mappers.
        class SourceTable(object):
            pass

        class Temp(object):
            pass

        mapper(Temp, temp_table)
        mapper(SourceTable, source_table)

        for source in self.session.query(SourceTable):
            temp_object = Temp()
            for name in temp_table.columns.keys():
                setattr(temp_object, name, getattr(source, name))
            self.session.add(temp_object)
            self.session.commit()

        # exit("Testing object data from query after mapper thing ...")

        # Drop the now cloned table.
        # op.drop_table(table_name)

        # Then immediately recreate it without the offending 'title' column.
        # All that work just to replicate
        # op.drop_column('forum', 'title') in SQLite!
        # op.create_table(
        #     'forum',
        #     sa.Column('id', sa.Integer, primary_key=True),
        # )

        # Now clone the data back from the Temp table to the Forum table.
        # forums = (Forum(id=temp.id) for temp in session.query(Temp))
        # session.add_all(forums)
        # session.commit()
        #
        # # Finally drop the Temp table
        # op.drop_table('temp')

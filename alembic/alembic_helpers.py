"""
Calls to add extra feature to Alembic.
Feature that maybe oneday will be. Or that I will offer to the project

author: Marlen
"""
import pdb
from pprint import pprint
import warnings


# class Temp(object):
#     pass


class AlembicHelper:
    def __init__(self, op, sa, **kwargs):
        """Pull in the current alembic context."""

        self.op = op
        self.sa = sa
        bind = op.get_bind()
        self.insp = sa.inspect(bind)
        # self.metadata = sa.MetaData()
        # self.metadata.reflect(bind)

        # The order of this might matter. It should go at the end.
        self.Session = sa.orm.sessionmaker(bind=bind)
        self.bind = bind
        # Add in any args that seem like a good idea.
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def move_foreign_key_column(self, source_table_name, dest_table_name,
                                source_col_name=None, dest_col_name=None):
        """Move foreign key from one side of a relationship to another.

        Great if you built your database wrong and need to fix it.
        """
        op = self.op
        sa = self.sa
        bind = self.bind
        meta = sa.MetaData()
        session = self.Session()

        source_col_name = source_col_name or dest_table_name + "_id"
        dest_col_name = dest_col_name or source_table_name + "_id"

        try:
            op.add_column(
                dest_table_name,
                sa.Column(dest_col_name, sa.Integer,
                          sa.ForeignKey(source_table_name + ".id"))
            )
        except sa.exc.OperationalError as ex:
            if "Duplicate column name" in str(ex):
                warnings.warn("Overwriting table '{}' column '{}'".format(
                    dest_table_name, dest_col_name))
        # Reload metadata after adding column? I think that is probably it.
        meta.reflect(bind=bind)

        # Use the metadata.
        source_table = meta.tables[source_table_name]
        dest_table = meta.tables[dest_table_name]

        source_objs = session.query(source_table).all()

        Temp = type('Temp', (object,), {})
        sa.orm.mapper(Temp, dest_table)

        for obj in source_objs:
            fkey_id = getattr(obj, source_col_name)
            dest_obj = session.query(Temp).get(fkey_id)
            setattr(dest_obj, dest_col_name, obj.id)
            session.commit()
        session.close()
        self.drop_foreign_key_constraint(source_col_name, source_table_name)
        op.drop_column(source_table_name, source_col_name)

    def drop_foreign_key_constraint(self, column_name, table_name):
        """Drop a foreign key constraint if it exists.

        And can be found given the table name.
        """
        op = self.op

        fkeys = self.insp.get_foreign_keys(table_name)
        constraint_name = AlembicHelper.get_constraint_name(fkeys, column_name)

        if constraint_name:
            op.drop_constraint(constraint_name, table_name, type_='foreignkey')
        else:
            raise Exception("The table '{}' with column '{}' has no "
                            "associated foreign key constraint.".format(
                table_name, column_name))

    @staticmethod
    def get_constraint_name(fkeys, column_name):
        """Get the name the first constraint given a column name.

        fkeys is a list of dictionaries produced by
        inspector.get_foreign_keys(table_name) or some such similar construct.

        NOTE: Maybe only works with Foreign Keys?"""
        for fk in fkeys:
            if column_name in fk['constrained_columns']:
                return fk['name']

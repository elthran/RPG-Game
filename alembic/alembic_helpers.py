"""
Calls to add extra feature to Alembic.
Feature that maybe oneday will be. Or that I will offer to the project

author: Marlen
"""
import pdb
from pprint import pprint


class AlembicHelper:
    def __init__(self, op, sa, **kwargs):
        """Pull in the current alembic context."""

        self.op = op
        bind = op.get_bind()
        self.insp = sa.inspect(bind)

        # Add in any args that seem like a good idea.
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def drop_constraint(self, column_name, table_name, type_=None,
                        schema=None):
        if type_ != 'foreignkey' or schema is not None:
            raise Exception("That hasn't been implemented yet! "
                            "Feel free to do so.")

        elif type_ == 'foreignkey':
            fkeys = self.insp.get_foreign_keys(table_name)
            constraint_name = AlembicHelper.get_constraint_name(
                fkeys, column_name)

            if constraint_name:
                self.op.drop_constraint(constraint_name, table_name,
                                        type_='foreignkey', schema=schema)
                self.op.drop_column(table_name, column_name)
            else:
                raise Exception("The column_name '{}' has no associated "
                                "foreign key constraint.".format(column_name))

    @staticmethod
    def get_constraint_name(fkeys, column_name):
        """Maybe only works with Foreign Keys?"""
        for fk in fkeys:
            if column_name in fk['constrained_columns']:
                return fk['name']

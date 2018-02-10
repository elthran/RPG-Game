"""Fix cascading deletes

Revision ID: 7c0ce008d107
Revises: 9eedd032389a
Create Date: 2018-02-10 10:25:00.493367

If error:
sqlalchemy.exc.OperationalError: (_mysql_exceptions.OperationalError) (1054, "Unknown column 'inventory.hero_id' in 'field list'") [SQL: 'SELECT inventory.id AS inventory_id, inventory.hero_id AS inventory_hero_id \nFROM inventory \nWHERE %s = inventory.hero_id'] [parameters: (1,)]
"""
import os
import sys
import pdb
from pprint import pprint

from alembic import op
import sqlalchemy as sa

# Get the name of the current directory for this file and split it.
old_path = os.path.dirname(os.path.abspath(__file__)).split('\\')
new_path = '\\'.join(old_path[:-1])
# -1 refers to how many levels of directory to go up
# In this case add a new path at 'alembic' directory.
sys.path.insert(0, new_path)
from alembic_helpers import AlembicHelper
sys.path.pop(0)  # Then remove this path to be tidy.

# revision identifiers, used by Alembic.
revision = '7c0ce008d107'
down_revision = '9eedd032389a'
branch_labels = None
depends_on = None

bind = op.get_bind()  # bind is engine.
metadata = sa.MetaData(bind=bind)
metadata.reflect(bind)
Session = sa.orm.sessionmaker(bind=bind)
ah = AlembicHelper(op, sa)


def upgrade():
    op.add_column(
        "inventory",
        sa.Column("hero_id", sa.Integer, sa.ForeignKey('hero.id'))
    )

    session = Session()

    hero_table = metadata.tables['hero']
    inv_table = metadata.tables['inventory']
    heroes = session.query(hero_table).all()

    class Temp(object):
        pass

    sa.orm.mapper(Temp, inv_table)

    for hero in heroes:
        inventory = session.query(Temp).get(hero.inventory_id)
        inventory.hero_id = hero.id
        session.commit()

    pdb.set_trace()
    ah.drop_constraint("inventory_id", "hero", type_='foreignkey')


def downgrade():
    session = Session()

    # ah.
    op.drop_column("inventory", "hero_id")
    exit("This is just a test so stop revising!")

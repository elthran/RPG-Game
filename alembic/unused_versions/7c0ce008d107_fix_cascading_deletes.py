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
old_path = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
new_path = os.sep.join(old_path[:-1])
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
    ah.move_foreign_key_column('hero', 'inventory')
    ah.move_foreign_key_column('hero', 'specialization_container',
                               "specializations_id", "hero_id")
    ah.move_foreign_key_column('specialization_container', 'specialization',
                               'archetype_id', 'archetype_id')
    ah.move_foreign_key_column('specialization_container', 'specialization',
                               'calling_id', 'calling_id')
    ah.move_foreign_key_column('hero', 'attributes')
    ah.move_foreign_key_column('hero', 'proficiencies')
    ah.move_foreign_key_column('hero', 'journal')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'agility_id', 'agility_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'brawn_id', 'brawn_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'charisma_id', 'charisma_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'divinity_id', 'divinity_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'fortuity_id', 'fortuity_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'intellect_id', 'intellect_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'pathfinding_id', 'pathfinding_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'quickness_id', 'quickness_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'resilience_id', 'resilience_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'survivalism_id', 'survivalism_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'vitality_id', 'vitality_id')
    ah.move_foreign_key_column('attributes', 'attribute',
                               'willpower_id', 'willpower_id')


def downgrade():
    ah.move_foreign_key_column('inventory', 'hero')
    ah.move_foreign_key_column('specialization_container', 'hero',
                               "hero_id", "specializations_id")
    ah.move_foreign_key_column('specialization', 'specialization_container',
                               'archetype_id', 'archetype_id')
    ah.move_foreign_key_column('specialization', 'specialization_container',
                               'calling_id', 'calling_id')
    ah.move_foreign_key_column('attributes', 'hero')
    ah.move_foreign_key_column('proficiencies', 'hero')
    ah.move_foreign_key_column('journal', 'hero')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'agility_id', 'agility_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'brawn_id', 'brawn_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'charisma_id', 'charisma_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'divinity_id', 'divinity_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'fortuity_id', 'fortuity_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'intellect_id', 'intellect_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'pathfinding_id', 'pathfinding_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'quickness_id', 'quickness_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'resilience_id', 'resilience_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'survivalism_id', 'survivalism_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'vitality_id', 'vitality_id')
    ah.move_foreign_key_column('attribute', 'attributes',
                               'willpower_id', 'willpower_id')

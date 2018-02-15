"""Update database with new inventory/item table columns

Revision ID: e7aa53d2cb57
Revises: 
Create Date: 2018-02-09 13:10:24.233977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7aa53d2cb57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column(
            'item',
            sa.Column('inventory_id', sa.Integer, sa.ForeignKey(
                'inventory.id', ondelete="SET NULL"))
        )
    except sa.exc.OperationalError as ex:
        if "Duplicate column name 'inventory_id'" not in str(ex):
            raise


def downgrade():
    op.drop_column('item', 'inventory_id')

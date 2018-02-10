"""Add item equipped column.

Revision ID: 9eedd032389a
Revises: e7aa53d2cb57
Create Date: 2018-02-09 13:16:36.349211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eedd032389a'
down_revision = 'e7aa53d2cb57'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'item',
        sa.Column('equipped', sa.Boolean)
    )


def downgrade():
    op.drop_column('item', 'equipped')

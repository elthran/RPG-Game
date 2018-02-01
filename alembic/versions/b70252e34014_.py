"""Add new 'title' column to 'forum' table.

Also first revision, yay!

Revision ID: b70252e34014
Revises: 
Create Date: 2018-01-31 20:48:18.530044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70252e34014'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('forum', sa.Column('title', sa.String))


def downgrade():
    op.drop_column('forum', 'title')

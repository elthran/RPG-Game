"""Use SQLiteCompat module to drop a column.

Also first revision, yay!

IMPORTANT!!
Fancy method to drop a column when using SQLite.
Yes, it it super long and stupidly complex.
All it does is replicate:
op.drop_column('forum', 'title')

Revision ID: b70252e34014
Revises: 
Create Date: 2018-01-31 20:48:18.530044

"""
from alembic import op
import sqlalchemy as sa

import sys
import os

# Get the name of the current directory for this file and split it.
old_path = os.path.dirname(os.path.abspath(__file__)).split('\\')
new_path = '\\'.join(old_path[:-1])
# -1 refers to how many levels of directory to go up
sys.path.insert(0, new_path)
from sqlite_compat import SQLiteCompat
sys.path.pop(0)


# revision identifiers, used by Alembic.
revision = 'b70252e34014'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('forum', sa.Column('title', sa.String))


def downgrade():
    compat = SQLiteCompat()
    compat.drop_column('forum', 'title')

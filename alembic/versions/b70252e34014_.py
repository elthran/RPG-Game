"""Add new 'title' column to 'forum' table.

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


# revision identifiers, used by Alembic.
revision = 'b70252e34014'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('forum', sa.Column('title', sa.String))


def downgrade():
    # Import all the SQLAlchemy junk.
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    # Set up basic sqlalchemy classes.
    Session = sessionmaker()
    Base = declarative_base()

    # Set up classes with just the columns you need to interact with.
    class Temp(Base):
        __tablename__ = 'temp'

        id = sa.Column(sa.Integer, primary_key=True)

    class Forum(Base):
        __tablename__ = 'forum'

        id = sa.Column(sa.Integer, primary_key=True)

    # Use the sqlalchemy and alembic vars to set up a basic session.
    bind = op.get_bind()
    session = Session(bind=bind)

    # Create your temp table (buy keep a handle to the object)
    # If I just used op.create_table .. I wouldn't have a handle to the
    # Temp object.
    Temp.__table__.create(bind)

    # Make a bunch of new Temp objects with any relavant data from the Forum
    # object. In this case only the id is saved.
    temps = (Temp(id=forum.id) for forum in session.query(Forum))
    session.add_all(temps)
    session.commit()

    # Drop the now cloned Forum table.
    op.drop_table('forum')
    # Then immediately recreate it without the offending 'title' column.
    # All that work just to replicate
    # op.drop_column('forum', 'title') in SQLite!
    op.create_table(
        'forum',
        sa.Column('id', sa.Integer, primary_key=True),
    )

    # Now clone the data back from the Temp table to the Forum table.
    forums = (Forum(id=temp.id) for temp in session.query(Temp))
    session.add_all(forums)
    session.commit()

    # Finally drop the Temp table
    op.drop_table('temp')

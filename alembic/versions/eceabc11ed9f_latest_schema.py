"""Latest Schema

Revision ID: eceabc11ed9f
Revises: 
Create Date: 2018-06-10 09:45:20.032964

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eceabc11ed9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.Unicode(length=200), nullable=False),
    sa.Column('email', sa.Unicode(length=200), nullable=True),
    sa.Column('reset_key', sa.Unicode(length=200), nullable=True),
    sa.Column('reset_timeout', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('inbox_alert', sa.Boolean(), nullable=True),
    sa.Column('prestige', sa.Integer(), nullable=True),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.Column('signature', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_account')),
    sa.UniqueConstraint('username', name=op.f('uq_account_username'))
    )
    op.create_table('chat_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chat_log'))
    )
    op.create_table('np_c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('race', sa.String(length=50), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_np_c')),
    sa.UniqueConstraint('name', name=op.f('uq_np_c_name'))
    )
    op.create_table('point',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name=op.f('fk_point_location_id_location'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_point'))
    )
    op.create_table('chat_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_name', sa.String(length=50), nullable=True),
    sa.Column('message', sa.String(length=200), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('chat_log_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_log_id'], ['chat_log.id'], name=op.f('fk_chat_message_chat_log_id_chat_log')),
    sa.ForeignKeyConstraint(['sender_id'], ['hero.id'], name=op.f('fk_chat_message_sender_id_hero')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chat_message'))
    )
    op.create_table('hero_specialization_access',
    sa.Column('hero_id', sa.Integer(), nullable=False),
    sa.Column('specialization_id', sa.Integer(), nullable=False),
    sa.Column('hidden', sa.Boolean(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['hero_id'], ['hero.id'], name=op.f('fk_hero_specialization_access_hero_id_hero'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['specialization_id'], ['specialization.id'], name=op.f('fk_hero_specialization_access_specialization_id_specialization')),
    sa.PrimaryKeyConstraint('hero_id', 'specialization_id', name=op.f('pk_hero_specialization_access'))
    )
    op.create_table('journal_to_location',
    sa.Column('journal_id', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['journal_id'], ['journal.id'], name=op.f('fk_journal_to_location_journal_id_journal'), ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name=op.f('fk_journal_to_location_location_id_location'), ondelete='SET NULL')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('has_enemy', sa.Boolean(), nullable=True),
    sa.Column('hero_id', sa.Integer(), nullable=True),
    sa.Column('chat_log_id', sa.Integer(), nullable=True),
    sa.Column('random_encounter_monster_id', sa.Integer(), nullable=True),
    sa.Column('discovered_item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_log_id'], ['chat_log.id'], name=op.f('fk_game_chat_log_id_chat_log')),
    sa.ForeignKeyConstraint(['discovered_item_id'], ['item.id'], name=op.f('fk_game_discovered_item_id_item')),
    sa.ForeignKeyConstraint(['hero_id'], ['hero.id'], name=op.f('fk_game_hero_id_hero')),
    sa.ForeignKeyConstraint(['random_encounter_monster_id'], ['hero.id'], name=op.f('fk_game_random_encounter_monster_id_hero')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_game'))
    )
    op.drop_index('uq_user_username', table_name='user')
    op.drop_table('user')
    op.drop_table('monster_template')
    op.add_column('achievements', sa.Column('current_floor_progress', sa.Integer(), nullable=True))
    op.drop_column('achievements', 'current_dungeon_floor_progress')
    op.add_column('board', sa.Column('name', sa.String(length=50), nullable=True))
    op.add_column('board', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.drop_column('board', 'title')
    op.add_column('forum', sa.Column('name', sa.String(length=50), nullable=True))
    op.drop_column('forum', 'title')
    op.add_column('hero', sa.Column('account_id', sa.Integer(), nullable=True))
    op.add_column('hero', sa.Column('cave', sa.Boolean(), nullable=True))
    op.add_column('hero', sa.Column('city', sa.Boolean(), nullable=True))
    op.add_column('hero', sa.Column('forest', sa.Boolean(), nullable=True))
    op.add_column('hero', sa.Column('is_monster', sa.Boolean(), nullable=True))
    op.add_column('hero', sa.Column('maximum_level', sa.Integer(), nullable=True))
    op.add_column('hero', sa.Column('species', sa.String(length=50), nullable=True))
    op.add_column('hero', sa.Column('species_plural', sa.String(length=50), nullable=True))
    op.add_column('hero', sa.Column('template', sa.Boolean(), nullable=True))
    op.drop_constraint('fk_hero_user_id_user', 'hero', type_='foreignkey')
    op.create_foreign_key(op.f('fk_hero_account_id_account'), 'hero', 'account', ['account_id'], ['id'], ondelete='CASCADE')
    op.drop_column('hero', 'user_id')
    op.drop_column('hero', 'random_encounter_monster')
    op.add_column('inbox', sa.Column('account_id', sa.Integer(), nullable=True))
    op.drop_constraint('fk_inbox_user_id_user', 'inbox', type_='foreignkey')
    op.create_foreign_key(op.f('fk_inbox_account_id_account'), 'inbox', 'account', ['account_id'], ['id'], ondelete='CASCADE')
    op.drop_column('inbox', 'user_id')
    op.add_column('item', sa.Column('damage_type', sa.String(length=50), nullable=True))
    op.add_column('post', sa.Column('account_id', sa.Integer(), nullable=True))
    op.drop_constraint('fk_post_user_id_user', 'post', type_='foreignkey')
    op.create_foreign_key(op.f('fk_post_account_id_account'), 'post', 'account', ['account_id'], ['id'], ondelete='CASCADE')
    op.drop_column('post', 'user_id')
    op.add_column('proficiency', sa.Column('display_chunk', sa.String(length=200), nullable=True))
    op.add_column('specialization', sa.Column('hidden', sa.Boolean(), nullable=True))
    op.add_column('thread', sa.Column('name', sa.String(length=50), nullable=True))
    op.add_column('thread', sa.Column('views', sa.Integer(), nullable=True))
    op.drop_column('thread', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('thread', sa.Column('title', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True))
    op.drop_column('thread', 'views')
    op.drop_column('thread', 'name')
    op.drop_column('specialization', 'hidden')
    op.drop_column('proficiency', 'display_chunk')
    op.add_column('post', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk_post_account_id_account'), 'post', type_='foreignkey')
    op.create_foreign_key('fk_post_user_id_user', 'post', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('post', 'account_id')
    op.drop_column('item', 'damage_type')
    op.add_column('inbox', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk_inbox_account_id_account'), 'inbox', type_='foreignkey')
    op.create_foreign_key('fk_inbox_user_id_user', 'inbox', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('inbox', 'account_id')
    op.add_column('hero', sa.Column('random_encounter_monster', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('hero', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk_hero_account_id_account'), 'hero', type_='foreignkey')
    op.create_foreign_key('fk_hero_user_id_user', 'hero', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('hero', 'template')
    op.drop_column('hero', 'species_plural')
    op.drop_column('hero', 'species')
    op.drop_column('hero', 'maximum_level')
    op.drop_column('hero', 'is_monster')
    op.drop_column('hero', 'forest')
    op.drop_column('hero', 'city')
    op.drop_column('hero', 'cave')
    op.drop_column('hero', 'account_id')
    op.add_column('forum', sa.Column('title', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True))
    op.drop_column('forum', 'name')
    op.add_column('board', sa.Column('title', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True))
    op.drop_column('board', 'timestamp')
    op.drop_column('board', 'name')
    op.add_column('achievements', sa.Column('current_dungeon_floor_progress', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('achievements', 'current_floor_progress')
    op.create_table('monster_template',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True),
    sa.Column('species', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True),
    sa.Column('species_plural', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=True),
    sa.Column('level_min', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('level_max', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('experience_rewarded', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('city', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('forest', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('cave', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('level_modifier', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('agility', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('charisma', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('divinity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('resilience', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('fortuity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('pathfinding', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('quickness', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('willpower', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('brawn', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('survivalism', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('vitality', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('intellect', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('username', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=False),
    sa.Column('password', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=200), nullable=False),
    sa.Column('email', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=200), nullable=True),
    sa.Column('reset_key', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=200), nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), nullable=True),
    sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('inbox_alert', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('prestige', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('uq_user_username', 'user', ['username'], unique=True)
    op.drop_table('game')
    op.drop_table('journal_to_location')
    op.drop_table('hero_specialization_access')
    op.drop_table('chat_message')
    op.drop_table('point')
    op.drop_table('np_c')
    op.drop_table('chat_log')
    op.drop_table('account')
    # ### end Alembic commands ###

# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
# Author: Elthran B, Jimmy Zhang                                              #
# Email : jimmy.gnahz@gmail.com                                               #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

"""Objects used in the database and the game.

Suggestion: change name to game_objects.py
"""
import pdb

import sqlalchemy as sa
import sqlalchemy.orm

import models


class Game(models.Base):
    has_enemy = sa.Column(sa.Boolean)

    # Relationships
    # game to hero is one to one
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id'))
    hero = sa.orm.relationship("Hero", back_populates='game', foreign_keys="[Game.hero_id]")

    chat_log_id = sa.Column(sa.Integer, sa.ForeignKey('chat_log.id'))
    chat_log = sa.orm.relationship("ChatLog", back_populates="games")

    random_encounter_monster_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id'))
    random_encounter_monster = sa.orm.relationship("Hero", foreign_keys="[Game.random_encounter_monster_id]")

    @sa.orm.validates("random_encounter_monster")
    def validate_random_encounter_monster(self, key, value):
        if value and value.is_monster is False:
            raise Exception("Can only assign monsters to random_encounter_monster.")
        elif value and value.template is True:
            raise Exception("Can only assign a real monster not a template one.")
        else:
            return value

    def __init__(self, hero=None):
        self.hero = hero
        self.has_enemy = False

        # Use first ChatLog object or create it if it doesn't exits.
        # This could in theory be used to add custom player to player chat?
        self.chat_log = models.ChatLog.get(1)
        if not self.chat_log:
            self.chat_log = models.ChatLog()

        self.random_encounter_monster = None

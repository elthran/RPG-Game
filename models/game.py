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
    hero = sa.orm.relationship("Hero", back_populates='game')

    chat_log_id = sa.Column(sa.Integer, sa.ForeignKey('chat_log.id'))
    chat_log = sa.orm.relationship("ChatLog", back_populates="games")

    def __init__(self, hero=None):
        self.hero = hero
        self.has_enemy = False
        self.chat_log = models.ChatLog.get(1)
        if not self.chat_log:
            self.chat_log = models.ChatLog()

import sqlalchemy as sa
import sqlalchemy.orm

import models

models.Hero.game_id = sa.Column(sa.Integer, sa.ForeignKey('game.id', ondelete="CASCADE"))
models.Hero.game = sa.orm.relationship("Game", back_populates='hero', cascade="all, delete-orphan", single_parent=True)

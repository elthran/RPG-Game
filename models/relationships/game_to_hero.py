import sqlalchemy as sa
import sqlalchemy.orm

import models

models.Game.hero = sa.orm.relationship("Hero", uselist=True, back_populates='game', cascade="all, delete-orphan")

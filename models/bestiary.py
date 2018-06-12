# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
#  Author: Elthran B, Jimmy Zhang                                             #
#  Email : jimmy.gnahz@gmail.com                                              #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#
import sqlalchemy as sa
import sqlalchemy.orm

import models


class NPC(models.Base):
    name = sa.Column(sa.String(50), unique=True, nullable=False)
    race = sa.Column(sa.String(50))
    age = sa.Column(sa.Integer)

    def __init__(self, name, race="Humanoid", age=45):
        self.name = name
        self.race = race
        self.age = age


import sqlalchemy as sa
import sqlalchemy.orm

import models


# Messing with nodes
class Point(models.Base):
    __tablename__ = 'point'

    id = sa.Column(sa.Integer, primary_key=True)
    x = sa.Column(sa.Integer)
    y = sa.Column(sa.Integer)

    location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id', ondelete="CASCADE"))
    location = sa.orm.relationship('Location', back_populates='point')

    def __init__(self, x, y):
        """Create a point object.

        Object has both x and y coordinates which define a location from
        the origin at the TOP LEFT = (0, 0) corner of the map.

        I'd prefer BOTTOM LEFT == (0,0) but I'll go with what is here.
        """
        self.x = x  # How far away from the left edge of the map
        self.y = y  # How far away from the top edge of the map

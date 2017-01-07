"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

This is just a testbed to develop new saveable objects for the database.
"""

try:
    from game import Base
    
    from sqlalchemy import Column, Integer, String

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")

from game import Hero
        
class PrimaryAttributeList(Base):
    __tablename__ = "primary_attributes"
    
    id = Column(Integer, primary_key=True)
    agility = Column(Integer, default=1)
    charisma = Column(Integer, default=1)
    divinity = Column(Integer, default=1)
    fortitude = Column(Integer, default=1)
    fortuity = Column(Integer, default=1)
    perception = Column(Integer, default=1)
    reflexes = Column(Integer, default=1)
    resilience = Column(Integer, default=1)
    strength = Column(Integer, default=1)
    survivalism = Column(Integer, default=1)
    vitality = Column(Integer, default=1)
    wisdom = Column(Integer, default=1)
    
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship("Hero", back_populates='primary_attributes')
    
    def __repr__(self): 
        atts = []
        for key in self.__table__.columns.keys():
            atts.append('{}={}'.format(key, getattr(self, key)))
        
        data = "<PrimaryAttribute(" + ', '.join(atts) + ')>'
        return data        
    
if __name__ == "__main__":

    """
    """
    # pa = PrimaryAttribute()
    # print(pa)
    
    
    
    

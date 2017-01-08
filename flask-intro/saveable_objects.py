"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

This is just a testbed to develop new saveable objects for the database.
"""

try:
    from sqlalchemy.ext.declarative import declarative_base
    #Initialize SQLAlchemy base class.
    Base = declarative_base()
    #What this actually means or does I have no idea but it is neccessary. And I know how to use it.
        
    from sqlalchemy import Table, Column, Integer, String

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")

# from abilities import Ability
# from items import Item

# heroes_ablities_association_table = Table('heroes_ablities_association', Base.metadata,
    # Column('heroes_id', Integer, ForeignKey('heroes.id')),
    # Column('abilities_id', Integer, ForeignKey('abilities.id'))
# )
    
# class AllAbilitiesTable(Base, Ability):
    # __tablename__ = "all_ablities_table"
    
    # heroes = relationship("Hero", secondary=heroes_ablities_association_table, back_populates="abilities")

# class AllItemsTable(Base, Item):
    # __tablename__ = "all_items_table"
    
    # heroes = relationship("Hero", secondary=heroes_ablities_association_table, back_populates="abilities")
    
    
if __name__ == "__main__":

    """
    """
    # pa = PrimaryAttribute()
    # print(pa)
    
    
    
    

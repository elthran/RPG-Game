"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

This is just a testbed to develop new saveable objects for the database.
"""

try:
    from game import Base
    
    from sqlalchemy import Table, Column, Integer, String

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")
           
    
if __name__ == "__main__":

    """
    """
    # pa = PrimaryAttribute()
    # print(pa)
    
    
    
    

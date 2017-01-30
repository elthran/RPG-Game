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
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e
    
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
    
    
class BaseListElement(Base):
    """Stores list objects in database.
    
    To implement:
    1. add line in this class: parent_table_name_id = Column(Integer, ForeignKey('parent_table_name.id'))
    2. add line in foreign class: _my_list = relationship("BaseListElement")
    3. add method to foreign class:
    @hybrid_property
    def my_list(self):
        '''Return a list of elements.
        '''
        return [element.value for element in self._my_list]

    4. add method to foreign class:
    @my_list.setter
    def my_list(self, values):
        '''Create list of BaseListElement objects.
        '''
        self._my_list = [BaseListElement(value) for value in values]
    
    See Location class for example implementation.
    5. Probably a better way using decorators ...?
    """
    __tablename__ = "base_list"
    id = Column(Integer, primary_key=True)
    int_value = Column(Integer)
    str_value = Column(String)    
    
    dict_id = Column(Integer, ForeignKey('base_dict.id'))
    
    def __init__(self, value):
        """Build BaseListElement from value.
        """
        self.value = value
    
    
    @hybrid_property
    def value(self):
        """Return value of list element.
        
        Can be string or integer.
        """
        return self.int_value or self.str_value


    @value.setter
    def value(self, value):
        """Assign value to appropriate column.
        
        Currently implements the strings and integers.
        """
        if type(value) is type(str()):
            self.str_value = value
        elif type(value) is type(int()):
            self.int_value = value
        else:
            raise "TypeError: BaseListElement does not accept type '{}':".format(type(value))
            
    def __str__(self):
        """Return pretty string version of data.
        """
        return repr(self.value)
            

class BaseDict(Base):
    __tablename__ = "base_dict"
    id = Column(Integer, primary_key=True)
    keys = relationship("BaseListElement")
    values = relationship("BaseListElement")
    
    
    def __init__(self, dictionary={}):
        self.items = {}
        index = 0
        for x in dictionary.keys():
            self.keys.append(BaseListElement(x))
            self.values.append(BaseListElement(dictionary[x]))
            self.items[x] = index
            index += 1
            
    def __getitem__(self, key):
        index = self.items[key]
        return self.values[index].value
        
    def __setitem__(self, key, item):
        """Change value at key or create key with value.
        """
        try:
            index = self.items[key]
            self.values.pop(index)
            self.values.insert(index, BaseListElement(item))
        except KeyError as ex:
            self.add(key, item)
            
    def add(self, key, item):
        """Add an element to the end of the dictionary.
        
        """
        index = len(self.keys)
        self.keys.append(BaseListElement(key))
        self.values.append(BaseListElement(item))
        self.items[key] = index
        
        
    def items(self):
        return ((self.keys[index].value, self.values[index].value) for index in range(len(self.keys)))
                    
    
    def __str__(self):
        """Return pretty string version of data.
        """
        
        return "{" + ', '.join(['{}: {}'.format(self.keys[x], self.values[x]) for x in range(len(self.keys))]) + "}"
    

   
    
    
    
    

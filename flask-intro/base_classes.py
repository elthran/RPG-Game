"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

This class is imported first and can be used to add generic methods to all database objects.
Like a __str__ function that I can actually read.
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
from sqlalchemy import orm

import inspect
import pdb

#I didn't call this method __str__ as it would then overide the module string function.
def string_of(self): 
    """Return string data about a Database object.
    
    Note: prints lists as list of ids.
    Note2: key.lstrip('_') accesses _attributes as attributes due to my convention of using 
    _value, @hybrid_property of value, @value.setter.
    
    I don't understand why I need all of these ... only that each one seems to hold
    slightly different data than the others with some overlap.
    
    Not3: super class variables like 'type' and 'name' don't exist in WorldMap until they are
    referenced as they are declared in Map...? I called super to fix this ... but it may
    only allow ONE level of superclassing. Multi-level superclasses will probably fail.
    """

    data = set(vars(self).keys()) | \
        set(self.__table__.columns.keys()) | \
        set(self.__mapper__.relationships.keys())
        
    try:
        data |= set(vars(super(type(self), self)).keys())
        data |= set(super(type(self), self).__table__.columns.keys())
        data |= set(super(type(self), self).__mapper__.relationships.keys())
    except AttributeError:
        #If super is Base.
        pass
        
    data.discard('_sa_instance_state')
        
    atts = []
    for key in sorted(data):
        key = key.lstrip('_')
        value = getattr(self, key)
        # pdb.set_trace()
        if value and type(value) == orm.collections.InstrumentedList:
            value = '[' + ', '.join(e.__class__.__name__ + '.id=' + str(e.id) for e in value) + ']'
        elif value:
            try:
                value._sa_instance_state #Dummy call to test if value is a Database object.
                value = str(value)
            except AttributeError:
                pass #The object is not a databse object.
        atts.append('{}={}'.format(key, repr(value)))

    return "<{}({})>".format(self.__class__.__name__, ', '.join(atts))
        
Base.__str__ = string_of

#For testing.
def pprint(self):
    """Multi-line print of a database object -> good for object diff.
    
    Basically a string_of clone but one variable per line.
    """
    data = set(vars(self).keys()) | \
        set(self.__table__.columns.keys()) | \
        set(self.__mapper__.relationships.keys())
        
    try:
        data |= set(vars(super(type(self), self)).keys())
        data |= set(super(type(self), self).__table__.columns.keys())
        data |= set(super(type(self), self).__mapper__.relationships.keys())
    except AttributeError:
        #If super is Base.
        pass
        
    data.discard('_sa_instance_state')
    
    print("\n\n<{}(".format(self.__class__.__name__))
    for key in sorted(data):
        key = key.lstrip('_')
        value = getattr(self, key)
        # pdb.set_trace()
        if value and type(value) == orm.collections.InstrumentedList:
            value = '[' + ', '.join(e.__class__.__name__ + '.id=' + str(e.id) for e in value) + ']'
        elif value:
            try:
                value._sa_instance_state #Dummy call to test if value is a Database object.
                value = str(value)
            except AttributeError:
                pass #The object is not a databse object.
            
        print('{}={}'.format(key, repr(value)))
    print(")>\n")
        
Base.pprint = pprint

def get_all_atts(self):
    # inspect.getmro(self) #get all supers ... get all vars from this list?
    # print(inspect.getmro(self))
    data = set(vars(self).keys()) | \
        set(self.__table__.columns.keys()) | \
        set(self.__mapper__.relationships.keys())
        
    try:
        data |= set(vars(super(type(self), self)).keys())
        data |= set(super(type(self), self).__table__.columns.keys())
        data |= set(super(type(self), self).__mapper__.relationships.keys())
    except AttributeError:
        #If super is Base.
        pass
        
    data.discard('_sa_instance_state')
    return data

def is_equal(self, other):
    """Test if two database objects are equal.
    
    hero.is_equal(hero) vs. str(hero) == str(hero)
    is_equal is 0.3 seconds faster over 1000 iterations than str == str.
    So is_equal is not that useful. I would like it if it was 5-10 times faster.
    """
    data = get_all_atts(self)
    other_data = get_all_atts(other)
    
    if not data == other_data:
        return False   
    
    if not self.__class__.__name__ == other.__class__.__name__:
        return False
        
    for key in sorted(data):
        key = key.lstrip('_')
        value = getattr(self, key)
        other_value = getattr(other, key)
                
        #Add recursion in here :P        
        # pdb.set_trace()
        if value and type(value) == orm.collections.InstrumentedList:
            value = '[' + ', '.join(e.__class__.__name__ + '.id=' + str(e.id) for e in value) + ']'
            other_value = '[' + ', '.join(e.__class__.__name__ + '.id=' + str(e.id) for e in value) + ']'
        elif value:
            try:
                value._sa_instance_state #Dummy call to test if value is a Database object.
                value = str(value)
                other_value = str(other_value)
            except AttributeError:
                pass #The object is not a databse object.
            
        if not value == other_value:
            return False
    return True
    
Base.is_equal = is_equal
    
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
    
    dict_id_keys = Column(Integer, ForeignKey('base_dict.id'))
    dict_id_values = Column(Integer, ForeignKey('base_dict.id'))
    
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
            

class BaseItem(Base):
    __tablename__ = 'base_item'
    id = Column(Integer, primary_key=True)
    str_key = Column(String)
    int_key = Column(Integer)
    str_value = Column(String)
    int_value = Column(Integer)
    
    base_dict_id = Column(Integer, ForeignKey('base_dict.id'))
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    @hybrid_property
    def key(self):
        """Return key of appropriate type.
        
        Can be string or integer.
        """
        return self.int_key or self.str_key


    @key.setter
    def key(self, key):
        """Assign key to appropriate typed column.
        
        Currently implements strings and integers.
        """
        if type(key) is type(str()):
            self.str_key = key
        elif type(key) is type(int()):
            self.int_key = key
        else:
            raise "TypeError: BaseItem does not accept type '{}':".format(type(key))

    @hybrid_property
    def value(self):
        """Return value of appropriate type.
        
        Can be string or integer.
        """
        return self.int_value or self.str_value


    @value.setter
    def value(self, value):
        """Assign value to appropriate typed column.
        
        Currently implements strings and integers.
        """
        if type(value) is type(str()):
            self.str_value = value
        elif type(value) is type(int()):
            self.int_value = value
        else:
            raise "TypeError: BaseItem does not accept type '{}':".format(type(value))
    

class BaseDict(Base):
    """Mimic a dictionary but be storable in a database.
    
    
    """
    __tablename__ = "base_dict"
    id = Column(Integer, primary_key=True)
    
    base_items = relationship("BaseItem")
    
    def __init__(self, d={}):
        """Build a list of items and a matching dictionary.
        
        The dictionary should act as a hash table/index for the list.
        """
        self.d_items = {}
        for key in d:
            self.d_items[key] = BaseItem(key, d[key])
            self.base_items.append(self.d_items[key])
            assert self.d_items[key] is self.base_items[-1]
 
             
    @orm.reconstructor
    def rebuild_d_items(self):
        self.d_items = {}
        for item in self.base_items:
            self.d_items[item.key] = item
        
    
    def remove(self, key):
        base_item = self.d_items.pop(key, None)
        if base_item:
            self.base_items.remove(base_item)
            
            
    def __getitem__(self, key):
        """Get value of key using a dict key name or list index.
        """

        return self.d_items[key].value
            
            
    def __setitem__(self, key, value):
        """Change value at key or create key with value.
        """
        try:
            self.d_items[key].value = value
        except KeyError as ex:
            self.add(key, value)
            
    def add(self, key, value):
        """Add an element to the end of the dictionary.
        
        """
        self.d_items[key] = BaseItem(key, value)
        self.base_items.append(self.d_items[key])
    
    def keys(self):
        return (item.key for item in self.base_items)
    
    def values(self):
        return (item.value for item in self.base_items)
        
    def items(self):
        return ((item.key, item.value) for item in self.base_items)
        
    # def __iter__(self):
        # return (key for key in self.d_items)
        
    def __str__(self):
        """Return pretty string version of data.
        
        """
        
        data = ', '.join(['{}: {}'.format(repr(item.key), repr(item.value))
            for item in self.base_items])
        return "BaseDict{" + data + "}"
 





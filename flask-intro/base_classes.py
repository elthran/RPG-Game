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
            

class BaseDict(Base):
    __tablename__ = "base_dict"
    id = Column(Integer, primary_key=True)
    keys = relationship("BaseListElement", foreign_keys="[BaseListElement.dict_id_keys]")
    values = relationship("BaseListElement", foreign_keys="[BaseListElement.dict_id_values]")
    
    
    def __init__(self, dictionary={}):
        self.d_items = {}
        index = 0
        for x in dictionary.keys():
            self.keys.append(BaseListElement(x))
            self.values.append(BaseListElement(dictionary[x]))
            self.d_items[x] = index
            index += 1
            
    @orm.reconstructor
    def rebuild_d_items(self):
        # import pdb; pdb.set_trace()
        self.d_items = {}
        for index in range(len(self.keys)):
            key = self.keys[index].value
            self.d_items[key] = index
        
            
    def __getitem__(self, key):
        """Get value of key using a dict key name or list index.
        """
        index = self.d_items[key]
        return self.values[index].value
            
            
    def __setitem__(self, key, item):
        """Change value at key or create key with value.
        """
        try:
            index = self.d_items[key]
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
        self.d_items[key] = index
        
        
    def items(self):
        return ((self.keys[index].value, self.values[index].value) for index in range(len(self.keys)))
        
    def __iter__(self):
        return (key for key in self.d_items)
        
    
    # def __eq__(self, other): 
        # return self.__dict__ == other.__dict__
                    
    
    def __str__(self):
        """Return pretty string version of data.
        
        NOTE: due to sorting this is quite slow.
        """
        
        return "{" + ', '.join(sorted(['{}: {}'.format(self.keys[x], self.values[x]) for x in range(len(self.keys))])) + "}"
    

   
    
    
    
    

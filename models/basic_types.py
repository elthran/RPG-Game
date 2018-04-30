# from models import Base


# class BaseListElement(Base):
#     """Stores list objects in database.
#
#     To implement:
#     1. add line in this class:
#         parent_table_name_id = Column(Integer,
#             ForeignKey('parent_table_name.id'))
#     2. add line in foreign class: _my_list = relationship("BaseListElement")
#     3. add method to foreign class:
#     @hybrid_property
#     def my_list(self):
#         '''Return a list of elements.
#         '''
#         return [element.value for element in self._my_list]
#
#     4. add method to foreign class:
#     @my_list.setter
#     def my_list(self, values):
#         '''Create list of BaseListElement objects.
#         '''
#         self._my_list = [BaseListElement(value) for value in values]
#
#     See Location class for example implementation.
#     5. Probably a better way using decorators ...?
#     """
#     __tablename__ = "base_list"
#     id = Column(Integer, primary_key=True)
#     int_value = Column(Integer)
#     str_value = Column(String(50))
#
#     # dict_id_keys = Column(Integer, ForeignKey('base_dict.id',
#     #                                           ondelete="CASCADE"))
#     # dict_id_values = Column(Integer, ForeignKey('base_dict.id',
#     #                                             ondelete="CASCADE"))
#
#     def __init__(self, value):
#         """Build BaseListElement from value.
#         """
#         self.value = value
#
#     @hybrid_property
#     def value(self):
#         """Return value of list element.
#
#         Can be string or integer.
#         """
#         return self.int_value or self.str_value
#
#     @value.setter
#     def value(self, value):
#         """Assign value to appropriate column.
#
#         Currently implements the strings and integers.
#         """
#         if isinstance(value, str):
#             self.str_value = value
#         elif isinstance(value, int):
#             self.int_value = value
#         else:
#             raise "TypeError: BaseListElement does not accept " \
#                 "type '{}':".format(type(value))
#
#     def __str__(self):
#         """Return pretty string version of data.
#         """
#         return repr(self.value)
#
#
# class BaseItem(Base):
#     __tablename__ = 'base_item'
#     id = Column(Integer, primary_key=True)
#     str_key = Column(String(50))
#     int_key = Column(Integer)
#     str_value = Column(String(50))
#     int_value = Column(Integer)
#
#     base_dict_id = Column(Integer, ForeignKey('base_dict.id',
#                                               ondelete="CASCADE"))
#     def __init__(self, key, value):
#         self.key = key
#         self.value = value
#
#     @hybrid_property
#     def key(self):
#         """Return key of appropriate type.
#
#         Can be string or integer.
#         """
#         return self.int_key or self.str_key
#
#
#     @key.setter
#     def key(self, key):
#         """Assign key to appropriate typed column.
#
#         Currently implements strings and integers.
#         """
#         if type(key) is type(str()):
#             self.str_key = key
#         elif type(key) is type(int()):
#             self.int_key = key
#         else:
#             raise "TypeError: BaseItem does not accept type '{}':".format(type(key))
#
#     @hybrid_property
#     def value(self):
#         """Return value of appropriate type.
#
#         Can be string or integer.
#         """
#         return self.int_value or self.str_value
#
#
#     @value.setter
#     def value(self, value):
#         """Assign value to appropriate typed column.
#
#         Currently implements strings and integers.
#         """
#         if type(value) is type(str()):
#             self.str_value = value
#         elif type(value) is type(int()):
#             self.int_value = value
#         else:
#             raise "TypeError: BaseItem does not accept type '{}':".format(type(value))
#
#
# class BaseDict(Base):
#     """Mimic a dictionary but be storable in a database.
#
#
#     """
#     __tablename__ = "base_dict"
#     id = Column(Integer, primary_key=True)
#
#     base_items = relationship("BaseItem", cascade="all, delete-orphan")
#
#     def __init__(self, d={}):
#         """Build a list of items and a matching dictionary.
#
#         The dictionary should act as a hash table/index for the list.
#         """
#         self.d_items = {}
#         for key in d:
#             self.d_items[key] = BaseItem(key, d[key])
#             self.base_items.append(self.d_items[key])
#             assert self.d_items[key] is self.base_items[-1]
#
#
#     @orm.reconstructor
#     def rebuild_d_items(self):
#         self.d_items = {}
#         for item in self.base_items:
#             self.d_items[item.key] = item
#
#
#     def remove(self, key):
#         base_item = self.d_items.pop(key, None)
#         if base_item:
#             self.base_items.remove(base_item)
#
#
#     def __getitem__(self, key):
#         """Get value of key using a dict key name or list index.
#         """
#
#         return self.d_items[key].value
#
#
#     def __setitem__(self, key, value):
#         """Change value at key or create key with value.
#         """
#         try:
#             self.d_items[key].value = value
#         except KeyError as ex:
#             self.add(key, value)
#
#     def add(self, key, value):
#         """Add an element to the end of the dictionary.
#
#         """
#         self.d_items[key] = BaseItem(key, value)
#         self.base_items.append(self.d_items[key])
#
#     def keys(self):
#         return (item.key for item in self.base_items)
#
#     def values(self):
#         return (item.value for item in self.base_items)
#
#     def items(self):
#         return ((item.key, item.value) for item in self.base_items)
#
#     # def __iter__(self):
#         # return (key for key in self.d_items)
#
#     def __str__(self):
#         """Return pretty string version of data.
#
#         """
#
#         data = ', '.join(['{}: {}'.format(repr(item.key), repr(item.value))
#             for item in self.base_items])
#         return "BaseDict{" + data + "}"
#
#
# class Map(dict):
#     """
#     Example:
#     m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
#
#     Should allow a dictionary to behave like an object.
#     So you can do either ->
#     map['some_key']
#     OR
#     map.some_key
#
#     NOTE: the iterator function is not normal for dictionaries.
#     It returns .values() (ordered) not .keys() (random)
#     """
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for arg in args:
#             if isinstance(arg, dict):
#                 for k, v in arg.items():
#                     self[k] = v
#
#         if kwargs:
#             for k, v in kwargs.items():
#                 self[k] = v
#
#         self.sorted_keys = sorted(self.keys())
#
#     def __getattr__(self, attr):
#         return self.get(attr)
#
#     def __setattr__(self, key, value):
#         self.__setitem__(key, value)
#
#     def __setitem__(self, key, value):
#         super(Map, self).__setitem__(key, value)
#         self.__dict__.update({key: value})
#
#     def __delattr__(self, item):
#         self.__delitem__(item)
#
#     def __delitem__(self, key):
#         super(Map, self).__delitem__(key)
#         del self.__dict__[key]
#
#     def __iter__(self):
#         """Return all the values (sorted by key) of this Map as an iterator.
#
#         Overrides default of returning .keys() (unsorted).
#         Now returns .values() (sorted by .keys())
#         """
#         if self.sorted_keys:
#             # pdb.set_trace()
#             return (self[key] for key in self.sorted_keys)
#         self.sorted_keys = sorted(self.keys())
#         return (self[key] for key in self.sorted_keys)

import functools
import operator

import sqlalchemy as sa
import sqlalchemy.orm.collections


def attribute_mapped_dict_hybrid(key):
    """A dictionary-based collection type with attribute-based keying.

    See http://docs.sqlalchemy.org/en/latest/orm/collections.html#sqlalchemy.orm.collections.attribute_mapped_collection
    Returns a MappedCollection factory with a keying based on the ‘attr_name’
    attribute of entities in the collection, where attr_name is the string
    name of the attribute.

    The key value must be immutable for the lifetime of the object.
    You can not, for example, map on foreign key values if those key values
    will change during the session, i.e. from None to a database-assigned
    integer after a session flush.

    As far as I can see ... this shouldn't work at all. Clearly it does.
    Wish I understood how.
    """
    return lambda: DictHybrid(key_attr=key)


class DictHybrid(sa.orm.collections.MappedCollection):
    """A Python object that acts like a JS one.

    You can assign values via attribute or via key.
    e.g.
        obj.foo = obj['foo'] all but really special keys :P

    The attribute_mapped_dict_hybrid
    allows me to build a factory for this class similar to
    sqlalchemy.orm.collections.attribute_mapped_collection(attr_name)

    Defaults to keying on object 'type'.
    """

    invalid_keys = {'__emulates__', 'id', 'keyfunc', '_sa_adapter'}

    def __init__(self, *args, key_attr='type', **kwargs):
        """Create a new DictHybrid with keying on 'type'.

        This is mostly cloned code I don't understand. I hope it doesn't
        break. I have a test suite so if it does break I should be able
        to come up with a solid fix.

        You can create a new internal dict by passing in a dict
        or by by passing tuples of key, value pairs.
        """
        super().__init__(operator.attrgetter(key_attr))
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    @sa.orm.collections.collection.internally_instrumented
    def __setitem__(self, key, value, _sa_initiator=None):
        """Instrumented version of dict setitem.

        I don't know how this works."""
        # noinspection PyArgumentList
        super().__setitem__(key, value, _sa_initiator)

    @sa.orm.collections.collection.internally_instrumented
    def __delitem__(self, key, _sa_initiator=None):
        """Instrumented version of dict delitem.

        I don't know how this works."""
        # noinspection PyArgumentList
        super().__delitem__(key, _sa_initiator)

    def __getattr__(self, attr):
        """Overloaded getattr method with custom handling.

        Any attribute that isn't in {'__emulates__', 'id', 'keyfunc'}
        gets called as a key to the dictionary.

        I'm not sure why these aren't ... how it works though is:

        self.id ... returns self.id like a normal object.
        self.some_key ... returns self[some_key] as though self was a dict.
        """
        if attr not in self.invalid_keys:
            return self[attr]
        return self.get(attr)

    @sa.orm.collections.collection.internally_instrumented
    def __setattr__(self, key, _sa_initiator=None):
        """Overloaded and Instrumented setattr method with custom handling.

        Any attribute that isn't in {'keyfunc', '_sa_adapter'}
        gets added as a key to the dictionary.

        I'm not sure why these aren't ... how it works though is:

        self.keyfunc = somefunc ... sets self.keyfunc like a normal object.
        self.some_key ... sets self[some_key] as though self was a dict.
        """
        if key not in self.invalid_keys:
            self.__setitem__(key, _sa_initiator)
        super().__setattr__(key, _sa_initiator)

    def __delattr__(self, item):
        """Makes object delatter act like dict delitem.

        del self.some_key ... does del self[some_key]
        as though self was a dict.
        """
        self.__delitem__(item)

    def sorted_keys(self):
        """Returns the the dictionary keys of self as a sorted frozenset.

        It is frozen so it can be used in a cache function.
        I don't really know how this works ... but it should allow repeated
        calls to sorted_keys to be very fast.
        """
        keys = self._key_sort(frozenset(self.keys()))
        return (x for x in sorted(keys))

    @staticmethod
    @functools.lru_cache(maxsize=16)
    def _key_sort(keys):
        """Cached sort method.

        Cache uses frozenset so it should be order independent?
        """
        return sorted(keys)

    def __iter__(self):
        """Return all the values (sorted by keys) of this dict as an iterator.

        If you want the normal dict method for __iter__ do:
        self.keys() instead. This will return unsorted keys.
        """

        return (self[key] for key in self.sorted_keys())

    def sorted_items(self):
        """Return the keys and values sorted by keys."""
        return ((k, self[k]) for k in self.sorted_keys())

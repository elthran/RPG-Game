"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at:
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

This class is imported first and can be used to add generic methods to all
database objects. Like a __str__ function that I can actually read.
"""

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.orderinglist
import sqlalchemy.orm.collections
import sqlalchemy.ext.declarative

import services
from . import database


class Base(object):
    def get_mro_till_base(self):
        """Return the MRO until you hit base."""

    def get_mro_keys(self):
        """Return all attributes of objects in MRO

        All non-base objects in inheritance path.
        Remove <class 'sqlalchemy.ext.declarative.api.Base'>,
        <class 'object'> as these are the last two objects in the MRO
        """
        hierarchy_keys = set()

        hierarchy = type(self).__mro__
        max_index = hierarchy.index(Base)
        hierarchy = hierarchy[1:max_index]

        for obj in hierarchy:
            if "Mixin" in obj.__name__:
                hierarchy_keys |= set(vars(obj).keys())
            else:
                hierarchy_keys |= set(vars(obj).keys()) \
                              - set(obj.__mapper__.relationships.keys())

        # Remove private variables and id keys to prevent weird recursion
        # and redundancy.
        hierarchy_keys -= set(
            [key for key in hierarchy_keys if key.startswith('_')]
        )  # ? or 'id' in key])

        return hierarchy_keys

    def get_all_atts(self):
        if self.__class__ == Base:
            return set()
        # noinspection PyUnresolvedReferences
        data = set(vars(self).keys()) | \
            set(self.__table__.columns.keys()) | \
            set(self.__mapper__.relationships.keys())

        data.discard('_sa_instance_state')

        hierarchy_keys = set()
        try:
            hierarchy_keys = self.get_mro_keys()
        except IndexError:
            pass  # This is the Base class and has no useful MRO.

        data |= hierarchy_keys

        # Remove special hoisted variable that I add in Mixin.
        # I don't know why it even exits in the MRO.
        data.discard('session')

        # Remove weird SQLAlchemy var available to higher class but no
        # lower ones.
        keys_to_remove = set()
        for key in data:
            try:
                getattr(self, key)
            except AttributeError:
                # Because of single table inheritance ... invalid attributes
                # can end up inside of the object hierarchy list.
                keys_to_remove.add(key)
        data -= keys_to_remove

        # Don't print the object's methods.
        data -= set([e for e in data
                     if "method" in repr(type(getattr(self, e)))])

        return data

    def data_to_string(self, data):
        for key in sorted(data):
            value = getattr(self, key)
            if value and (type(value) == sa.orm.collections.InstrumentedList or
                          type(value) ==
                          sa.ext.orderinglist.OrderingList):
                value = '[' + ', '.join(
                    "<{}(id={})>".format(e.__class__.__name__, e.id)
                    for e in value) + ']'
            elif value and type(value) == sa.orm.collections.MappedCollection:
                value = "{" + ', '.join(
                    "{}: <{}(id={})>".format(k, v.__class__.__name__, v.id)
                    for k, v in value.items()) + '}'
            # This if/try is a way to print ONE to ONE relationship objects
            # without infinite recursion.
            elif value:
                try:
                    # Dummy call to test if value is a Database object.
                    # value._sa_instance_state  # temporarily removed.
                    value = "<{}(id={})>".format(
                        value.__class__.__name__, value.id)
                except AttributeError:
                    pass  # The object is not a databse object.
            yield '{}={}'.format(key, repr(value))

    def __str__(self):
        """Return string data about a Database object.

        Note: prints lists as list of ids.
        Note2: key.lstrip('_') accesses _attributes as attributes due to my
        convention of using _value, @hybrid_property of value, @value.setter.

        I don't understand why I need all of these ... only that each one seems
        to hold slightly different data than the others with some overlap.

        Not3: super class variables like 'type' and 'name' don't exist in
        WorldMap until they are referenced as they are declared in Map...?
        I called super to fix this ... but it may only allow ONE level of
        superclassing. Multi-level superclasses will probably fail.
        """

        data = self.get_all_atts()
        data_str_gen = self.data_to_string(data)
        return "<{}({})>".format(
            self.__class__.__name__, ', '.join(data_str_gen))

    def pprint(self):
        """Multi-line print of a database object -> good for object diff.

        Basically a string_of clone but one variable per line.
        """

        data = self.get_all_atts()

        print("\n\n<{}(".format(self.__class__.__name__))
        for line in self.data_to_string(data):
                print(line)
        print(")>\n")

    @property
    def pretty(self):
        data = self.get_all_atts()

        lines = (line for line in self.data_to_string(data))
        return "\n<{}(\n{}\n)>\n".format(
            self.__class__.__name__, '\n'.join(lines))

    @staticmethod
    def pretty_list(obj_list, key='id'):
        """Build a human readable string version of a list of objects.

        :param obj_list: The list of Base objects to print.
        :param key: and attribute of the each object to print by.
        :return: A nicely formatted string version of the list.

        Mainly used for print 'InstrumentedList' that most hated of objects.
        NOTE: the list is sorted! If the key can't be sorted then this will
        fail.
        """
        return '[' + ', '.join(
            '{}.{}={}'.format(
                obj.__class__.__name__,
                key,
                repr(getattr(obj, key))
            ) for obj in sorted(
                obj_list,
                key=lambda x, k=key: getattr(x, k))
        ) + ']'

    def is_equal(self, other):
        """Test if two database objects are equal.

        hero.is_equal(hero) vs. str(hero) == str(hero)
        is_equal is 0.3 seconds faster over 1000 iterations than str == str.
        So is_equal is not that useful. I would like it if it was 5-10 times
        faster.
        """
        data = self.get_all_atts()
        other_data = other.get_all_atts()

        if data != other_data:
            return False

        if self.__class__.__name__ != other.__class__.__name__:
            return False

        for key in data:
            value = getattr(self, key)
            other_value = getattr(other, key)
            if value != other_value:
                return False
        return True

    Session = None

    @classmethod
    def query(cls):
        with services.session_helpers.session_scope(cls.Session) as session:
            return session.query(cls)

    @classmethod
    def first(cls):
        return cls.query().first()

    @classmethod
    def get(cls, id_):
        return cls.query().get(id_)

    save = database.sesson_helpers.save


# Initialize SQLAlchemy base class.
convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(column_0_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

# This used a class factory to build a class called base in the local
# context. The engine is a connection to the database. It should
# be live at this point.
metadata = sqlalchemy.MetaData(naming_convention=convention)
Base = sa.ext.declarative.declarative_base(bind=database.engine, cls=Base, metadata=metadata)

Base.Session = sa.orm.sessionmaker(bind=database.engine)
Base.session = Base.Session()

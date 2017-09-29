from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from pprint import pprint
from collections import Callable
from functools import partialmethod, partial

import pdb

def normalize_naming(names, scheme='attribute'):
    """A function to convert a list of names into names of a certain type.

    Returns a generator! So don't reuse!
    Input type is always assumed to be Human Readable names
    e.g. 'Resist flame'
    schemes are:
        attribute -> name.lower().replace(" ", "_")
        classname -> name.title().replace(" ", '')

    Conversion would look like:
    Resist flame -> attribute -> resist_flame
    Resist flame -> classname -> ResistFlame
    """
    if scheme == 'attribute':
        return (name.lower().replace(" ", "_") for name in names)
    elif scheme == 'classname':
        return (name.title().replace(" ", '') for name in names)


class RelationshipCallable(Callable):
    """Return a relationship as a function for mixins"""
    def __init__(self, name, relationship_cls_name, container_name,
                 cls_name):
        self.name = name
        self.relationship_cls_name = relationship_cls_name
        self.container_name = container_name
        self.cls_name = cls_name

    def __call__(self, cls):
        """Makes this object act like a function.

        Basically does this:
        @declared_attr
        def target(cls):
            return relationship("Target",
                primaryjoin="Target.id==cls.target_id".format(cls.__name__)
            )
        and some extra magic too :)
        """
        if False:
            print("and_({}.id=={}.{}_id, {}.name=='{}')".format(
                    self.container_name,
                    self.cls_name,
                    self.container_name.lower(),
                    self.relationship_cls_name,
                    self.name))
        return relationship(
            self.relationship_cls_name,
            primaryjoin="and_({}.id=={}.{}_id, {}.name=='{}')".format(
                self.container_name,
                self.cls_name,
                self.container_name.lower(),
                self.relationship_cls_name,
                self.name),
            back_populates=self.container_name.lower(),
            uselist=False)


def relationship_mixin_factory(container_name, cls_name,
                               attribute_and_class_names,
                               connects_on_class_name=False):
    """Build a Mixin of relationships for the container class.

    Example:
        scholar = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Scholar')",
        back_populates="abilities", uselist=False)
    OR
        health = relationship(
        "Health",
        primaryjoin="and_(Proficiencies.id==Proficiency.proficiencies_id, "
                    "Proficiency.name=='Heath')",
        back_populates="proficiencies", uselist=False)

    NOTE: the attribute name != relationship name
    i.e. 'scholar' != "AuraAbility"
    NOTE: the attribute name == relationship name capitalized
    i.e. 'health' -> "Heath"

    names = [('scholar', 'AuraAbility'), (...)]
    names =[('health', 'Health'), (...)]
    """
    dct = {}
    for name, relationship_cls_name in attribute_and_class_names:

        if connects_on_class_name:
            dct[name] = RelationshipCallable(relationship_cls_name,
                                             relationship_cls_name,
                                             container_name,
                                             cls_name)
        else:
            # TODO: Safer name mangling!
            dct[name] = RelationshipCallable(
                name.title().replace("_", ' '),
                relationship_cls_name,
                container_name,
                cls_name)
        dct[name] = declared_attr(dct[name])
    return type('RelationshipMixin', (object, ), dct)


def container_factory(cls_name, cls_name_singular, supers, names, namespace):
    """Build a container object that pretends to be a normal python class
    but is really a Database object.

    Example init looks like:
        def __init__(self):
            self.health = Health()
            self.sanctity = Sanctity()
    """

    # NOTE: if you don't convert these to lists you can only use them once!
    # This is because it is a generator and generators get used up.
    attrib_names = list(normalize_naming(names))
    attribute_and_class_names = list(
        zip(normalize_naming(names),
            normalize_naming(names, scheme='classname'))
    )

    dct = {
        '__tablename__': cls_name.lower(),
        'id': Column(Integer, primary_key=True),

        # Relationships
        # Hero class, One -> One
        'hero': relationship("Hero", back_populates=cls_name.lower(),
                             uselist=False)
    }

    def setup_init(self):
        """Create a generic init function with a bunch of objects.

        self.health = Health()
        self.sanctity = Sanctity()

        This may not work.
        """
        for attrib, classname in attribute_and_class_names:
            setattr(self, attrib, namespace[classname]())
    dct['__init__'] = setup_init

    RelationshipMixin = relationship_mixin_factory(
        cls_name, cls_name_singular, attribute_and_class_names,
        connects_on_class_name=True)

    IterItemsExtension = iter_items_factory(attrib_names)

    supers += (RelationshipMixin, IterItemsExtension)
    return type(cls_name, supers, dct)


def iter_items_factory(attrib_names):
    dct = {}
    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like
        [(key, value), (key, value), ...]
        """
        return ((key, getattr(self, key)) for key in attrib_names)
    dct['items'] = items

    def __iter__(self):
        """Return all the attributes of this function as a list."""
        return (getattr(self, key) for key in attrib_names)
    dct['__iter__'] = __iter__

    return type("IterItemsExtension", (), dct)


class PolymorphicIdentityOnClassNameMixin:
    """Set the polymorphic identity of an object to its class name."""
    @declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__}

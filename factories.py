from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


def named_relationship_mixin_factory(container_name, cls_name, names):
    """Build a Mixin of relationships for the container class.

    Example:
        health = relationship(
        "Health",
        primaryjoin="and_(Proficiencies.id==Proficiency.proficiencies_id, "
                    "Proficiency.name=='Heath')",
        back_populates="proficiencies", uselist=False)
    OR
        scholar = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='scholar')",
        back_populates="abilities", uselist=False)
    """
    dct = {}
    for false_name in names:
        attr_name = false_name.lower().replace(" ", "_")
        name = false_name.title().replace(" ", '')
        dct[attr_name] = lambda cls, name_=name: relationship(
            name_,
            primaryjoin="and_({}.id=={}.{}_id, {}.name=='{}')".format(
                container_name, cls_name, container_name.lower(),
                cls_name, name_),
            back_populates=container_name.lower(),
            uselist=False,
            cascade="all, delete-orphan")

        dct[attr_name] = declared_attr(dct[attr_name])

    return type('NamedRelationshipMixin', (), dct)


def container_factory(cls_name, cls_name_singular, supers, names, namespace):
    """Build a container object that pretends to be a normal python class
    but is really a Database object.

    Example init looks like:
        def __init__(self):
            self.health = Health()
            self.sanctity = Sanctity()
    """
    attrib_names = [name.lower().replace(" ", "_") for name in names]
    dct = {
        '__tablename__': cls_name.lower(),
        'id': Column(Integer, primary_key=True),

        # Relationships
        # Hero class, One -> One
        'hero_id': Column(Integer, ForeignKey('hero.id',
                                              ondelete="CASCADE")),
        'hero': relationship("Hero", back_populates=cls_name.lower())
    }

    def setup_init(self):
        """Create a generic init function with a bunch of objects.

        self.health = Health()
        self.sanctity = Sanctity()

        This may not work.
        """
        for false_name in names:
            attrib_name = false_name.lower().replace(" ", "_")
            name = false_name.title().replace(" ", '')
            setattr(self, attrib_name, namespace[name]())
    dct['__init__'] = setup_init

    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like
        [(key, value), (key, value), ...]
        """
        return [(key, getattr(self, key)) for key in attrib_names]
    dct['items'] = items

    def __iter__(self):
        """Return all the attributes of this function as a list."""
        return (getattr(self, key) for key in attrib_names)
    dct['__iter__'] = __iter__

    NamedRelationshipMixin = named_relationship_mixin_factory(
        cls_name, cls_name_singular, names)
    supers += (NamedRelationshipMixin, )
    return type(cls_name, supers, dct)


class TemplateMixin(object):
    """Add the ability to use an item of the class as a template.

    NOTE: for inherited class must include:
    def __init__(*arg, template=True, **kwarg)
        self.template = template

    def build_new_from_template(self):
        return FooBar(*arg, **kwarg, template=False)

    Should include a validator that automates template building:
    i.e.
    @validates('trigger')
    def valid_trigger(self, key, trigger):
        if trigger.template:
            trigger = trigger.build_new_from_template()
        return trigger

    !Important!
    To set template creation order in subclass create the column in the
    subclass. There is a better way but I can't get it to work.
    see https://stackoverflow.com/a/3924814 Should be:

    TemplateMixin.template._creation_order = 2

    e.g.
    class Item(TemplateMixin, Base):
        id = etc
        template = Column(Boolean, default=False)
    """

    id = Column(Integer, primary_key=True)

    @declared_attr
    def template(cls):
        col = Column(Boolean, default=False)
        col._creation_order = cls.id._creation_order + 0.5
        return col

    def build_new_from_template(self):
        """Build a new object from a given template object.

        Code should look something like:

        if self.template:
            # should create a new object of same class as self but with
            # data from template object. I guess it is running the init method?
            return self.__class__(self.arg1=arg1, self.arg2=arg2, etc)
        """
        raise Exception("You need to implement this in your code.")

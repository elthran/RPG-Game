{% macro build_container(cls_name, back_populates, names) %}
{% set container_name = cls_name + "Container" %}
{% set container_table_name = cls_name.lower() + "_container" %}
{% set attrib_names = normalized_attrib_names(names) %}
class {{ container_name }}(Base):
    __tablename__ = "{{ container_table_name }}"

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE")),
    hero = relationship("Hero", back_populates="{{ back_populates }}")

    def __init__(self):
        {% for name in attrib_names %}
        {% set class_name = normalized_class_name(names[loop.index0]) %}
        self.{{ name }} = {{ class_name }}()
        {% endfor %}
{% endmacro %}


def container_factory(cls_name, cls_name_singular, supers, names, namespace):
    """Build a container object that pretends to be a normal python class
    but is really a Database object.

    Example init looks like:
        def __init__(self):
            self.health = Health()
            self.sanctity = Sanctity()
    """


    def setup_init(self):
        """Create a generic init function with a bunch of objects.

        self.health = Health()
        self.sanctity = Sanctity()

        This may not work.
        """


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

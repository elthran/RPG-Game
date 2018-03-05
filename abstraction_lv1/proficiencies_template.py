from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from factories import TemplateMixin
from base_classes import Base
from flask import render_template_string

from math import sin, floor

# For testing
from pprint import pprint
import pdb

{% include "proficiencies_data.py" %}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Proficiency", "proficiencies", PROFICIENCY_INFORMATION, no_container=True) }}

class Proficiency(TemplateMixin, Base):
    """Proficiency class that stores data about a hero object.
    """
    __tablename__ = "proficiency"
    
    id = Column(Integer, primary_key=True)

    # Relationships
    # Hero to Proficiencies is One to many?
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="base_proficiencies")

    # Proficiency to Ability is One to Many
    ability_id = Column(Integer, ForeignKey('ability.id', ondelete="CASCADE"))
    ability = relationship("Ability", back_populates="proficiencies")

    # Proficiency to Item is One to Many
    item_id = Column(Integer, ForeignKey('item.id', ondelete="CASCADE"))
    items = relationship("Item", back_populates="proficiencies")

    # Main colums
    level = Column(Integer)
    base = Column(Integer)
    modifier = Column(Float)

    type_ = Column(String(50))
    name = Column(String(50))
    hidden = Column(Boolean)
    description = Column(String(200))
    tooltip = Column(String(50))
    attribute_type = Column(String(50))
    next_value = Column(Integer)
    reason_for_zero = Column(String(50))    # Maybe remove
    current = Column(Integer)
    error = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': "Proficiency",
        'polymorphic_on': type_
    }

    def __init__(self, level=0, base=0, modifier=0, template=False):
        self.type_ = self.__class__.__name__
        self.name = normalize_attrib_name(self.type_)
        self.tooltip = ""
        self.level = level
        self.base = base
        self.modifier = modifier
        self.template = template
        self.current = self.get_final()

    def build_new_from_template(self):
        if not self.template:
            raise Exception("Only use this method if obj.template == True.")
        return self.__class__(level=self.level, base=self.base,
                              modifier=self.modifier, template=False)

    def level_up(self):
        self.level += 1
        self.current = self.get_final()

    def scale_by_level(self):
        """Return some function of the level attribute.

        This is different for each proficiency.
        Options are:

        "root:
        return round((100 * self.level)**0.5 - (self.level / 4), precision)
        "linear"
        return round(value1 * self.level, precision)
        "empty"
        return self.level  # Defaults to 0

        NOTE: base value has now been moved to the get_final() function
        """
        return self.level

    def get_final(self):
        """Return the scaled value + base + modifier percent."""

        return (self.scale_by_level() + self.base) * (self.modifier + 1)

    def get_percent(self):
        """Return the percent of the current to the final value."""
        try:
            return round(self.current / self.get_final(), 2) * 100
        except ZeroDivisionError:
            return 0


{% for prof in PROFICIENCY_INFORMATION %}
{% set prof_class = normalize_class_name(prof[0]) %}
{% set attrib_name = normalize_attrib_name(prof[0]) %}
class {{ prof_class }}(Proficiency):
    __mapper_args__ = {
        'polymorphic_identity': "{{ prof_class }}"
    }

    {% set value = prof[3][0] %}
    def __init__(self, *args, base={{ value[2][-2] }}, **kwargs):
        super().__init__(*args, base=base, **kwargs)
        self.description = "{{ prof[1]}}"
        self.attribute_type = "{{ prof[2]}}"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def scale_by_level(self):
        """Update {{ prof_class }}'s attributes and tooltip variable.
        """

    {% if value[1] == "root" %}
        return round((100 * self.level)**0.5 - (self.level / 4), {{ value[2][1]}})
    {% elif value[1] == "linear" %}
        return round({{ value[2][0] }} * self.level, {{ value[2][2]}})
    {% elif value[1] == "empty" %}
        return super().scale_by_level()
    {% endif %}
    {% if prof[0] == "Block" %}

    def check_shield(self, hero):
        if hero.inventory.left_hand is None or hero.inventory.left_hand.type != "Shield":
            self.chance = 0
            self.reason_for_zero = "You must have a shield equipped"
        else:
            self.reason_for_zero = ""
    {% endif %}

    @property
    def current_tootip(self):
        """Create a tooltip for each variable.
        """
        {% raw %}
        tooltip = """{% for attrib in ['name', 'level', 'base', 'modifier', 'current', 'get_final()', 'get_percent()'] %}
                {% if attrib == 'name' %}<h1>{{ getattr(prof, attrib, "Proficiency error").title() }}</h1>{% else %}
                <li>{{ attrib }}: {{ getattr(prof, attrib, "Proficiency error") }}</li>{% endif %}
        {% endfor %}"""
        {% endraw %}
        return render_template_string(tooltip, prof=self, getattr=getattr)


{% endfor %}


'''{% raw %}
Old code that might need to be readded at some point.
@staticmethod
    def keys():
        return [{% for value in prof[3] %}'{{ normalize_attrib_name(value[0]) }}'{% if not loop.last %}, {% endif %}{% endfor %}]

    def items(self):
        """Basically a dict.items() clone that looks like ((key, value),
            (key, value), ...)

        This is an iterator? Maybe it should be a list or a view?
        """
        return ((key, getattr(self, key)) for key in self.keys())

    def __iter__(self):
        """Return all the attributes of this object as an iterator."""
        return (key for key in self.keys())
{% endraw %}
'''

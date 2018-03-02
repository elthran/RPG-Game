from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from base_classes import Base

from math import sin, floor

# For testing
from pprint import pprint
import pdb

{% include "proficiencies_data.py" %}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Proficiency", "proficiencies", PROFICIENCY_INFORMATION, no_container=True) }}

class Proficiency(Base):
    """Proficiency class that stores data about a hero object.
    """
    __tablename__ = "proficiency"
    
    id = Column(Integer, primary_key=True)

    # Relationships
    # Hero to Proficiencies is One to many?
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="base_proficiencies")

    type_ = Column(String(50))
    description = Column(String(200))
    tooltip = Column(String(50))
    attribute_type = Column(String(50))
    level = Column(Integer)
    next_value = Column(Integer)
    reason_for_zero = Column(String(50))    # Maybe remove
    modifier = Column(Float)
    hidden = Column(Boolean)
    current = Column(Integer)

    # Extra Ability columns
    error = Column(String(50))
    name = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': "Proficiency",
        'polymorphic_on': type_
    }

    def __init__(self, level=0, modifier=1.0):
        self.type_ = self.__class__.__name__
        self.name = normalize_attrib_name(self.type_)
        self.tooltip = ""
        self.level = level
        self.modifier = modifier
        self.current = self.get_final()

    def level_up(self):
        self.level += 1
        self.current = self.get_final()

    def get_base(self):
        """Return some function of the level attribute."""
        return self.level

    def get_final(self):
        """Return the modifier * the base."""
        return self.get_base() * self.modifier

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "{{ prof[1]}}"
        self.attribute_type = "{{ prof[2]}}"
        self.error = "You do not have enough {}".format(self.attribute_type)

{% set value = prof[3][0] %}
    def get_base(self):
        """Update {{ prof_class }}'s attributes and tooltip variable.
        """

    {% if value[1] == "root" %}
        return round((100 * self.level)**0.5 - (self.level / 4) + {{ value[2][0]}}, {{ value[2][1]}})
    {% elif value[1] == "linear" %}
        return round({{ value[2][0] }} * self.level + {{ value[2][1] }}, {{ value[2][2]}})
    {% elif value[1] == "empty" %}
        return super().get_base()
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
        tooltips = []
        for attrib in self.modifiable_on:
            # This creates a tooltip for each variable
            tooltips.append("{}: {}".format(attrib.capitalize(), getattr(
                self, attrib, 'error')))

        # This updates the main tooltip string variable.
        self.tooltip = ';'.join(tooltips)
        return ';'.join(tooltips)


{% endfor %}


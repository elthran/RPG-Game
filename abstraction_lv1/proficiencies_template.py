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
{{ container_helpers.build_container("Proficiency", "proficiencies", PROFICIENCY_INFORMATION) }}

class Proficiency(Base):
    """Proficiency class that stores data about a hero object.
    """
    __tablename__ = "proficiency"
    
    id = Column(Integer, primary_key=True)

    type_ = Column(String(50))
    description = Column(String(200))
    tooltip = Column(String(50))
    attribute_type = Column(String(50))
    level = Column(Integer)
    next_value = Column(Integer)
    is_not_max_level = Column(Boolean)  # Maybe remove
    reason_for_zero = Column(String(50))    # Maybe remove
    modifier = Column(Float)

    # Extra Ability columns
    error = Column(String(50))
    formatted_name = Column(String(50))
    {% for column in ALL_PROFICIENCY_COLUMNS %}
    {{ column }} = Column(Integer)
    {% endfor %}

    # Relationships
    proficiency_container_id = Column(
        Integer, ForeignKey('proficiency_container.id', ondelete="CASCADE"))

    __mapper_args__ = {
        'polymorphic_identity': "Proficiency",
        'polymorphic_on': type_
    }

    def __init__(self, level=0):
        self.type_ = self.__class__.__name__
        self.formatted_name = normalize_attrib_name(self.type_)
        self.tooltip = ""
        # self.reason_for_zero = ""
        self.level = level
        # self.is_not_max_level = False

    def is_max_level(self):
        """Return whether proficiency is max level.

        Should be able to get hero internally but the
        relationships may be messed up.

        Replaces:
            is_not_max_level attribute.
        """

        return self.level >= getattr(
            self.proficiencies.hero.attributes,
            self.attribute_type.lower()
        ).level // 2

    def level_up(self):
        self.level += 1


class DynamicMixin(object):
    @declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maximum = 0
        self.current = 0

    def get_modifiable(self):
        """Return modifiable columns for this class.

        Possible options:
            [(key, getattr(self, key)) for key in attrib_names]
        OR
            [getattr(self, key) for key in attrib_names]
        """
        attrib_names = ['maximum']
        return [getattr(self, key) for key in attrib_names]


class Health(Proficiency):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "How much you can take before you die"
        self.attribute_type = "Vitality"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def update(self, hero):
        """Update Health's attributes and tooltip variable.
        """

        self.maximum = round(2 * self.level + 5, 0)
        self.current = self.maximum
        super().generic_update(hero)


class Sanctity(DynamicMixin, Proficiency):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "Amount of sanctity you can have"
        self.attribute_type = "Divinity"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def update(self, hero):
        """Update Sanctity's attributes and tooltip variable.
        """

        self.maximum = round(3 * self.level + 0, 0)
        self.current = self.maximum
        super().generic_update(hero)


class Endurance(DynamicMixin, Proficiency):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "Actions performed each day"
        self.attribute_type = "Resilience"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def update(self, hero):
        """Update Endurance's attributes and tooltip variable.
        """
        self.maximum = round(1 * self.level + 3, 0)
        self.current = self.maximum
        super().generic_update(hero)


class Storage(DynamicMixin, Proficiency):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "Your carrying capacity"
        self.attribute_type = "Brawn"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def update(self, hero):
        """Update Storage's attributes and tooltip variable.
        """

        self.maximum = round(2 * self.level + 10, 0)
        self.current = self.maximum
        super().generic_update(hero)


class StaticMixin(object):
    @declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__}

    def __init__(self, *args, **kwargs):
        """Generic init for static classes.

        Main usage is to set init values to 0.
        Example (the code does):
            self.speed = 0
        OR
            self.skill = 0
        """
        super().__init__(*args, **kwargs)
        for attrib in self.modifiable_on:
            setattr(self, attrib, 0)

    @property
    def modifiable_on(self):
        return ['ability', 'accuracy', 'amount', 'chance', 'efficiency',
                'maximum', 'minimum', 'modifier', 'skill', 'speed']

    def get_all_modifiable(self):
        """Return modifiable columns for this class.

        Possible options:
            [(key, getattr(self, key)) for key in attrib_names]
        OR
            [getattr(self, key) for key in attrib_names]
        """
        return [getattr(self, key) for key in self.modifiable_on]

    def generic_update(self, hero):



class Regeneration(StaticMixin, Proficiency):
    @property
    def modifiable_on(self):
        return ['speed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "How quickly your wounds heal"
        self.attribute_type = "Vitality"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def update(self, hero):
        """Update Regeneration's attributes and tooltip variable.
        """
        self.speed = round((100 * self.level)**0.5 - (self.level / 4) + 1, 2)
        super().generic_update(hero)

{% for prof in PROFICIENCY_INFORMATION %}
{% set prof_class = normalize_class_name(prof[0]) %}
{% set attrib_name = normalize_attrib_name(prof[0]) %}
class {{ prof_class }}(Proficiency):
    __mapper_args__ = {
        'polymorphic_identity': cls.__name__
    }
    @property
    def modifiable_on(self):
        return [{% for value in prof[3] %}'{{ value[0] | normalized_attrib_name }}', {% endfor %}]

    @property
    def percent(self):
        try:
            return round(self.current / self.maximum, 2) * 100
        except ZeroDivisionError:
            return 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "{{ prof[1]}}"
        self.attribute_type = "{{ prof[2]}}"
        self.error = "You do not have enough {}".format(self.attribute_type)

    def update(self, hero):
        """Update {{ prof_class }}'s attributes and tooltip variable.
        """
        {% for value in prof[3] %}
        {% if value[1] == "root" %}
        self.{{ value[0].lower() }} = round((100 * self.level)**0.5 - (self.level / 4) + {{ value[2][0]}}, {{ value[2][1]}})
        {% elif value[1] == "linear" %}
        self.{{ value[0].lower() }} = round({{ value[2][0] }} * self.level + {{ value[2][1] }}, {{ value[2][2]}})
        {% elif value[1] == "empty" %}
        self.{{ value[0].lower() }} = self.maximum
        {% endif %}
        {% endfor %}
        {% if prof[0] == "Block" %}
        if hero.inventory.left_hand is None or hero.inventory.left_hand.type != "Shield":
            self.chance = 0
            self.reason_for_zero = "You must have a shield equipped"
        else:
            self.reason_for_zero = ""
        {% endif %}

    @property
    def current_tootip(self):
        """Generic update function.
        """
        # This creates a tooltip for each variable
        tooltips = ["Maximum: {}".format(self.maximum)]
        # This updates the main tooltip string variable.
        self.tooltip = ';'.join(tooltips)
        """Generic update function.

                Requires that modifiable_on be declared in
                subclass.

                Usage does:
                    for item in hero.equipped_items():
                        self.efficiency += item.recovery_efficiency
                    for ability in hero.abilities:
                        self.efficiency += ability.recovery_efficiency * ability.level
                OR
                    for item in hero.equipped_items():
                        self.speed += item.regeneration_speed
                    for ability in hero.abilities:
                        self.speed += ability.regeneration_speed * ability.level

                Also sets the tooltip variable. Which will probably get moved to JS.
                """
        tooltips = []
        for attrib in self.modifiable_on:
            # This creates a tooltip for each variable
            tooltips.append("{}: {}".format(attrib.capitalize(), getattr(
                self, attrib, 'error')))

            item_attrib = self.__class__.__name__.lower() + attrib
            for item in hero.equipped_items():
                new_value = 0
                try:
                    new_value = getattr(item, item_attrib)
                except AttributeError:
                    # If the item doesn't have this attribute, don't worry
                    # about it.
                    pass
                new_value += getattr(self, attrib)
                setattr(self, attrib, new_value)

            for ability in hero.abilities:
                new_value = 0
                try:
                    new_value = getattr(ability, item_attrib)
                except AttributeError:
                    # If the item doesn't have this attribute, don't worry
                    # about it.
                    pass
                new_value *= ability.level
                new_value += getattr(self, attrib)
                setattr(self, attrib, new_value)

        # This updates the main tooltip string variable.
        self.tooltip = ';'.join(tooltips)

{% endfor %}


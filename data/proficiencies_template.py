"""This file is generated by "data/build_code.py"
It has been set to read only so that you don't edit it without using
build_code.py.
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, validates

from base_classes import Base

from math import sin, floor

{% include "proficiencies_data.py" %}

class Proficiencies(Base):
    __tablename__ = 'proficiencies'
    
    id = Column(Integer, primary_key=True)

    #Relationships     
    {%- for name in ALL_PROFICIENCIES %}
    {{ name }}_id = Column(Integer, ForeignKey('proficiency.id'))
    {{ name }} = relationship("Proficiency", uselist=False, foreign_keys="[Proficiencies.{{ name }}_id]")
    {%- endfor %}
    
    def __init__(self):
        {% for prof in PROFICIENCY_INFORMATION %}
        {% set objectValue = prof[0].title().replace(" ", '') -%}
        self.{{ prof[0].lower().replace(' ', '_') }} = {{ objectValue }}("{{ prof[0] }}", "{{ prof[1] }}", "{{ prof[2] }}", "{{ prof[3] }}")
        {%- endfor %}
        

    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like ([(key, value), (key, value), ...])
        """
        return ((key, getattr(self, key)) for key in ALL_PROFICIENCIES)
        
        
    def __iter__(self):
        return (getattr(self, key) for key in ALL_PROFICIENCIES)

        
class Proficiency(Base):
    """Proficiency class that stores data about a hero object.
    """
    __tablename__ = "proficiency"
    
    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)
    tooltip = Column(String)
    attribute_type = Column(String)
    type = Column(String)
    level = Column(Integer)
    next_value = Column(Integer)
    is_not_max_level = Column(Boolean)
    
    _class = Column(String)
    __mapper_args__ = {
        'polymorphic_identity':"Proficiency",
        'polymorphic_on':_class
    }

    def __init__(self, name, description, attribute_type, type):
        self.name = name
        self.description = description
        self.attribute_type = attribute_type
        self.type = type
        self.tooltip = ""
        
        self.level = 1
        self.is_not_max_level = False
        
    def is_max_level(self, hero):
        """Return whether proficiency is max level.
        
        Should be able to get hero internally but the 
        relationships may be messed up.
        
        Replaces:
            is_not_max_level attribute.
        """
        return self.level >= getattr(hero.attributes, self.attribute_type.lower()).level // 2
        
    def level_up(self):
        self.level += 1

{% for prof in PROFICIENCY_INFORMATION %}
{% set prof_class = prof[0].title().replace(" ", '') -%}
{% set prof_tablename = prof[0].lower().replace(" ", '_') -%}
class {{ prof_class }}(Proficiency):
    __tablename__ = "{{ prof_tablename }}"

    id = Column(Integer, ForeignKey("proficiency.id"), primary_key=True)

    {% for column in prof[4] -%}
    {{ column[0].lower() }} = Column(Integer)
    {% endfor %}
    {% if prof[4][0][0] == "Maximum" -%}
    percent = Column(Integer)
    {%- endif %}
    error = Column(String)
    formatted_name = Column(String)
    __mapper_args__ = {
        'polymorphic_identity':"{{ prof_class }}",
}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        {% for value in prof[4] -%}
        self.{{ value[0].lower() }} = 0
        {% endfor -%}
        {% if prof[4][0][0] == "Maximum" -%}
        self.percent = 0
        {%- endif %}
        self.error = "You do not have enough {{ prof[2].lower() }}"
        self.formatted_name = "{{ prof_tablename }}" # (Elthran) I needed to add this to get the COMMAND code to work. Hopefully (Haldon) can improve this.
        
    def update(self, myHero):
        self.tooltip = "" # This creates the tooltip variable. I think the way I have done it is very shitty.
        if self.level < myHero.attributes.{{ prof[2].lower() }}.level // 2:
            self.is_not_max_level = True
        else:
            self.is_not_max_level = False
        {% for value in prof[4] -%}
        {% if value[1] == "percent" -%}
        self.{{ value[0].lower() }} = floor((- ({{ value[2][1] }}*{{ value[2][2] }})/(({{ value[2][0] }} * self.level) + {{ value[2][1] }}) + {{ value[2][2] }}) * 7.9 + {{ value[2][3] }})
        {% elif value[1] == "linear" -%}
        self.{{ value[0].lower() }} = floor({{ value[2][0] }}*self.level + {{ value[2][1] }})
        {% elif value[1] == "curvy" -%}
        self.{{ value[0].lower() }} = floor(floor(3 * ({{ value[2][0] }}*sin({{ value[2][2] }}*self.level) + {{ value[2][1] }}*self.level)) + {{ value[2][3] }})
        {% elif value[1] == "sensitive" -%}
        self.{{ value[0].lower() }} = round((3 * ({{ value[2][0] }}*sin({{ value[2][2] }}*self.level) + {{ value[2][1] }}*self.level)) + {{ value[2][3] }}, 2)
        {% elif value[1] == "empty" -%}
        self.{{ value[0].lower() }} = self.maximum
        {% endif -%}
        {% if value[1] != "empty" -%}
        self.tooltip += "{{ value[0].title() }}: " + str(self.{{ value[0].lower() }}) + ";" # This adds a tooltip for each variable
        {% endif -%}
        {% endfor -%}
        self.tooltip = self.tooltip[:-1] # This removes the separating character from the end of the final tooltip in the list. Please help me improve this code

    {% if prof[4][0][0] == "Maximum" -%}
    @validates('current')
    def validate_{{ prof[0].lower() }}(self, key_name, current):
        #Update {{ prof[0].lower() }} percent on health change.
        try:
            self.percent = round(current / self.maximum, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.percent = 0
        return max(current or 0, 0)
    {%- endif %}
    
{% endfor %}



    """

    @validates('endurance')
    def sync_endurance_percent(self, key_name, endurance_value):
        #Update endurance_percent on endurance change.

        try:
            self.endurance_percent = round(endurance_value / self.proficiencies.endurance.maximum, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.endurance_percent = 0

        return max(endurance_value, 0)

    @validates('sanctity')
    def sync_sanctity_percent(self, key_name, sanctity_value):
        #Update sanctity_percent on sanctity change.

        try:
            self.sanctity_percent = round(sanctity_value / self.proficiencies.sanctity.maximum, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.sanctity_percent = 0

        return max(sanctity_value, 0)

    @validates('experience')
    def sync_experience_percent(self, key_name, xp_value):
        #Update exp_percent on current_exp change.

        #String conversion occurs in HTML and add the percent sign is added there to.
        #key_name is "current_exp" .. not actually used here at this time but it is sent to
        #this function so it must be accepted.

        try:
            self.experience_percent = round(xp_value / self.experience_maximum, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.experience_percent = 0
        return xp_value

    @validates('health')
    def sync_health_percent(self, key_name, health_value):
        #Update health_percent on health change.

        try:
            self.health_percent = round(health_value / self.proficiencies.health.maximum, 2) * 100
        except (TypeError, ZeroDivisionError):
            self.health_percent = 0

        return max(health_value or 0, 0)
    """

    
    def __iter__(self):
        pass # I don't know what to put here yet but it will be used later on.

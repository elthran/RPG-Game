from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from flask import render_template_string

from base_classes import Base
import pdb

# This is a list of specializations. Your hero can have one of each type active at any time. There are 4 types of specs.
# You get one basic spec which defines your basic character stats. Then you further choose an archetype (eg. Scoundrel -> Thief,
# or Ascetic -> Monk). Then you can also choose a calling, which is more like your career path. And lastly you choose a religion.
# Each of the 4 choices unlocks different abilities to learn. So each character will be very unique based on the 4 paths they choose.
# name, type, description, requirements

ALL_SPECIALIZATIONS = {{ ALL_SPECIALIZATIONS }}

SPECIALIZATION_NAMES = [key[0] for key in ALL_SPECIALIZATIONS]

SPECIALIZATIONS_CATEGORIES = ['archetype', 'calling']

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Ability", "abilities", ALL_SPECIALIZATIONS, no_container=True) }}

class Specialization(Base):
    __tablename__ = "specialization"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))  # Maybe 'unique' is not necessary?
    type = Column(String(50))
    description = Column(String(200))
    requirements = Column(String(50))

    # Relationships
    # Each hero can have one list of abilities (bi, one to one)
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="specializations")

    # I DONT KNOW WHAT THIS DOES!!!?? :'( - Elthran
    __mapper_args__ = {
        'polymorphic_identity': 'Specialization',
        'polymorphic_on': type
    }

    def __init__(self, name, description, requirements):
        self.name = name
        self.description = description
        self.requirements = requirements


class Archetype(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'ArchetypeSpecialization',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Calling(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'CallingSpecialization',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pantheon(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'PantheonSpecialization',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


{% for spec in ALL_SPECIALIZATIONS %}
{% set cls_name = normalize_class_name(spec[0]) %}
{% set spec_type = "Specialization" if spec[1] in ["BasicSpecialization", "basic"] else spec[1] %}
{% set description = spec[2] %}
{% set requirements = spec[3] %}
class {{ cls_name }}({{ spec_type }}):
    attrib_name = "{{ normalize_attrib_name(spec[0]) }}"

    __mapper_args__ = {
        'polymorphic_identity': '{{ cls_name }}',
    }

    def __init__(self, args=("{{ cls_name }}", "{{ description }}", "{{ requirements }}"), **kwargs):
        super().__init__(*args, **kwargs)
{% if loop.last %}
{% else %}


{% endif %}
{% endfor %}

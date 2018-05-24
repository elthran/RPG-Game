import sqlalchemy as sa
import sqlalchemy.orm

import models
import services.naming
import interfaces.requirements

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

class HeroSpecializationAccess(models.Base):
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"), primary_key=True)
    specialization_id = sa.Column(sa.Integer, sa.ForeignKey('specialization.id'), primary_key=True)
    hidden = sa.Column(sa.Boolean)
    disabled = sa.Column(sa.Boolean)
    specialization = sa.orm.relationship("Specialization")
    hero = sa.orm.relationship("Hero")

    def __init__(self, specialization, hidden=True, disabled=True):
        self.specialization = specialization
        self.hidden = hidden
        self.disabled = disabled
        self.requirement_interface = None
        # self.requirement_interface = interfaces.requirements.Requirement(self.requirements)

    # @orm.reconstructor
    # def init_on_load(self):
    #     self.requirement_interface = interfaces.requirements.Requirement(self.requirements)

    def check_locked(self, hero):
        if getattr(self, 'requirement_interface', None) is None:
            self.requirement_interface = interfaces.requirements.Requirement(self.specialization.requirements)
        self.disabled = not self.requirement_interface.met(hero)
        return self.disabled


class Specialization(models.mixins.TemplateMixin, models.Base):
    name = sa.Column(sa.String(50))  # Maybe 'unique' is not necessary?
    type = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))
    requirements = sa.Column(sa.String(50))
    attrib_name = sa.Column(sa.String(50))
    hidden = sa.Column(sa.Boolean)

    # Relationships
    # Each hero can have one list of abilities (bi, one to one)
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship(
        "Hero",
        back_populates="_specializations",
        cascade="all, delete-orphan",
        single_parent=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Specialization',
        'polymorphic_on': type
    }

    def __init__(self, name, description, requirements, template=False):
        self.name = name
        self.attrib_name = services.naming.normalize_attrib_name(name)
        self.description = description
        self.requirements = requirements
        self.template = template
        self.hidden = True


class Archetype(Specialization):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'Archetype',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Calling(Specialization):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'Calling',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pantheon(Specialization):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'Pantheon',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


{% for spec in ALL_SPECIALIZATIONS %}
{% set cls_name = normalize_class_name(spec[0]) %}
{% set spec_type = spec[1] %}
{% set description = spec[2] %}
{% set requirements = spec[3] %}
def {{ cls_name }}(template=False):
    return {{ spec_type }}("{{ cls_name }}", "{{ description }}", "{{ requirements }}", template=template)
# What do the two lines of code below do?
{% if loop.last %}
{% else %}


{% endif %}
{% endfor %}

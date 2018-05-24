"""
This file is generated by 'build_code.py'.
It has been set to read only so that you don't edit it without using
'build_code.py'. Thought that may change in the future.
"""

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

ALL_SPECIALIZATIONS = [('Brute', 'Archetype', 'A character who uses strength and combat to solve problems. Proficient with many types of weapons.', 'Brawn Attribute Level 3'), ('Scoundrel', 'Archetype', 'A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.', 'Dagger Talent of 6, Virtue of -100'), ('Ascetic', 'Archetype', 'A character who focuses on disciplining mind and body. They use a combination of combat and intellect.', '10 Errands Complete, Virtue of 100, Willpower of 4'), ('Survivalist', 'Archetype', 'A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.', '5 Locations Discovered, 10 Animals in Bestiary'), ('Philosopher', 'Archetype', 'A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.', 'Alchemy Ability Level 3'), ('Opportunist', 'Archetype', 'A character who solves problems using speech and dialogue.', 'Charisma of 7, Fame of 200'), ('Test Calling', 'Calling', 'A blacksmith dude.', 'Be a dude ... who likes hitting hot metal.'), ('Test Pantheon', 'Pantheon', 'A fire god dude.', 'Be a Pyro ... and a dude.')]

SPECIALIZATION_NAMES = [key[0] for key in ALL_SPECIALIZATIONS]

SPECIALIZATIONS_CATEGORIES = ['archetype', 'calling']

ALL_NAMES = ['Ascetic', 'Brute', 'Opportunist', 'Philosopher', 'Scoundrel', 'Survivalist', 'Test  calling', 'Test  pantheon']
ALL_ATTRIBUTE_NAMES = ['ascetic', 'brute', 'opportunist', 'philosopher', 'scoundrel', 'survivalist', 'test__calling', 'test__pantheon']
ALL_CLASS_NAMES = ['Ascetic', 'Brute', 'Opportunist', 'Philosopher', 'Scoundrel', 'Survivalist', 'TestCalling', 'TestPantheon']


class HeroSpecializationAccess(Base):
    __tablename__ = 'hero_specialization_access'
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"), primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specialization.id'), primary_key=True)
    hidden = Column(Boolean)
    disabled = Column(Boolean)
    specialization = relationship("Specialization")
    hero = relationship("Hero")

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
    hidden = Column(Boolean)

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


def Brute(template=False):
    return Archetype("Brute", "A character who uses strength and combat to solve problems. Proficient with many types of weapons.", "Brawn Attribute Level 3", template=template)
# What do the two lines of code below do?


def Scoundrel(template=False):
    return Archetype("Scoundrel", "A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.", "Dagger Talent of 6, Virtue of -100", template=template)
# What do the two lines of code below do?


def Ascetic(template=False):
    return Archetype("Ascetic", "A character who focuses on disciplining mind and body. They use a combination of combat and intellect.", "10 Errands Complete, Virtue of 100, Willpower of 4", template=template)
# What do the two lines of code below do?


def Survivalist(template=False):
    return Archetype("Survivalist", "A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.", "5 Locations Discovered, 10 Animals in Bestiary", template=template)
# What do the two lines of code below do?


def Philosopher(template=False):
    return Archetype("Philosopher", "A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.", "Alchemy Ability Level 3", template=template)
# What do the two lines of code below do?


def Opportunist(template=False):
    return Archetype("Opportunist", "A character who solves problems using speech and dialogue.", "Charisma of 7, Fame of 200", template=template)
# What do the two lines of code below do?


def TestCalling(template=False):
    return Calling("TestCalling", "A blacksmith dude.", "Be a dude ... who likes hitting hot metal.", template=template)
# What do the two lines of code below do?


def TestPantheon(template=False):
    return Pantheon("TestPantheon", "A fire god dude.", "Be a Pyro ... and a dude.", template=template)
# What do the two lines of code below do?

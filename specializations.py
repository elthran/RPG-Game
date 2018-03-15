"""
This file is generated by 'build_code.py'.
It has been set to read only so that you don't edit it without using
'build_code.py'. Thought that may change in the future.
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from flask import render_template_string

from base_classes import Base
from factories import TemplateMixin
from build_code import normalize_attrib_name
import pdb

# This is a list of specializations. Your hero can have one of each type active at any time. There are 4 types of specs.
# You get one basic spec which defines your basic character stats. Then you further choose an archetype (eg. Scoundrel -> Thief,
# or Ascetic -> Monk). Then you can also choose a calling, which is more like your career path. And lastly you choose a religion.
# Each of the 4 choices unlocks different abilities to learn. So each character will be very unique based on the 4 paths they choose.
# name, type, description, requirements

ALL_SPECIALIZATIONS = [('Brute', 'Archetype', 'A character who uses strength and combat to solve problems. Proficient with many types of weapons.', 'Brawn of 6, Any Weapon Talent ~ 10'), ('Scoundrel', 'Archetype', 'A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.', 'Dagger Talent of 6, Virtue of -100'), ('Ascetic', 'Archetype', 'A character who focuses on disciplining mind and body. They use a combination of combat and intellect.', '10 Errands Complete, Virtue of 100, Willpower of 4'), ('Survivalist', 'Archetype', 'A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.', '5 Locations Discovered, 10 Animals in Bestiary'), ('Philosopher', 'Archetype', 'A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.', 'Intellect of 7, Books Read of 10'), ('Opportunist', 'Archetype', 'A character who solves problems using speech and dialogue.', 'Charisma of 7, Fame of 200'), ('Blacksmith', 'Calling', 'A blacksmith dude.', 'Be a dude ... who likes hitting hot metal.'), ('Fire god', 'Pantheon', 'A fire god dude.', 'Be a Pyro ... and a dude.')]

SPECIALIZATION_NAMES = [key[0] for key in ALL_SPECIALIZATIONS]

SPECIALIZATIONS_CATEGORIES = ['archetype', 'calling']

ALL_NAMES = ['Ascetic', 'Blacksmith', 'Brute', 'Fire god', 'Opportunist', 'Philosopher', 'Scoundrel', 'Survivalist']
ALL_ATTRIBUTE_NAMES = ['ascetic', 'blacksmith', 'brute', 'fire_god', 'opportunist', 'philosopher', 'scoundrel', 'survivalist']
ALL_CLASS_NAMES = ['Ascetic', 'Blacksmith', 'Brute', 'FireGod', 'Opportunist', 'Philosopher', 'Scoundrel', 'Survivalist']


class Specialization(TemplateMixin, Base):
    __tablename__ = "specialization"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))  # Maybe 'unique' is not necessary?
    type = Column(String(50))
    description = Column(String(200))
    requirements = Column(String(50))
    attrib_name = Column(String(50))

    # Relationships
    # Each hero can have one list of abilities (bi, one to one)
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship(
        "Hero",
        back_populates="_specializations",
        cascade="all, delete-orphan",
        single_parent=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Specialization',
        'polymorphic_on': type
    }

    def __init__(self, name, description, requirements, template=False):
        """Create a new Specialization object.

        NOTE: you can pretty much ignore templating hero as when you
        assign a value to a hero it creates a new object from the template.
        """
        self.name = name
        self.attrib_name = normalize_attrib_name(name)
        self.description = description
        self.requirements = requirements
        self.template = template


class Archetype(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'Archetype',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Calling(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'Calling',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pantheon(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'Pantheon',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def Brute(template=False):
    return Archetype("Brute", "A character who uses strength and combat to solve problems. Proficient with many types of weapons.", "Brawn of 6, Any Weapon Talent ~ 10", template=template)


def Scoundrel(template=False):
    return Archetype("Scoundrel", "A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.", "Dagger Talent of 6, Virtue of -100", template=template)


def Ascetic(template=False):
    return Archetype("Ascetic", "A character who focuses on disciplining mind and body. They use a combination of combat and intellect.", "10 Errands Complete, Virtue of 100, Willpower of 4", template=template)


def Survivalist(template=False):
    return Archetype("Survivalist", "A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.", "5 Locations Discovered, 10 Animals in Bestiary", template=template)


def Philosopher(template=False):
    return Archetype("Philosopher", "A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.", "Intellect of 7, Books Read of 10", template=template)


def Opportunist(template=False):
    return Archetype("Opportunist", "A character who solves problems using speech and dialogue.", "Charisma of 7, Fame of 200", template=template)


def Blacksmith(template=False):
    return Calling("Blacksmith", "A blacksmith dude.", "Be a dude ... who likes hitting hot metal.", template=template)


def FireGod(template=False):
    return Pantheon("FireGod", "A fire god dude.", "Be a Pyro ... and a dude.", template=template)

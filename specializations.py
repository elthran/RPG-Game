from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from flask import render_template_string

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base
import pdb

# This is a list of specializations. Your hero can have one of each type active at any time. There are 4 types of specs.
# You get one basic spec which defines your basic character stats. Then you further choose an archetype (eg. Scoundrel -> Thief,
# or Ascetic -> Monk). Then you can also choose a calling, which is more like your career path. And lastly you choose a religion.
# Each of the 4 choices unlocks different abilities to learn. So each character will be very unique based on the 4 paths they choose.
# name, type, description, requirements

ALL_SPECIALIZATIONS = [
    ("Brute", "BasicSpecialization", "A character who uses strength and combat to solve problems. Proficient with many types of weapons.", "Brawn of 6, Any Weapon Talent ~ 10"),
    #("Scoundrel", "basic",  "A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.", "Dagger Talent of 6, Virtue of -100"),
    #("Ascetic", "basic",  "A character who focuses on disciplining mind and body. They use a combination of combat and intellect.", "10 Errands Complete, Virtue of 100, Willpower of 4"),
    #("Survivalist", "basic",  "A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.", "5 Locations Discovered, 10 Animals in Bestiary"),
    #("Philosopher", "basic",  "A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.", "Intellect of 7, Books Read of 10"),
    #("Opportunist", "basic",  "A character who solves problems using speech and dialogue.", "Charisma of 7, Fame of 200"),
    ("ArchetypeTEST", "archetype", "TEST CODE1", "TEST1"),
    ("CallingTEST", "calling", "TEST CODE2", "TEST2"),
    ("PantheonTEST", "pantheon", "TEST CODE3", "TEST3")
]

SPECIALIZATION_NAMES = [key[0] for key in ALL_SPECIALIZATIONS]

# Relationships to a particular ability.
# Brute = relationship(
#     "BasicSpecialization",
#     primaryjoin="and_(SpecializationContainer.id==Specialization.specialization_container_id, "
#                 "Specialization.name=='Brute')",
#     back_populates="specialization_container", uselist=False)
# ArchetypeTEST = relationship(
#     "ArchetypeSpecialization",
#     primaryjoin="and_(Specializations.id==Specializations.specializations_id, "
#                 "Specializations.name=='ArchetypeTEST')",
#     back_populates="Specializations", uselist=False)
# CallingTEST = relationship(
#     "CallingSpecialization",
#     primaryjoin="and_(Specializations.id==Specializations.specializations_id, "
#                 "Specializations.name=='CallingTEST')",
#     back_populates="Specializations", uselist=False)
# PantheonTEST = relationship(
#     "PantheonSpecialization",
#     primaryjoin="and_(Specializations.id==Specializations.specializations_id, "
#                 "Specializations.name=='PantheonTEST')",
#     back_populates="Specializations", uselist=False)

# def __init__(self):
    # self.ArchetypeTEST = ArchetypeSpecialization('ArchetypeTEST', 'archetype', 'TEST CODE1', 'TEST1')
    # self.CallingTEST = CallingSpecialization('CallingTEST', 'calling', 'TEST CODE2', 'TEST2')
    # self.PantheonTEST = PantheonSpecialization('PantheonTEST', 'pantheon', 'TEST CODE3', 'TEST3')


class Specialization(Base):
    __tablename__ = "specialization"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Maybe 'unique' is not necessary?
    type = Column(String)
    description = Column(String)
    requirements = Column(String)

    # Relationships.
    # Relationships
    # Each hero can have one list of abilities (bi, one to one)
    hero_id = Column(Integer, ForeignKey('hero.id'))
    hero = relationship("Hero")

    # I DONT KNOW WHAT THIS DOES!!!?? :'( - Elthran
    __mapper_args__ = {
        'polymorphic_identity': 'Specialization',
        'polymorphic_on': type
    }

    def __init__(self, name, description, requirements):
        self.name = name
        self.description = description
        self.requirements = requirements


class BasicSpecialization(Specialization):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'BasicSpecialization',
    }


class ArchetypeSpecialization(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'ArchetypeSpecialization',
    }


class CallingSpecialization(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'CallingSpecialization',
    }


class PantheonSpecialization(Specialization):
    __mapper_args__ = {
        'polymorphic_identity': 'PantheonSpecialization',
    }




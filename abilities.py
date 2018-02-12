# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
#  Author: Elthran B, Jimmy Zhang                                             #
#  Email : jimmy.gnahz@gmail.com                                              #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from flask import render_template_string

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base
import pdb

"""

Abilities spec goes:

name, class, class arguments (not including name as it is added later).
"""

ALL_ABILITIES = [
    ("Relentless", "AuraAbility", "5, 'Gain {{ level * 5 }} maximum health. Master this ability to unlock the Brute archetype.', learnable=True, health_maximum=5"),
    ("Trickster", "AuraAbility", "5, 'Become {{ level * 5 }}% harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.', learnable=True, stealth_chance=5"),
    ("Discipline", "AuraAbility", "5, 'Gain devotion {{ level * 5 }}% faster. Master this ability to unlock the Ascetic archetype.', learnable=True"),
    ("Explorer", "AuraAbility", "5, 'Reveal {{ level * 10 }}% more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.', learnable=True"),
    ("Arcanum", "AuraAbility", "5, 'Gain {{ level * 3 }} maximum sanctity. Master this ability to unlock the Philosopher archetype.', learnable=True, sanctity_maximum=3"),
    ("Poet", "AuraAbility", "5, 'Gain fame {{ level * 5 }}% faster. Master this ability to unlock the Opportunist archetype.', learnable=True"),
    ("Blackhearted", "AuraAbility", "3, 'Lose virtue {{ level * 5 }}% faster.', tree='archetype', tree_type='scoundrel'"),
    ("Backstab", "AuraAbility", "3, 'You are {{ level * 15 }}% more likely to attack first in combat.', tree='archetype', tree_type='scoundrel', firststrike_chance=15"),
    ("MartialArts", "AuraAbility", "3, 'You deal {{ level * 5 }}% more damage in combat.', tree='archetype', tree_type='ascetic'"),
    ("Apprentice", "AuraAbility", "3, 'You are capable of learning level {{ level }} spells.', tree='archetype', tree_type='ascetic'"),
    ("Meditation", "AuraAbility", "3, 'Regenerate {{ level }} sanctity per day.', tree='archetype', tree_type='ascetic', sanctity_regeneration=1"),
    ("Bash", "AuraAbility", "3, 'You deal {{ level * 10 }}% more damage with blunt weapons.', tree='archetype', tree_type='brute'"),
    ("Student", "AuraAbility", "3, 'You are capable of learning level {{ level }} spells.', tree='archetype', tree_type='philosopher'"),
    ("Scholar", "AuraAbility", "3, 'Gain experience {{ level }}% faster.', learnable=True, tree='archetype', tree_type='philosopher', understanding_modifier=1"),
    ("Vigilance", "AuraAbility", "3, 'You are {{ level * 10 }}% less likely to be ambushed.', tree='archetype', tree_type='survivalist'"),
    ("Strider", "AuraAbility", "3, 'Traveling on the map requires {{ level * 10 }}% less endurance.', tree='archetype', tree_type='survivalist'"),
    ("Skinner", "AuraAbility", "3, 'You have a {{ level * 5 }}% chance of obtaining a usable fur after kiling a beast.', tree='archetype', tree_type='survivalist'"),
    ("Charm", "AuraAbility", "3, 'You are {{ level * 5 }}% more likely to succeed when choosing charm dialogues.', tree='archetype', tree_type='opportunist'"),
    ("Haggler", "AuraAbility", "3, 'Prices at shops are {{ level * 3}}% cheaper.', tree='archetype', tree_type='opportunist'")
]


ABILITY_NAMES = [key[0] for key in ALL_ABILITIES]

"""
End of documentation.

"""

# "determination", 5, "Increases Endurance by 3 for each level."


class Abilities(Base):
    __tablename__ = 'abilities'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Each hero can have one list of abilities (bi, one to one)
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates='abilities')

    # Relationships to a particular ability.
    Relentless = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Relentless')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Trickster = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Trickster')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Discipline = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Discipline')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Explorer = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Explorer')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Arcanum = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Arcanum')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Poet = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Poet')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Blackhearted = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Blackhearted')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Backstab = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Backstab')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    MartialArts = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='MartialArts')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Apprentice = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Apprentice')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Meditation = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Meditation')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Bash = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Bash')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Student = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Student')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Scholar = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Scholar')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Vigilance = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Vigilance')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Strider = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Strider')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Skinner = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Skinner')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Charm = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Charm')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")
    
    Haggler = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='Haggler')",
        back_populates="abilities", uselist=False,
        cascade="all, delete-orphan")

    def __init__(self):
        self.Relentless = AuraAbility('Relentless', 5, 'Gain <font color="green">{{ (level+1) * 5 }}</font> maximum health. Master this ability to unlock the Brute archetype.', learnable=True, health_maximum=5)
        self.Trickster = AuraAbility('Trickster', 5, 'Become <font color="green">{{ (level+1) * 5 }}</font>% harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.', learnable=True, stealth_chance=5)
        self.Discipline = AuraAbility('Discipline', 5, 'Gain devotion <font color="green">{{ (level+1) * 5 }}</font>% faster. Master this ability to unlock the Ascetic archetype.', learnable=True)
        self.Explorer = AuraAbility('Explorer', 5, 'Reveal <font color="green">{{ (level+1) * 10 }}</font>% more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.', learnable=True)
        self.Arcanum = AuraAbility('Arcanum', 5, 'Gain <font color="green">{{ (level+1) * 3 }}</font> maximum sanctity. Master this ability to unlock the Philosopher archetype.', learnable=True, sanctity_maximum=3)
        self.Poet = AuraAbility('Poet', 5, 'Gain fame <font color="green">{{ (level+1) * 5 }}</font>% faster. Master this ability to unlock the Opportunist archetype.', learnable=True)
        self.Blackhearted = AuraAbility('Blackhearted', 3, 'Lose virtue {{ level * 5 }}% faster.', tree='archetype', tree_type='scoundrel')
        self.Backstab = AuraAbility('Backstab', 3, 'You are {{ level * 15 }}% more likely to attack first in combat.', tree='archetype', tree_type='scoundrel', firststrike_chance=15)
        self.MartialArts = AuraAbility('MartialArts', 3, 'You deal {{ level * 5 }}% more damage in combat.', tree='archetype', tree_type='ascetic')
        self.Apprentice = AuraAbility('Apprentice', 3, 'You are capable of learning level {{ level }} spells.', tree='archetype', tree_type='ascetic')
        self.Meditation = AuraAbility('Meditation', 3, 'Regenerate {{ level }} sanctity per day.', tree='archetype', tree_type='ascetic', sanctity_regeneration=1)
        self.Bash = AuraAbility('Bash', 3, 'You deal {{ level * 10 }}% more damage with blunt weapons.', tree='archetype', tree_type='brute')
        self.Student = AuraAbility('Student', 3, 'You are capable of learning level {{ level }} spells.', tree='archetype', tree_type='philosopher')
        self.Scholar = AuraAbility('Scholar', 3, 'Gain experience {{ level }}% faster.', learnable=True, tree='archetype', tree_type='philosopher', understanding_modifier=1)
        self.Vigilance = AuraAbility('Vigilance', 3, 'You are {{ level * 10 }}% less likely to be ambushed.', tree='archetype', tree_type='survivalist')
        self.Strider = AuraAbility('Strider', 3, 'Traveling on the map requires {{ level * 10 }}% less endurance.', tree='archetype', tree_type='survivalist')
        self.Skinner = AuraAbility('Skinner', 3, 'You have a {{ level * 5 }}% chance of obtaining a usable fur after kiling a beast.', tree='archetype', tree_type='survivalist')
        self.Charm = AuraAbility('Charm', 3, 'You are {{ level * 5 }}% more likely to succeed when choosing charm dialogues.', tree='archetype', tree_type='opportunist')
        self.Haggler = AuraAbility('Haggler', 3, 'Prices at shops are {{ level * 3}}% cheaper.', tree='archetype', tree_type='opportunist')

    def items(self):
        """Return each Ability and its name.

        Returns a list of 2-tuples
        Basically a dict.items() clone that looks like ([(key, value),
            (key, value), ...])

        Usage:
        for name, ability in abilities.items():
            name -- the name of the attribute
            ability -- the object that corresponds to the named attribute.
        """

        return ((key, getattr(self, key)) for key in ABILITY_NAMES)

    def __iter__(self):
        """Allow this object to be used in a for call.

        for ability in abilities:
            ability -- where the ability is each of the attribute objects of
                the abilities class.
        """
        return (getattr(self, key) for key in ABILITY_NAMES)


class Ability(Base):
    """Ability object base class.

    Relates to the Abilities class which is a meta list of all Abilities ...
    with maybe some extra functions to make it worth while? I guess so that
    you can call the items by name.

    How to use:
    name : Name of the Item, e.x. "power bracelet"
    buy_price : Price to buy the item
    level_req : level requirement
    """
    __tablename__ = "ability"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))  # Maybe 'unique' is not necessary?
    level = Column(Integer)
    max_level = Column(Integer)
    # Maybe description should be unique? use: unique=True as keyword.
    description = Column(String(200))
    cost = Column(String(50))

    # Note: Original code used default of "Unknown"
    # I chopped the BasicAbility class as redundant. Now I am going to
    # have to add the fucker back in.
    type = Column(String(50))
    ability_type = orm.synonym('type')

    # This determines if the ability is hidden and can not be learned or seen by the player
    hidden = Column(Boolean)
    learnable = Column(Boolean)

    # This decides which of the 4 types of abilities it is (default is basic)

    tree = Column(String(50))
    tree_type = Column(String(50))
    image = Column(String(50))

    # Relationships.
    # Ability to abilities. Abilities is a list of ability objects.
    abilities_id = Column(Integer, ForeignKey('abilities.id',
                                              ondelete="CASCADE"))
    abilities = relationship("Abilities")

    # Requirements is a One to Many relationship to self.
    """
    Use (pseudo-code):
    hero.can_learn(ability)
    if all hero.abilities are in ability.requirements.
    """
    # requirements = relationship("Ability")

    __mapper_args__ = {
        'polymorphic_identity': 'Basic',
        'polymorphic_on': type
    }

    def __init__(self, name, max_level, description, hero=None, hidden=True, learnable=False, tree="basic", tree_type="", cost=1):
        """Build a basic ability object.

        Note: arguments (name, hero, max_level, etc.) that require input are
        the same as setting nullable=False as a Column property.
        Note2: can't currently set 'level' attribute.
        Note3: Ability to Hero relationship is Many to Many. This will require
        some major restructuring.

        Future:
        add in 'toggleable'=True/False for abilities that can be turned on and
        off add in active=True/False for whether the ability is turned on or
        off right now.
        Or possibly extend the Ability class into a Spell Class and make a
        Toggleable Class that various Abilities could inherit from.
        """
        self.name = name
        self.level = 0
        self.max_level = max_level  # Highest level that this ability can get to
        self.description = description  # Describe what it does
        self.cost = cost
        if learnable == True:   # If the ability starts as a default of learnable, then it shouldn't start hidden to the player
            self.hidden = False
        else:
            self.hidden = hidden    # If the player can see it
        self.learnable = learnable  # If the player currently has the requirements to learn/upgrade it
        self.tree = tree    # Which research tree it belongs to (basic, archetype, class, religious)
        self.tree_type = tree_type  # Which specific tree (ie. if the tree is religious, then which religion is it)
        self.image = "ability_icon_" + self.name

        self.init_on_load()

        # On load ... not implemented.

    @orm.reconstructor
    def init_on_load(self):
        self.adjective = ["I", "II", "III", "IV", "V", "VI"]
        self.display_name = self.adjective[self.level - 1]
        self.learn_name = self.adjective[self.level]

    # @property
    # def display_name(self):
    #     return self.name.capitalize()

    def get_description(self):
        return render_template_string(self.description,
            level=self.level)

    def is_max_level(self):
        """Return True if level is at max_level."""
        return self.level >= self.max_level

    def update_stats(self, hero):
        hero.refresh_proficiencies()

    def activate(self, hero):
        return self.cast(hero)

    def update_display(self):
        self.display_name = self.adjective[self.level - 1]
        if self.level < self.max_level:
            self.learn_name = self.adjective[self.level]

    def update_owner(self, hero):
        print("Ability to Hero relationship is now Many to Many.")
        print("Instead of One Hero to Many Ablities.")
        exit("Removed in favor of add_hero and remove_hero")
        # self.heroes = [hero]


class CastableAbility(Ability):
    castable = Column(Boolean)
    sanctity_cost = Column(Integer)
    endurance_cost = Column(Integer)
    heal_amount = Column(Integer)
    gold_amount = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'CastableAbility',
    }

    def __init__(self, *args, sanctity_cost=0, endurance_cost=0, heal_amount=0, gold_amount=0, **kwargs):
        """Build a new ArchetypeAbility object.

        Note: self.type must be set in __init__ to polymorphic_identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        super().__init__(*args, **kwargs)
        self.castable = True
        self.sanctity_cost = sanctity_cost
        self.endurance_cost = endurance_cost
        self.heal_amount = heal_amount
        self.gold_amount = gold_amount

    def cast(self, hero):
        """Use the ability. Like casting a spell.

        use:
        ability.activate(hero)
        NOTE: returns False if spell is too expensive (cost > proficiencies.sanctity.current)
        If cast is succesful then return value is True.
        """
        if hero.proficiencies.sanctity.current < self.sanctity_cost or hero.proficiencies.endurance.current < self.endurance_cost:
            return False
        else:
            hero.proficiencies.sanctity.current -= self.sanctity_cost
            hero.proficiencies.endurance.current -= self.endurance_cost
            hero.proficiencies.health.current += self.heal_amount
            hero.gold += self.gold_amount
            return True


class AuraAbility(Ability):
    __mapper_args__ = {
        'polymorphic_identity': 'AuraAbility',
    }

    health_maximum = Column(Integer)
    sanctity_maximum = Column(Integer)
    damage_maximum = Column(Integer)
    damage_minimum = Column(Integer)
    understanding_modifier = Column(Integer)
    stealth_chance = Column(Integer)
    firststrike_chance = Column(Integer)

    def __init__(self, *args, health_maximum=0, sanctity_maximum=0, damage_maximum=0, damage_minimum=0, understanding_modifier=0, stealth_chance=0, sanctity_regeneration=0, firststrike_chance=0, **kwargs):
        """Build a new Archetype_Ability object.

        Note: self.type must be set in __init__ to polymorphic identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        super().__init__(*args, **kwargs)

        self.health_maximum = health_maximum
        self.sanctity_maximum = sanctity_maximum
        self.damage_maximum = damage_maximum
        self.damage_minimum = damage_minimum
        self.understanding_modifier = understanding_modifier
        self.stealth_chance = stealth_chance
        self.firststrike_chance = firststrike_chance

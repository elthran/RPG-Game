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

import proficiencies
# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base, attribute_mapped_dict_hybrid
import pdb

ALL_ABILITIES = {{ ALL_ABILITIES }}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Ability", "abilities", ALL_ABILITIES, no_container=True) }}

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
    current = Column(String(50))
    next = Column(String(50))
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

    # Relationships
    # Hero to self is one to one.
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="abilities")

    # Ability to Proficiencies is One to Many
    proficiencies = relationship(
        "Proficiency",
        collection_class=attribute_mapped_dict_hybrid('name'),
        back_populates='ability',
        cascade="all, delete-orphan")

    attrib_name = 'ability'
    adjective = ["I", "II", "III", "IV", "V", "VI"]

    @property
    def display_name(self):
        return self.adjective[self.level - 1]

    @property
    def learn_name(self):
        return self.adjective[self.level]

    # Requirements is a One to Many relationship to self.
    """
    Use (pseudo-code):
    hero.can_learn(ability)
    if all hero.abilities are in ability.requirements.
    """
    # ability_id = Column(Integer, ForeignKey('ability.id'))
    # requirements = relationship("Ability")

    __mapper_args__ = {
        'polymorphic_identity': 'Basic',
        'polymorphic_on': type
    }

    def __init__(self, name, max_level, description, current=0, next=0, hidden=True, learnable=False, tree="basic", tree_type="", cost=1, proficiency_data=()):
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
        self.current = current
        self.next = next
        self.cost = cost
        if learnable:   # If the ability starts as a default of learnable, then it shouldn't start hidden to the player
            self.hidden = False
        else:
            self.hidden = hidden    # If the player can see it
        self.learnable = learnable  # If the player currently has the requirements to learn/upgrade it
        self.tree = tree  # Which research tree it belongs to (basic, archetype, class, religious)
        self.tree_type = tree_type  # Which specific tree (ie. if the tree is religious, then which religion is it)
        self.image = "ability_icon_" + self.name

        # Initialize proficiencies
        # Currently doesn't add any proficiencies.
        for class_name, arg_dict in proficiency_data:
            Class = getattr(proficiencies, class_name)
            # pdb.set_trace()
            obj = Class(**arg_dict)
            self.proficiencies[obj.name] = obj

    # @property
    # def display_name(self):
    #     return self.name.capitalize()

    @orm.validates('level')
    def validate_level(self, key, current):
        """Set the base and modifier off the current level.

        x = 7
        for y in range(1, 10):
            x = (x // (y - 1 or 1)) * y (base)
            x = (x / (y - 1 or 1)) * y (modifier)

        NOTE: hero get_summed_proficiecies must check if level of Ability is 0
        """
        for prof in self.proficiencies:
            if current > 0:
                prof.base = (prof.base // (current-1 or 1)) * current
                prof.modifier = (prof.modifier // (current-1 or 1)) * current
        return current

    def get_description(self):
        return render_template_string(self.description)

    def get_current_bonus(self):
        return render_template_string(self.current, level=self.level)

    def get_next_bonus(self):
        return render_template_string(self.next, level=self.level)

    def is_max_level(self):
        """Return True if level is at max_level."""
        return self.level >= self.max_level

    def update_stats(self, hero):
        hero.refresh_proficiencies()

    def activate(self, hero):
        return self.cast(hero)

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
        if hero.get_summed_proficiencies('sanctity').current < self.sanctity_cost or hero.get_summed_proficiencies('endurance').current < self.endurance_cost:
            return False
        else:
            hero.base_proficiencies['sanctity'].current -= self.sanctity_cost
            hero.base_proficiencies['endurance'].current -= self.endurance_cost
            hero.base_proficiencies['health'].current += self.heal_amount
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

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """
        {% raw %}
        temp = """<h1>{{ ability.name }} (Level {{ ability.level }})</h1>
                      <h2>{{ ability.description }}</h2>
                      {% if ability.level %}<h3>Current Bonus:</h3> {{ ability.current }}{% endif %}
                      {% if not ability.is_max_level() %}<h3>Next Level Bonus:</h3> {{ ability.next }}{% else %}This ability is at its maximum level.{% endif %}
                      {% if not ability.is_max_level() %}
                      <button id=levelUpAbilityButton class="upgradeButton" onclick="sendToPy(event, abilityTooltip, 'update_ability', {'id': {{ ability.id }}});"></button>
                      {% endif %}"""
        {% endraw %}
        return render_template_string(temp, ability=self)


{% for value in ALL_ABILITIES %}
class {{ value[0] }}({{ value[1] }}):
    attrib_name = "{{ normalize_attrib_name(value[0]) }}"

    __mapper_args__ = {
        'polymorphic_identity': '{{ value[0] }}',
    }

    def __init__(self, *args, **kwargs):
        super().__init__('{{ value[0] }}', {{ value[2] }}, '{{ value[3] }}', current='{{ value[4] }}', next='{{ value[5] }}', learnable={{ value[6] }}, proficiency_data=[('{{ value[7] }}', {'base': {{ value[8] }}})])

        for key, value in kwargs:
            setattr(self, key, value)
{% if loop.last %}
{% else %}


{% endif %}
{% endfor %}

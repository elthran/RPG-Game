# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
#  Author: Elthran B, Jimmy Zhang                                             #
#  Email : jimmy.gnahz@gmail.com                                              #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

import sqlalchemy as sa
import sqlalchemy.orm
import flask

import models

ALL_ABILITIES = {{ ALL_ABILITIES }}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Ability", "abilities", ALL_ABILITIES, no_container=True) }}

class Ability(models.Base):
    """Ability object base class.

    Relates to the Abilities class which is a meta list of all Abilities ...
    with maybe some extra functions to make it worth while? I guess so that
    you can call the items by name.

    How to use:
    name : Name of the Item, e.x. "power bracelet"
    buy_price : Price to buy the item
    level_req : level requirement
    """
    name = sa.Column(sa.String(50))  # Maybe 'unique' is not necessary?
    level = sa.Column(sa.Integer)
    max_level = sa.Column(sa.Integer)
    # Maybe description should be unique? use: unique=True as keyword.
    description = sa.Column(sa.String(200))
    castable = sa.Column(sa.Boolean)
    _current = sa.Column(sa.String(50))
    _next = sa.Column(sa.String(50))
    sanctity_cost = sa.Column(sa.Integer)
    endurance_cost = sa.Column(sa.Integer)

    # Note: Original code used default of "Unknown"
    # I chopped the BasicAbility class as redundant. Now I am going to
    # have to add the fucker back in.
    type_ = sa.Column(sa.String(50))
    ability_type = sa.orm.synonym('type')

    # This determines if the ability is hidden and can not be learned or seen by the player
    hidden = sa.Column(sa.Boolean)
    learnable = sa.Column(sa.Boolean)

    # This decides which of the 4 types of abilities it is (default is basic)

    tree = sa.Column(sa.String(50))
    tree_type = sa.Column(sa.String(50))
    image = sa.Column(sa.String(50))

    # Relationships
    # Hero to self is one to one.
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship("Hero", back_populates="abilities")

    # Ability to Proficiencies is One to Many
    proficiencies = sa.orm.relationship(
        "Proficiency",
        collection_class=models.attribute_mapped_dict_hybrid('name'),
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

    @property
    def current(self):
        return flask.render_template_string(self._current, level=self.level)

    @property
    def next(self):
        return flask.render_template_string(self._next, level=self.level)

    # Requirements is a One to Many relationship to self.
    """
    Use (pseudo-code):
    hero.can_learn(ability)
    if all hero.abilities are in ability.requirements.
    """
    # ability_id = sa.Column(sa.Integer, ForeignKey('ability.id'))
    # requirements = relationship("Ability")

    __mapper_args__ = {
        'polymorphic_identity': 'Basic',
        'polymorphic_on': type_
    }

    def __init__(self, name, max_level, description, spell_thing="", current=0, next_=0, hidden=True, learnable=False, tree="basic", tree_type="", proficiency_data=(), spell_data=(), sanctity_cost=0, endurance_cost=0):
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
        self.castable = False
        self._current = current
        self._next = next_
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
        for class_name_, arg_dict in proficiency_data:
            class_ = getattr(models.proficiencies, class_name_)
            # pdb.set_trace()
            obj = class_(**arg_dict)
            self.proficiencies[obj.name] = obj

        # Jacob did this. I need some help setting it up. This should be for casting spells.
        for class_name_, arg_dict in spell_data:
            class_ = getattr(models.proficiencies, class_name_)
            # pdb.set_trace()
            obj = class_(**arg_dict)
            self.proficiencies[obj.name] = obj

        # These and the one above should only be in castable.
        self.sanctity_cost = sanctity_cost
        self.endurance_cost = endurance_cost

    # @property
    # def display_name(self):
    #     return self.name.capitalize()

    @sa.orm.validates('level')
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
        return flask.render_template_string(self.description)

    def get_current_bonus(self):
        return flask.render_template_string(self.current, level=self.level)

    def get_next_bonus(self):
        return flask.render_template_string(self._next, level=self.level)

    def is_max_level(self):
        """Return True if level is at max_level."""
        return self.level >= self.max_level

    def update_stats(self, hero):
        pass
        # hero.refresh_proficiencies()

    def activate(self, hero):
        return self.cast(hero)

    def update_owner(self, hero):
        print("Ability to Hero relationship is now Many to Many.")
        print("Instead of One Hero to Many Ablities.")
        exit("Removed in favor of add_hero and remove_hero")
        # self.heroes = [hero]


class CastableAbility(Ability):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'CastableAbility',
    }

    def __init__(self, *args, **kwargs):
        """Build a new ArchetypeAbility object.

        Note: self.type must be set in __init__ to polymorphic_identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        super().__init__(*args, **kwargs)
        self.castable = True

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """
        {% raw %}
        temp = """<h1>{{ ability.name }} (Level {{ ability.level }})</h1>
                      <h2>{{ ability.description }}</h2>
                      {% if ability.level %}<h3>Current: {{ ability.current }}</h3>{% endif %}
                      {% if not ability.is_max_level() %}<h3>Next: {{ ability.next }}</h3>{% else %}<h3>This ability is at its maximum level.</h3>{% endif %}
                      {% if not ability.is_max_level() and ((ability.tree == "Basic" and ability.hero.basic_ability_points) or (ability.tree == "Archetype" and ability.hero.archetype_ability_points))%}
                      <button id=levelUpAbilityButton class="upgradeButton" onclick="sendToPy(event, abilityTooltip, 'update_ability', {'id': {{ ability.id }}});"></button>
                      {% endif %}"""
        {% endraw %}
        return flask.render_template_string(temp, ability=self)

    def cast(self, hero):
        """Use the ability. Like casting a spell.

        use:
        ability.activate(hero)
        NOTE: returns False if spell is too expensive (cost > proficiencies.sanctity.current)
        If cast is succesful then return value is True.
        """
        if hero.base_proficiencies['sanctity'].current < self.sanctity_cost:
            print("Trying to cast a spell but you have not enough sanctity.")
            return "error: not enough sanctity"
        if hero.base_proficiencies['endurance'].current < self.endurance_cost:
            print("Trying to cast a spell but you have not enough endurance.")
            return "error: not enough endurance"
        hero.base_proficiencies['sanctity'].current -= self.sanctity_cost
        hero.base_proficiencies['endurance'].current -= self.endurance_cost
        return "success"


class AuraAbility(Ability):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'AuraAbility',
    }

    def __init__(self, *args, **kwargs):
        """Build a new Archetype_Ability object.

        Note: self.type must be set in __init__ to polymorphic identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        super().__init__(*args, **kwargs)

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """
        {% raw %}
        temp = """<h1>{{ ability.name }} (Level {{ ability.level }})</h1>
                      <h2>{{ ability.description }}</h2>
                      {% if ability.level %}<h3>Current: {{ ability.current }}</h3>{% endif %}
                      {% if not ability.is_max_level() %}<h3>Next: {{ ability.next }}</h3>{% else %}<h3>This ability is at its maximum level.</h3>{% endif %}
                      {% if not ability.is_max_level() and ((ability.tree == "Basic" and ability.hero.basic_ability_points) or (ability.tree == "Archetype" and ability.hero.archetype_ability_points))%}
                      <button id=levelUpAbilityButton class="upgradeButton" onclick="sendToPy(event, abilityTooltip, 'update_ability', {'id': {{ ability.id }}});"></button>
                      {% endif %}"""
        {% endraw %}
        return flask.render_template_string(temp, ability=self)


{% for value in ALL_ABILITIES %}
{% set class_name = normalize_class_name(value[0]) %}
class {{ class_name }}({{ value[1] }}):
    attrib_name = "{{ normalize_attrib_name(value[0]) }}"
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': '{{ value[0] }}',
    }

    def __init__(self, *args, **kwargs):
        {% if value[1] == 'AuraAbility' %}
        super().__init__(name='{{ value[0] }}', tree='{{ value[2] }}', tree_type='{{ value[3] }}', max_level={{ value[4] }}, description='{{ value[5] }}', current='{{ value[6] }}', next_='{{ value[6] }}'.replace("(level)", "(level+1)"), learnable={{ value[7] }}, proficiency_data=[('{{ value[8] }}', {'base': {{ value[9] }}}), {% if value[10] != 'Null' %}('{{ value[10] }}', {'base': {{ value[11] }}}){% endif %}])
        {% elif value[1] == 'CastableAbility' %}
        super().__init__(name='{{ value[0] }}', tree='{{ value[2] }}', tree_type='{{ value[3] }}', max_level={{ value[4] }}, description='{{ value[5] }}', current='{{ value[6] }}', next_=next, learnable={{ value[7] }}, proficiency_data=[], spell_data=[('{{ value[8] }}', {'base': {{ value[9] }}}), ('{{ value[10] }}', {'base': {{ value[11] }}})], sanctity_cost={{ value[12] }}, endurance_cost={{ value[13] }})
        {% endif %}
        for key, value in kwargs:
            setattr(self, key, value)
{% if loop.last %}
{% else %}


{% endif %}
{% endfor %}

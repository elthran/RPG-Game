import sqlalchemy as sa
import sqlalchemy.orm
import flask

import models

# For testing


ALL_PROFICIENCIES = {{ ALL_PROFICIENCIES }}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Proficiency", "proficiencies", ALL_PROFICIENCIES, no_container=True) }}

class Proficiency(models.mixins.TemplateMixin, models.Base):
    """Proficiency class that stores data about a hero object.
    """
    # Relationships
    # Hero to Proficiencies is One to many?
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship("Hero", back_populates="base_proficiencies")

    # Proficiency to Ability is One to Many
    ability_id = sa.Column(sa.Integer, sa.ForeignKey('ability.id', ondelete="CASCADE"))
    ability = sa.orm.relationship("Ability", back_populates="proficiencies")

    # Proficiency to Item is One to Many
    item_id = sa.Column(sa.Integer, sa.ForeignKey('item.id', ondelete="CASCADE"))
    items = sa.orm.relationship("Item", back_populates="proficiencies")

    # Main colums
    level = sa.Column(sa.Integer)
    base = sa.Column(sa.Float)
    modifier = sa.Column(sa.Float)

    type_ = sa.Column(sa.String(50))
    attribute_type = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))
    # tooltip = sa.Column(sa.String(50))
    reason_for_zero = sa.Column(sa.String(50))    # Maybe remove
    current = sa.Column(sa.Integer)
    hidden = sa.Column(sa.Boolean)
    error = sa.Column(sa.String(50))
    display_chunk = sa.Column(sa.String(200))

    # In child classes this allows different levels of rounding.
    num_of_decimals = 0
    # In the child classes this allows nice output formatting
    format_spec = '{:.2f}'
    name = "proficiency"

    __mapper_args__ = {
        'polymorphic_identity': "Proficiency",
        'polymorphic_on': type_
    }

    def __init__(self, level=0, base=0, modifier=0, template=False):
        self.type_ = self.__class__.__name__
        # self.tooltip = ""
        self.level = level
        self.base = base
        self.modifier = modifier
        self.template = template
        self.current = self.final

    def clone(self):
        if not self.template:
            raise Exception("Only use this method if obj.template == True.")
        return self.__class__(level=self.level, base=self.base,
                              modifier=self.modifier, template=False)

    def level_up(self):
        self.level += 1
        self.current = self.hero.get_summed_proficiencies(self.name).final

    def scale_by_level(self, level=None):
        """Return some function of the level attribute.

        This is different for each proficiency.
        Options are:

        "root:
        return round((100 * self.level)**0.5 - (self.level / 4), precision)
        "linear"
        return round(value1 * self.level, precision)
        "empty"
        return self.level  # Defaults to 0

        NOTE: base value has now been moved to the final function
        """

        # Allows you to determine the value at the next level without
        # modifying self.level (which might have unintended consequences).
        if level is None:
            level = self.level
        return level

    @property
    def next_value(self):
        """Return the value this proficiency will have if it is updated."""
        return round((self.scale_by_level(level=self.level+1) + self.base) *
                     ((self.modifier + 100) / 100), self.num_of_decimals)

    @property
    def final(self):
        """Return the scaled value + base + modifier percent."""
        return round((self.scale_by_level() + self.base) *
                     ((self.modifier + 100) / 100), self.num_of_decimals)

    @property
    def percent(self):
        """Return the percent of the current to the final value."""
        try:
            return round(self.current / self.final, 2) * 100
        except ZeroDivisionError:
            return 0

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """
        {% raw %}
        temp = """<h1>{{ prof.display_name }} (Level {{ prof.level }})</h1>
                  <h2>{{ prof.description }}</h2>
                  <h2>Current value: {{ formatted_final }}</h2>
                  {% if not prof.is_max_level and prof.hero.proficiency_points %}
                  <h2>Next value: <font color="green">{{ formatted_next }}</font></h2>
                  <button id=levelUpProficiencyButton class="upgradeButton" onclick="sendToPy(event, proficiencyTooltip, 'update_proficiency', {'id': {{ prof.id }}});"></button>
                  {% elif prof.is_max_level %}<font color="red">Not enough {{ prof.attribute_type }}</font>{% endif %}</h2>"""
        {% endraw %}
        return flask.render_template_string(
            temp, prof=self,
            formatted_final=self.format_spec.format(self.final),
            formatted_next=self.format_spec.format(self.next_value))

    @property
    def attribute(self):
        return None

    @property
    def max_level(self):
        return self.attribute.level * 2

    @property
    def is_max_level(self):
        """Cap the proficiency level at double the attribute level."""
        return True if self.level >= self.attribute.level * 2 else False


{% for prof in ALL_PROFICIENCIES %}
{% set prof_class = normalize_class_name(prof[0]) %}
{% set attrib_name = normalize_attrib_name(prof[0]) %}
{% set display_name = prof[0].capitalize() %}
{% set growth = prof[3] %}
{% set base = prof[4] %}
{% set weight = prof[5] %}
{% set decimals = prof[6] %}
{% if prof[7] == "TRUE" %}{% set hidden = True %}{% else %}{% set hidden = False %}{% endif %}
{% set percent = prof[8] %}
{% set display_chunk = prof[9] %}
class {{ prof_class }}(Proficiency):
    # If this is true, then the proficiency should not show up on the
    # prof page and should only be modifiable by items/abilities.
    hidden = {{ hidden }}
    name = "{{attrib_name}}"
    display_name = "{{ display_name.title() }}"
    num_of_decimals = {{ decimals }}
    # This should add a "%" to the display at the end of a prof.
    is_percent = {{ percent }}  # Should be {{ percent }} but I'm getting an error
    format_spec = "{{ '{' }}:.{{ decimals }}f{{ '}' }}{{ '%' if percent else '' }}"
    display_chunk = "{{ display_chunk }}"

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': "{{ prof_class }}"
    }

    {% if prof[2] %}
    # Proficiency to Attribute is many to one.
    @property
    def attribute(self):
        return self.hero.attributes.{{ normalize_attrib_name(prof[2]) }}

    {% endif %}
    def __init__(self, *args, base={{ base }}, **kwargs):
        super().__init__(*args, base=base, **kwargs)
        self.description = "{{ prof[1]}}"
        self.attribute_type = {{ '"' + prof[2] + '"' if prof[2] else None }}
        self.error = "You do not have enough {}".format(self.attribute_type)

    def scale_by_level(self, level=None):
        """Update {{ prof_class }}'s attributes and tooltip variable.
        """

        # Allows you to determine the value at the next level without
        # modifying self.level (which might have unintended consequences).
        if level is None:
            level = self.level

    {% if growth == "root" %}
        return round((100 * level)**0.5 - (level / 4), self.num_of_decimals)
    {% elif growth == "linear" %}
        return round({{ weight }} * level, self.num_of_decimals)
    {% elif growth == "empty" %}
        return super().scale_by_level()
    {% endif %}
    {% if prof[0] == "Block" %}

    def check_shield(self, hero):
        if hero.inventory.left_hand is None or hero.inventory.left_hand.type != "Shield":
            self.current = 0
            self.reason_for_zero = "You must have a shield equipped"
        else:
            self.reason_for_zero = ""
    {% endif %}


{% endfor %}

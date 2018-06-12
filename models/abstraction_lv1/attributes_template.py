import sqlalchemy as sa
import sqlalchemy.orm

import models

ALL_ATTRIBUTES = {{ ALL_ATTRIBUTES }}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Attribute", "attributes", ALL_ATTRIBUTES, no_container=True) }}

class Attribute(models.Base):
    """Attribute class that stores data about a hero object.
    """
    type_ = sa.Column(sa.String(50))
    name = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))
    level = sa.Column(sa.Integer)

    # Relationships
    # Hero to self is one to one.
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship("Hero", back_populates="attributes")

    attrib_name = 'attribute'

    __mapper_args__ = {
        'polymorphic_identity': 'Attribute',
        'polymorphic_on': type_
    }
    
    def __init__(self, name, description):
        """Build the initial Attribute object.
        
        Set all values to 1.
        """
        
        self.name = name
        self.description = description
        self.level = 1


{% for attrib in ALL_ATTRIBUTES %}
class {{ attrib[0] }}(Attribute):
    attrib_name = "{{ normalize_attrib_name(attrib[0]) }}"

    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': '{{ attrib[0] }}',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("{{ attrib[0] }}", "{{ attrib[1] }}")

        for key, value in kwargs:
            setattr(self, key, value)
{% if loop.last %}
{% else %}


{% endif %}
{% endfor %}

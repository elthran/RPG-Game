from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models.base_classes import Base

ALL_ATTRIBUTES = {{ ALL_ATTRIBUTES }}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Attribute", "attributes", ALL_ATTRIBUTES, no_container=True) }}

class Attribute(Base):
    """Attribute class that stores data about a hero object.
    """
    __tablename__ = "attribute"
    
    id = Column(Integer, primary_key=True)

    type_ = Column(String(50))
    name = Column(String(50))
    description = Column(String(200))
    level = Column(Integer)

    # Relationships
    # Hero to self is one to one.
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="attributes")

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

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base

{% include "attributes_data.py" %}

{% import 'container_helpers.py' as container_helpers %}
{{ container_helpers.build_container("Attribute", "attributes", ATTRIBUTE_INFORMATION) }}
        
class Attribute(Base):
    """Attribute class that stores data about a hero object.
    """
    __tablename__ = "attribute"
    
    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    description = Column(String(200))
    level = Column(Integer)

    # Relationships
    # Ability to abilities. Abilities is a list of ability objects.
    attribute_container_id = Column(
        Integer, ForeignKey('attribute_container.id', ondelete="CASCADE"))

    __mapper_args__ = {
        'polymorphic_identity': 'Attribute',
        'polymorphic_on': name
    }
    
    def __init__(self, name, description):
        """Build the initial Attribute object.
        
        Set all values to 1.
        """
        
        self.name = name
        self.description = description
        self.level = 1


{% for attrib in ATTRIBUTE_INFORMATION %}
class {{ attrib[0] }}(Attribute):
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

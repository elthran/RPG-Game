{% include "attributes_data.py" %}

class Attributes(Base):
    __tablename__ = 'attributes'
    
    id = Column(Integer, primary_key=True)                     

    {% for attrib in ATTRIBUTE_INFORMATION %}
    {{ attrib[0].lower() }} = relationship("Attribute", uselist=False, back_populates="attributes")
    {%- endfor %}
    
   
    def __init__(self, hero):
        {% for attrib in ATTRIBUTE_INFORMATION %}
        self.{{ attrib[0].lower() }} = Attribute("{{ attrib[0] }}", "{{ attrib[1] }}")
        {%- endfor %}

        
class Attribute(Base):
    """Attribute class that stores data about a hero object.
    """
    __tablename__ = "attribute"
    
    id = Column(Integer, primary_key=True)
    
    attributes_id = Column(Integer, ForeignKey('attributes.id'))
    attributes = relationship("Attributes", back_populates="attribute")
   
    name = Column(String)
    description = Column(String)
    level = Column(Integer)
    
    def __init__(self, name, description):
        """Build the initial Attribute object.
        
        Set all values to 1.
        """
        
        self.name = name
        self.description = description
        self.value = 1

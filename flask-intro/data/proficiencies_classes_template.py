{% for name in ALL_PROFICIENCIES %}        
class {{ name.title().replace("_", '') }}(Proficiency):
    id = Column(Integer, ForeignKey("proficiency.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':"{{ name.title().replace("_", '') }}",
    }
    
    def update(self):   
{%- endfor %}

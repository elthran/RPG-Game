ATTRIBUTE_INFORMATION = [
    ("Agility", "A measure of how agile a character is. Dexterity controls attack and movement speed and accuracy, as well as evading an opponent's attack ."),
    ("Charisma", "A measure of a character's social skills, and sometimes their physical appearance."),
    ("Divinity", "A measure of a character's common sense and/or spirituality."),
    ("Fortitude", "A measure of how resilient a character is."),
    ("Fortuity", "A measure of a character's luck. "),
    ("Perception", "A measure of a character's openness to their surroundings."),
    ("Reflexes", "A measure of how agile a character is. "),
    ("Resilience", "A measure of how resilient a character is. "),
    ("Strength", "A measure of how physically strong a character is. "),
    ("Survivalism", "A measure of a character's openness to their surroundings. "),
    ("Vitality", "A measure of how sturdy a character is."),
    ("Wisdom", "A measure of a character's problem-solving ability.")
]

class Attributes(Base):
    __tablename__ = 'attributes'
    
    id = Column(Integer, primary_key=True)                     

    
    agility = relationship("Attribute", uselist=False, back_populates="attributes")
    charisma = relationship("Attribute", uselist=False, back_populates="attributes")
    divinity = relationship("Attribute", uselist=False, back_populates="attributes")
    fortitude = relationship("Attribute", uselist=False, back_populates="attributes")
    fortuity = relationship("Attribute", uselist=False, back_populates="attributes")
    perception = relationship("Attribute", uselist=False, back_populates="attributes")
    reflexes = relationship("Attribute", uselist=False, back_populates="attributes")
    resilience = relationship("Attribute", uselist=False, back_populates="attributes")
    strength = relationship("Attribute", uselist=False, back_populates="attributes")
    survivalism = relationship("Attribute", uselist=False, back_populates="attributes")
    vitality = relationship("Attribute", uselist=False, back_populates="attributes")
    wisdom = relationship("Attribute", uselist=False, back_populates="attributes")
    
   
    def __init__(self, hero):
        
        self.agility = Attribute("Agility", "A measure of how agile a character is. Dexterity controls attack and movement speed and accuracy, as well as evading an opponent's attack .")
        self.charisma = Attribute("Charisma", "A measure of a character's social skills, and sometimes their physical appearance.")
        self.divinity = Attribute("Divinity", "A measure of a character's common sense and/or spirituality.")
        self.fortitude = Attribute("Fortitude", "A measure of how resilient a character is.")
        self.fortuity = Attribute("Fortuity", "A measure of a character's luck. ")
        self.perception = Attribute("Perception", "A measure of a character's openness to their surroundings.")
        self.reflexes = Attribute("Reflexes", "A measure of how agile a character is. ")
        self.resilience = Attribute("Resilience", "A measure of how resilient a character is. ")
        self.strength = Attribute("Strength", "A measure of how physically strong a character is. ")
        self.survivalism = Attribute("Survivalism", "A measure of a character's openness to their surroundings. ")
        self.vitality = Attribute("Vitality", "A measure of how sturdy a character is.")
        self.wisdom = Attribute("Wisdom", "A measure of a character's problem-solving ability.")

        
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
#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

try:
    from sqlalchemy import Column, Integer, String, Boolean
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy import orm
except ImportError as e:
    exit("Open a command prompt and type: pip install sqlalchemy."), e
    
#!Important!: Base can only be defined in ONE location and ONE location ONLY!
#Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base
    
# exit('********Ability: inheritance not implemented********')

class Ability(Base):
    """Ability object base class.
    
    A list of all abilities, the relationship to the Hero class is many to many.
    Each hero can have many abilities and each abilities can be assigned multiple heros.
    I think this is a good idea?
    
    How to use:
    name : Name of the Item, e.x. "power bracelet"
    hero : The Hero who owns the item
	buy_price : Price to buy the item
	level_req : level requirment
    """
    __tablename__ = "abilities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    level = Column(Integer, default=1)
    max_level = Column(Integer, nullable=False)
    description = Column(String, nullable=False) #Maybe description should be unique? use: unique=True as keyword.
    
    #Note: Original code used default of "Unknown"
    #I chopped the BasicAbility class as redundant. Now I am going to have to add the fucker back in.
    ability_type = Column(String, default="basic") 
    activated = Column(Boolean, default=False)
    cost = Column(Integer, default=0)
    
    
    def __init__(self, name, myHero, max_level, description, activated=False, cost=0):
        self.name = name
        self.myHero = myHero #I will remove this and make a default as None or something?
        self.level = 1
        self.max_level = max_level
        self.description = description
        self.ability_type = "Unknown"
        self.activated = activated
        self.cost = cost
        
        # External table ... not implemented.
        self.requirements = []
        
        # On load ... not implemented.
        self.adjective = ["I","II","III","IV", "V", "VI"]
        self.display_name = self.adjective[self.level - 1]
        self.learn_name = self.adjective[self.level]

    def update_stats(self):
        if self.name == "Determination":
            self.myHero.max_endurance += 3 * self.level
        if self.name == "Salubrity":
            self.myHero.max_health += 4 * self.level

    def activate(self):
        if self.myHero.current_sanctity < self.cost:
            return
        else:
            self.myHero.current_sanctity -= self.cost
        if self.name == "Gain Gold to Test":
            self.myHero.gold += 3 * self.level

    def update_display(self):
        self.display_name = self.adjective[self.level - 1]
        if self.level < self.max_level:
            self.learn_name = self.adjective[self.level]

    def update_owner(self, myHero):
        self.myHero = myHero
        
    
    def __repr__(self): 
        """Return string data about Ability object.
        """
        atts = []
        column_headers = self.__table__.columns.keys()
        extra_attributes = [key for key in vars(self).keys() if key not in column_headers]
        for key in column_headers:
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
            
        for key in sorted(extra_attributes):
            atts.append('{}={}'.format(key, repr(getattr(self, key))))
        
        data = "<Ability(" + ', '.join(atts) + ')>'
        return data
        

class Archetype_Ability(Ability):
    def __init__(self, *args, archetype="All", **kwargs):
        super().__init__(*args, **kwargs)
        self.ability_type = "archetype"
        self.archetype = archetype

class Class_Ability(Ability):
    def __init__(self, *args, specialization="All", **kwargs):
        super().__init__(*args, **kwargs)
        self.ability_type = "class"
        self.specialization = specialization

class Religious_Ability(Ability):
    def __init__(self, *args, religion="All", **kwargs):
        super().__init__(*args, **kwargs)
        self.ability_type = "religious"
        self.religion = religion


# all_abilities = [Ability("Determination", "Null", 5, "Increases Endurance by 3 for each level."),
                 # Ability("Salubrity", "Null", 5, "Increases Health by 4 for each level."),
                 # Ability("Gain Gold to Test", "Null", 5, "Gain 3 gold for each level, every time you actvate this ability.", activated=True, cost=2),
                 # Archetype_Ability("Survivalism", "Null", 10, "Increases survivalism by 1 for each level.", "Woodsman"),
                 # Archetype_Ability("Piety", "Null", 10, "Increases divinity by 1 for each level.", "Priest"),
                 # Archetype_Ability("Sagacious", "Null", 10, "Increases experience gained by 5% for each level."),
                 # Class_Ability("Panther Aspect", "Null", 10, "Increases evade chance by 1% for each level.", "Hunter"),
                 # Class_Ability("Camouflage", "Null", 10, "Increases stealth by 1% for each level.", "Trapper"),
                 # Class_Ability("Luck", "Null", 10, "Increases luck by 2 for each level."),
                 # Religious_Ability("Iron Bark", "Null", 10, "Increases defence by 2% for each level.", "Dryarch"),
                 # Religious_Ability("Wreath of Flames", "Null", 10, "Increases fire damage by 3 for each level.", "Forgoth"),
                 # Religious_Ability("Blessed", "Null", 10, "Increases devotion by 5 for each level.")]

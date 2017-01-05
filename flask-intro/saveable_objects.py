"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship
except ImportError:
    exit("Open a command prompt and type: pip install sqlalchemy.")

import hashlib
import os #Testing only

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
    
    heroes = relationship("Hero", order_by='Hero.id', back_populates='user')

    def __repr__(self):
       return "<User(username='{}', password='{}', email='{}')>" .format(
                        self.username, self.password, self.email)
          

class Hero(Base):
    __tablename__ = 'heroes'
    
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    age = Column(Integer, default=7)
    archetype = Column(String, default="Woodsman")
    specialization = Column(String, default="Hunter")
    religion = Column(String, default="Dryarch")
    house = Column(String, default="Unknown")
    current_exp = Column(Integer, default=0)
    max_exp = Column(Integer, default=10)
    renown = Column(Integer, default=0)
    virtue = Column(Integer, default=0)
    devotion = Column(Integer, default=0)
    gold = Column(Integer, default=50)
    
    ability_points= Column(Integer, default=3) #TEMP. Soon will use the 4 values below
    basic_ability_points = Column(Integer, default=0)
    archetype_ability_points = Column(Integer, default=0)
    specialization_ability_points = Column(Integer, default=0)
    pantheonic_ability_points = Column(Integer, default=0)
    
    attribute_points = Column(Integer, default=0)
        
    current_sanctity = Column(Integer, default=0)
    current_health = Column(Integer, default=0)
    current_endurance = Column(Integer, default=0)
    current_carrying_capacity = Column(Integer, default=0)
    max_health = Column(Integer, default=0)
    
    #Not yet implemented
    # self.primary_attributes = {"Strength": 1, "Resilience": 1, "Vitality": 1, "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1, "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1}
    # self.strength = 1
    # self.resilience = 1
    # self.vitality = 1
    # self.fortitude = 1
    # self.reflexes = 1
    # self.agility = 1
    # self.perception = 1
    # self.wisdom = 1
    # self.divinity = 1
    # self.charisma = 1
    # self.survivalism = 1
    # self.fortuity = 1
    # self.equipped_items = []
    # self.inventory = []
    # self.abilities = []
    # self.chest_equipped = []

    # self.errands = []
    # self.current_quests = []
    # self.completed_quests = []
    # self.completed_achievements = []
    # self.kill_quests = {}
    # self.bestiary = []

    # self.known_locations = []
    # self.current_world = None #Type?
    # self.current_city = None #Type?

    # self.wolf_kills = 0
    # self.update_secondary_attributes() #Use @reconstructor decorator from sqlalchemy.orm
    #End of not yet implemented
    
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="heroes")

    def __repr__(self): 
        atts = []
        for key in self.__table__.columns.keys():
            atts.append('{}={}'.format(key, getattr(self, key)))
        
        data = "<Hero(" + ', '.join(atts) + ')>'
        return data 
                        

class EZDB:
    def __init__(self, database='sqlite:///:memory:', debug=True):
        engine = create_engine(database, echo=debug)
        self.file_name = database[10:]
        
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        
        self.engine = engine
        self.session = Session()
        
        
    def get_user_id(self, username):
        """Return the id of the user by username from the User's table.
        
        """
        return self.session.query(User).filter_by(username=username).first().id
    
    
    def add_new_user(self, username, password, email=''):
        """Add a user to the username with a given a unique username and a password.
        
        The password is hashed.
        """
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        self.session.add(User(username=username, password=hashed_password, email=email))
        self.session.commit()
        
    def add_new_character(self, username_or_id, character_name=None, archetype=None):
        """Add a character with the specified archetype to a given user by id or username.
        
        Username is a unique field and is more human readable then using id's.
        """
        
        user = None
        if isinstance(username_or_id, int):
            user = self.session.query(User).filter_by(id=username_or_id).first()
        else:
            user = self.session.query(User).filter_by(username=username_or_id).first()
        self.session.add(Hero(character_name=character_name, archetype=archetype, user=user))
        self.session.commit()
    
    def validate(self, username, password):
        """Check if password if valid for user.
        """
        hashed_password = self.session.query(User).filter_by(username=username).first().password
        return  hashed_password == hashlib.md5(password.encode()).hexdigest()
        
    def fetch_hero(self, username_or_id=None, character_name_or_id=None):
        """Return live hero objected based on username_or_id and character_name.
        
        If no character_name is passed just return first hero.
        Note: Providing a username when you have the hero/character id is redundant.
        """

        if character_name_or_id and isinstance(character_name_or_id, int):
            if username_or_id:
                exit("Providing a username when you have the hero/character id is redundant.")
            return self.session.query(Hero).filter_by(id=character_name_or_id).first()
           
        if isinstance(username_or_id, str):
            username_or_id = self.get_user_id(username_or_id)
        
        if character_name_or_id:
            return self.session.query(Hero).filter_by(user_id=username_or_id, character_name=character_name_or_id).first()
        return self.session.query(User).filter_by(id=username_or_id).first().heroes[0]
                   
    
    def update(self):
        """Commit current session.
        
        NOTE: update function is now mostly redundant! Only use on program exit or logout.
        When you edit the hero ... he stayes edited! Using any of the other methods will push him to database.
        """
        self.session.commit()
    
    def update_time(id):
        """Currently updates the time of a specific hero.
        
        Perhaps it should update all heros?
        """
        exit(*****writeme!*******)
        
    
    def _delete_database(self):
        """Deletes current database file.
        
        Use with caution, mainly for testing.
        """
        os.remove(self.file_name)
        
def pr(*args):
    return print(args[0], repr(args[-1]))                    
                        
if __name__ == "__main__":

    """Methods to replicated:
    update_time
    check_password
    validate
    add_new_user - Done!
    get_user_id - Done!
    add_new_character
    update_character
    fetch_character_data
    """
    # ezdb = EZDB()
    
    # print('###################')
    # username = 'marlen'
    # password = 'brunner'
    # ezdb.add_new_user(username, password)
    # id = ezdb.get_user_id(username)
    # pr('ID:', id)
    # pr(m_user.username)
    # session.add(m_user)
    
    
    # our_user = EzDB.get_user_by_username(session, 'marlen')
    # print(our_user.username)
    # print(m_user is our_user)
    
    
    
    

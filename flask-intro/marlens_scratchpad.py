from base_classes import Base, BaseDict
from secondary_attributes import *

class Hero(object):
    class_attribute = 0
    
    def __init__(self, user_id=0):
        """Make a new Hero object.
        NOTE: user_id of zero is nobody ever. The minimum user_id is 1. :)
        """
        self.user_id = user_id
        self.name = "Admin"
        self.age = 7
        self.archetype = "Woodsman"
        self.specialization = "Hunter"
        self.religion = "Dryarch"
        self.house = "Unknown"
        self.current_exp = 0
        self.max_exp = 10
        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        self.ability_points = 3 #TEMP. Soon will use the 4 values below
        self.basic_ability_points = 0
        self.archetype_ability_points = 0
        self.specialization_ability_points = 0
        self.pantheonic_ability_points = 0

        self.attribute_points = 0
        self.primary_attributes = {"Strength": 1, "Resilience": 1, "Vitality": 1, "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1, "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1}
        self.current_sanctity = 0
        self.current_health = 0
        self.current_endurance = 0
        self.current_carrying_capacity = 0
        self.max_health = 0
		
        self.equipped_items = []
        self.inventory = []
        self.abilities = []
        self.chest_equipped = []

        self.errands = []
        self.current_quests = []
        self.completed_quests = []
        self.completed_achievements = []
        self.kill_quests = {}
        self.bestiary = []

        self.known_locations = []
        self.current_world = None
        self.current_city = None
        
        self.wolf_kills = 0
        self.update_secondary_attributes()

    # Sets damage
    def update_secondary_attributes(self):
        self.maximum_damage = update_maximum_damage(self)
        self.minimum_damage = update_minimum_damage(self)
        self.attack_speed = update_attack_speed(self)
        self.attack_accuracy = update_attack_accuracy(self)
        self.first_strike = update_first_strike_chance(self)
        self.critical_hit_chance = update_critical_hit_chance(self)
        self.critical_hit_modifier = update_critical_hit_modifier(self)
        self.defence_modifier = update_defence_modifier(self)
        self.evade_chance = update_evade_chance(self)
        self.parry_chance = update_parry_chance(self)
        self.riposte_chance = update_riposte_chance(self)
        self.block_chance = update_block_chance(self)
        self.block_reduction = update_block_reduction(self)
        self.stealth_skill = update_stealth_skill(self)
        self.faith = update_faith(self)
        self.max_sanctity = update_maximum_sanctity(self)
        self.max_endurance = update_maximum_endurance(self)
        self.max_carrying_capacity = update_carrying_capacity(self)
        self.barter = update_bartering(self)
        self.oration = update_oration(self)
        self.knowledge = update_knowledge(self)
        self.luck = update_luck_chance(self)
        previous_max_health = self.max_health
        self.max_health = update_maximum_health(self)
        # Hidden attributes
        self.experience_gain_modifier = 1 # This is the percentage of exp you gain
        self.gold_gain_modifier = 1 # This is the percentage of gold you gain

        for ability in self.abilities:
            ability.update_stats()
        for item in self.equipped_items:
            item.update_stats()

        # When you update max_health, current health will also change by the same amount
        max_health_change = self.max_health - previous_max_health
        if max_health_change != 0: 
            self.current_health += max_health_change	
        if self.current_health < 0:
            self.current_health = 0	        
        
    def refresh_character(self):
        self.current_sanctity = self.max_sanctity
        self.current_health = self.max_health
        self.current_endurance = self.max_endurance
        self.current_carrying_capacity = self.max_carrying_capacity

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return False
        self.current_exp -= self.max_exp
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.age += 1
        self.ability_points += 2
        self.current_health = self.max_health
        self.update_secondary_attributes()
        return True

    def consume_item(self, item_name):
        for my_item in self.inventory:
            if my_item.name == item_name:
                my_item.apply_effect()
                my_item.amount_owned -= 1
                if my_item.amount_owned == 0:
                    self.inventory.remove(my_item)
                break

    def __str__(self):
        """Return string representation of Hero opject.
        """
        
        data = "Character object with attributes:"
        atts = []
        for key in sorted(vars(self).keys()):
            atts.append('{}: {} -> type: {}'.format(key, repr(vars(self)[key]), type(vars(self)[key])))
        data = '\n'.join(atts)
        return data
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
        
    def get_primary_attributes(self):
        return sorted(self.primary_attributes.items())


##testing##        
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import inspect
from sqlalchemy.orm import mapper

from sqlalchemy import create_engine





metadata = MetaData()       

hero = Hero()
            
            
class BuildTable:
    def __init__(self, obj):
        self.obj = obj
        self.tablename = BuildTable.get_table_name(obj)
        self.column_names = BuildTable.get_column_names(obj)
        #Attributes that require extra work.
        #They might be relationships, foreign keys or children or parents or something.
        #Or just basic lists, or dicts or booleans
        self.relationships = {'lists': [], 'dicts': [], 'nones': []}
        self.table = self.build_table()
        
    def build_table(self):
        """Return a Table object.
        
        Doesn't yet accomodate relationships.
        """
        return Table(self.tablename, metadata,
            Column('id', Integer, primary_key=True),
            *self.build_columns()
        )
        
    def build_columns(self):
        """Generate columns for table.
        
        Also updates relationship attribute whichi will be implemented using recursion.
        """
        data = vars(self.obj)
        for name in sorted(data.keys()):
            column_type = type(data[name])
            if type(list()) == column_type:
                self.relationships['lists'].append(name)
            elif type(dict()) == column_type:
                self.relationships['dicts'].append(name)    
            elif type(None) == column_type:
                self.relationships['nones'].append(name)    
            elif type(int()) == column_type:
                yield Column(name, Integer, default=data[name])
            elif type(str()) == column_type:
                yield Column(name, String, default=data[name])
            elif type(float()) == column_type:
                yield Column(name, Float, default=data[name])
            elif type(bool()) == column_type:
                yield Column(name, Boolean, default=data[name])
            else:
                raise TypeError("Can't yet handle type {}".format(type(data[name])))
        
    def get_column_names(obj):
        """Get column names for a given object.
        
        Ignores functions, may ignore class attributes.
        """
        try:
            return (attr for attr in vars(obj))
        except TypeError as ex:
            if type(dict()) == type(obj):
                return sorted(obj.keys())
            raise ex
            
    def get_table_name(obj):
        return obj.__class__.__name__
                
meta_hero = BuildTable(hero)
hero_table = meta_hero.table

mapper(Hero, hero_table)
# print(meta_hero.relationships)

# meta_dict = BuildTable(primary_attributes)
# dict_table = meta_dict.table
# mapper(primary_attributes, dict_table)

# address = Table('address', metadata,
            # Column('id', Integer, primary_key=True),
            # Column('user_id', Integer, ForeignKey('user.id')),
            # Column('email_address', String(50))
            # )

# mapper(User, user, properties={
    # 'addresses' : relationship(Address, backref='user', order_by=address.c.id)
# })

# mapper(Address, address)



# for t in metadata.sorted_tables:
    # print("Table name: ", t.name)
    # print("t is page_table: ", t is hero_table)

# for column in hero_table.columns:
    # print("Column Table name: ", column.type)

engine = create_engine('sqlite:///:memory:', echo=False)
# metadata.bind = engine
# metadata.create_all(checkfirst=True)
Base.metadata.create_all(engine)


primary_attributes = BaseDict({"Strength": 1, "Resilience": 1, "Vitality": 1, "Fortitude": 1, "Reflexes": 1, "Agility": 1, "Perception": 1, "Wisdom": 1, "Divinity": 1, "Charisma": 1, "Survivalism": 1, "Fortuity": 1})

#is a one to one list the same as just having a variable equal to a Base object?
# is primary_attributes = relationship(BaseDict, one to one) 
# equal to
# primary_attributes = BaseDict()?

print(primary_attributes)

# import pdb; pdb.set_trace()
primary_attributes['Badassery'] = 5
print(primary_attributes)
# print(primary_attributes.keys())



# from sqlalchemy.orm import sessionmaker

# Session = sessionmaker(bind=engine)
# session = Session()

# hero = Hero()
# hero.name = 'Haldon'
# session.add(hero)



# insp = inspect(Hero)
# for column in list(insp.columns):
    # print(repr(column))
# hero_table.update(hero)



#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#
from sqlalchemy import Column, Integer, String, Boolean

from base_classes import Base

class MonsterTemplate(Base):
    __tablename__ = 'monster_template'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    species = Column(String)
    species_plural = Column(String)
    level_min = Column(Integer) # The lowest level it can ever be generated as. (So you can't generate a level 1 dragon for example)
    level_max = Column(Integer) # The highest level you can ever generate as. (So you can't generatea level 75 rat for example)
    experience_rewarded = Column(Integer)

    # Query requests which help determine which monster to pull for the occassion
    forest = Column(Boolean)
    cave = Column(Boolean)

    # This is used to boost certain creatures. The stronger a creature would seem to be, the higher the boost it gets. For example, a rat
    # wouldn't seem to be as tough as a dog or human of the same level. So it would have a < 1 modifier. Default is 1.
    level_modifier = Column(Integer)

    # For generating monsters, this is merely the stat distribution. It has nothing to do with their power level. A level 10 rat and a level 10
    # goblin would have the same amount of stat points to distribute. The values below just tell the game HOW to distribute them. So the goblin
    # should have higher points in intellect and brawn, but likely lower agility and quickness. The default of any value should be 1
    # If you set a value to 0, it means it will never have any points into that statistic (like a rat should have 0 charisma)
    agility = Column(Integer)
    charisma = Column(Integer)
    divinity = Column(Integer)
    resilience = Column(Integer)
    fortuity = Column(Integer)
    pathfinding = Column(Integer)
    quickness = Column(Integer)
    willpower = Column(Integer)
    brawn = Column(Integer)
    survivalism = Column(Integer)
    vitality = Column(Integer)
    intellect = Column(Integer)

    def __init__(self, name, species="None", species_plural="None", level_min=1, level_max=99, experience_rewarded=0, level_modifier=1,
                 forest=False, cave=False,
                 agility=1, charisma=1, divinity=1, resilience=1, fortuity=1, pathfinding=1,
                 quickness=1, willpower=1, brawn=1, survivalism=1, vitality=1, intellect=1):
        self.name = name
        self.species = species
        self.species_plural = species_plural
        self.level_min = level_min
        self.level_max = level_max
        self.experience_rewarded = experience_rewarded
        self.level_modifier = level_modifier

        self.forest = forest
        self.cave = cave

        self.agility = agility
        self.charisma = charisma
        self.divinity = divinity
        self.resilience = resilience
        self.fortuity = fortuity
        self.pathfinding = pathfinding
        self.quickness = quickness
        self.willpower = willpower
        self.brawn = brawn
        self.survivalism = survivalism
        self.vitality = vitality
        self.intellect = intellect

class Monster(object):
    def __init__(self, name, level):
        self.name = name
        self.level = level

def create_monster(name, level):
    return Monster(name=name, level=level)



from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from base_classes import Base


class Achievements(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Achievements to Journal is One to One
    # Journal to Achievements is One to One.
    journal_id = Column(Integer, ForeignKey('journal.id', ondelete="CASCADE"))
    journal = relationship(
        "Journal",
        back_populates="achievements",
        cascade="all, delete-orphan",
        single_parent=True)

    deepest_dungeon_floor = Column(Integer)  # High score for dungeon runs
    current_dungeon_floor = Column(Integer)  # Which floor of dungeon your on
    # Current progress in current cave floor
    current_dungeon_floor_progress = Column(Integer)
    player_kills = Column(Integer)
    monster_kills = Column(Integer)
    deaths = Column(Integer)
    wolf_kills = Column(Integer)

    achievements = relationship("Achievement", cascade="all, delete-orphan")

    # Should return all completed Achievements?
    completed_achievements = relationship(
        "Achievement",
        primaryjoin="and_(Achievements.id==Achievement.achievements_id, "
                    "Achievement.completed==True)",
        cascade="all, delete-orphan")

    # Should return a list of all Achievement type with "kill" in their name.
    kill_achievements = relationship(
        "Achievement",
        primaryjoin="and_(Achievements.id==Achievement.achievements_id, "
                    "Achievement.name.ilike('%kill%'))",
        cascade="all, delete-orphan")

    def __init__(self):
        # Achievements and statistics
        self.deepest_dungeon_floor = 0
        self.current_dungeon_floor = 0
        self.current_dungeon_floor_progress = 0
        self.player_kills = 0
        self.monster_kills = 0
        self.deaths = 0
        self.wolf_kills = 0

        self.achievements = [Achievement("Wolf kills", experience=50)]


class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True)

    # Relationships
    achievements_id = Column(Integer, ForeignKey("achievements.id",
                                                 ondelete="CASCADE"))

    completed = Column(Boolean)

    name = Column(String(100))
    current_level = Column(Integer)
    next_level = Column(Integer)
    experience = Column(Integer)

    def __init__(self, name, experience=0):
        self.name = name
        self.experience = experience
        self.current_level = 0
        self.next_level = 1

    def leveling_scheme(self):
        return [1, 25, 100, 500]

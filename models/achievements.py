import sqlalchemy as sa
import sqlalchemy.orm

import models


class Achievements(models.Base):
    # Relationships
    # Achievements to Journal is One to One
    # Journal to Achievements is One to One.
    journal_id = sa.Column(sa.Integer, sa.ForeignKey('journal.id', ondelete="CASCADE"))
    journal = sa.orm.relationship(
        "Journal",
        back_populates="achievements",
        cascade="all, delete-orphan",
        single_parent=True)

    deepest_dungeon_floor = sa.Column(sa.Integer)  # High score for dungeon runs
    current_dungeon_floor = sa.Column(sa.Integer)  # Which floor of dungeon you are on
    current_floor_progress = sa.Column(sa.Integer)  # How much of the current floor you have explored.
    player_kills = sa.Column(sa.Integer)
    monster_kills = sa.Column(sa.Integer)
    deaths = sa.Column(sa.Integer)
    wolf_kills = sa.Column(sa.Integer)

    achievements = sa.orm.relationship("Achievement", cascade="all, delete-orphan")

    # Should return all completed Achievements?
    completed_achievements = sa.orm.relationship(
        "Achievement",
        primaryjoin="and_(Achievements.id==Achievement.achievements_id, "
                    "Achievement.completed==True)",
        cascade="all, delete-orphan")

    # Should return a list of all Achievement type with "kill" in their name.
    kill_achievements = sa.orm.relationship(
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


class Achievement(models.Base):
    # Relationships
    achievements_id = sa.Column(sa.Integer, sa.ForeignKey("achievements.id", ondelete="CASCADE"))

    completed = sa.Column(sa.Boolean)

    name = sa.Column(sa.String(100))
    current_level = sa.Column(sa.Integer)
    next_level = sa.Column(sa.Integer)
    experience = sa.Column(sa.Integer)

    def __init__(self, name, experience=0):
        self.name = name
        self.experience = experience
        self.current_level = 0
        self.next_level = 1

    def leveling_scheme(self):
        return [1, 25, 100, 500]

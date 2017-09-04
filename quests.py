"""
How to use:
Quests must be created separately in the prebuilt_objects.py module.
We will really need a quest editor. Some kind of 3D mind node thing :P

#Currently:
To connect a hero to a given quest (only connect to the first quest in the quest path).
for quest in database.get_default_quests():
    quest.add_hero(myHero)

To trigger a quest to advance to the next stage or complete.
for path in myHero.quest_paths:
    if path.quest.name == "Get Acquainted with the Blacksmith" and path.stage == 1:
        path.advance()
        

#Future:
database.connect_quest(quest_name, hero) #Not implemented.
database.disconnect_quest(quest_name, hero) #Not implemented.
database.advance_quest(quest_name, hero, stage?) #Not implemented.

#Far Future:
use triggers .... build a game engine :P
Thus to advance a quest you would spawn an event any time the hero did anything
and the engine would check the events data against each quest. Any quest that 
met the requirements of this trigger would advance.
eg. Trigger for "Talk to the Blacksmith" quest would be:
    t1 = Trigger(Location=Blacksmith, action=talk)
    t2 = Trigger(Location=Blacksmith, action=buy)
    t3 = Trigger((Location=Blacksmith, action=sell)
While the Quest object would look like
    q1 = Quest(name="Get aquainted with Blacksmith", descript="Talk to blacksmith",
        triggers=[t1], stage=1, next_quests=[q2], past_quests=[])
    q2 = Quest(name="Get aquainted with Blacksmith", descript="Buy or sell an item.",
        triggers=[t2, t3], stage=2, next_quests=[], past_quests=[q1])

A Trigger can have multiple actions. A Quest can have multiple Triggers. Only one needs to be met
to cause the Quest to advance? 

##############
Quest object/QuestPath object
Specification: 
    An object that allows interesting and complex path completion.
Considerations:
    A quest must have multiple stages.
    A quest must relate to a hero object or objects
    A quest must have a final stage. (I believe the start stage is implicit?)
    A quest must have a Self-Referential Many-to-Many Relationship (probably).
    A quest must have a reward for each stage.
    A quest must have a bonus reward for completing the final stage (a "multiplier" to 
        calculate the bonus from.) The multiplier should increase for each stage completed.
    A quest must have a description.
    A quest must have a name (which should be unique?).
    A quest must be able to have multiple start points.
    A quest must be able to have multiple exit points.
    A quest must have a special completion method for the final stage.

Methods:
    A quest must be able to advance to the next _relavant_ stage.
    A quest must be able to pay out when the current stage is completed.
    A quest must be able to pay out [plus the multiplier] at the final stage.

Potentials:
    A quest should be aware of the maximum number of stages?
    A quest must have some kind of display?
    A quest may need to have awareness of all stages and start and completion points?
        Though that could probably be a secondary table? Or metaclass or something?
    
    
Considering:
    A quest should have a list of triggers? The hero could send in a trigger
        instead of a quest object ... and the trigger would cause a specific
        quest path to be chosen?       
"""

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy import orm

from base_classes import Base
import pdb

class QuestPath(Base):
    """Allow storage of quest stage for a given hero and a given quest.
    
    This means that each hero can be in a different stage of the same quest.
    Each Hero can have many QuestPaths and many Quests
    Each QuestPath must have only one Hero and one Quest per path.
    Each Quest can be in many QuestPaths and held by many Heroes.
    Or something ... it makes sense if I draw a picture :P
    
    To check what quests a hero has active use:
    for path in hero.quest_paths:
        if path.acitve:
            return path.quest.name
    To check what quests a hero has completed use:
    for path in hero.quest_paths:
        if path.completed:
            return path.quest.name

        
    Use:
        quest.add_hero(hero) or,
        QuestPath(quest, hero) or,
        quest.quest_paths.append(QuestPath(quest, hero)) or,
        hero.quest_paths.append(QuestPath(quest, hero))
    
    But obviously the first one is fastest to type and use. And the first one uses only TWO
    classes (well 3 but the third is hidden).
    
    Considering: Add name to QuestPath object ... remove it from Quest object.
    
    Future: add and remove quest_paths using database. Database is sort of becomming the
    game engine ...
    """
    __tablename__ = 'quest_path'
    
    id = Column(Integer, primary_key=True)
    
    stage = Column(Integer)
    stage_count = orm.synonym('stage')
    display_stage = orm.synonym('stage')
    
    stages = Column(Integer)
    
    active = Column(Boolean)
    completed = Column(Boolean)
    
    def __init__(self, quest, hero, active=True, stage=1):
        self.quest = quest
        self.hero = hero
        
        self.stage = stage
        self.stages = quest.get_stage_count()
        self.active = active
        self.completed = False

        # Make Trigger available!
        self.quest.completion_trigger.link(hero)
        
    def advance(self):
        """Advance this path to the next stage.
        
        Also spawn any new paths and update hero and quest objects as neccessary
        to account for path ending. Update hero xp and such.
        
        NOTE: I am using the metaphor of each path being a glaxay with a decaying orbit.
        Sometimes this galaxy will break apart and spawn new galaxies.
        """
        
        # Sort of like a failsafe. Active paths should not be advanced.
        # Maybe this should be an assert?
        if self.completed:
            return
            
        FINAL_STAGE = 0
        SIMPLE_ADVANCE = 1
        COMPLEX_ADVANCE = 2
        orbit = len(self.quest.next_quests)
        
        if orbit == FINAL_STAGE:
            self.completed = True
            self.reward_hero(final=True)
        elif orbit == SIMPLE_ADVANCE:
            self.reward_hero()
            self.stage += 1
            self.quest = self.quest.next_quests[0]
        elif orbit >= COMPLEX_ADVANCE:
            self.reward_hero()
            self.stage += 1
            for quest in self.quest.next_quests:
                QuestPath(quest, self.hero, stage=self.stage)
                #Needs further testing.
                self.remove()
        return True
    
    # Needs further testing.
    def remove(self):
        """Break/erase current path.
        
        Used when spawning multiple new paths from this one.
        This method will need to be in the database.py module ... *sigh*
        I need to delete the record of this path after I have spawned a bunch
        of clones starting from the same point.
        """
        self.hero = None
        self.quest = None
        
    def reward_hero(self, final=False):
        """Reward the hero on stage completion.
        
        The hero gains a bonus when the final quest stage is completed.
        NOTE: the hero gets a different notification when completing vs.
        advancing for a quest. (quest.path_name vs quest.description)
        """
        
        hero = self.hero
        quest = self.quest
        if final:
            hero.experience += int(quest.reward_experience * self.stage * 0.3)
            hero.quest_notification = (quest.path_name, quest.reward_experience)
        else:
            hero.experience += quest.reward_experience
            hero.quest_notification = (quest.description, quest.reward_experience)

    @validates('active')
    def validate_active(self, key, flag):
        """Prevent quest being both active and completed at the same time.
        """

        if self.completed:
            return False
        return flag

    @validates('completed')
    def validate_completed(self, key, flag):
        """Prevent quest being both active and completed at the same time.
        """
        if flag:
            self.active = False
        return flag
        
    def active_heroes(quest):
        """Return all heroes that exist in quest.quest_paths and are active.
        
        for path in quest.quest_paths:
            if path.active:
                path.hero
                
        NOTE: class method!
        """
     
        return [path.hero for path in quest.quest_paths if path.active]

    @staticmethod
    def completed_heroes(quest):
        """Return all heroes that exist in quest.quest_paths and are completed.
        
        for path in quest.quest_paths:
            if path.completed:
                path.hero
        """
     
        return [path.hero for path in quest.quest_paths if path.completed]

    @staticmethod
    def all_heroes(quest):
        """Return all heroes that exist in quest.quest_paths.
        
        for path in quest.quest_paths:
            path.hero
        """
     
        return [path.hero for path in quest.quest_paths if path.completed]

    @staticmethod
    def find(quest, hero):
        """Return the path connecting quest to hero -> if it exists.
        
        This should maybe be a query? Because it is _slow_ right now.
        """
        for path in quest.quest_paths:
            if path.hero.id == hero.id:
                return path

                
quest_to_quest = Table("quest_to_quest", Base.metadata,
    Column("past_quest_id", Integer, ForeignKey("quest.id"), primary_key=True),
    Column("next_quest_id", Integer, ForeignKey("quest.id"), primary_key=True)
)


class Quest(Base):
    """A class to describe quest objects that can be stored in a database.
    
    
    Final stage is when next_quests == [].
    Initial stage is when past_quests == [].
    
    Useful note: Relationships are set ... but a commit must occur
    between adding in each new element.
    """
    __tablename__ = "quest"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path_name = orm.synonym('name')
    
    description = Column(String)
    current_description = orm.synonym('description')
    
    reward_experience = Column(Integer)

    # Relationships
    # Self ... Many to Many?
    next_quests = relationship("Quest",
        secondary=quest_to_quest,
        primaryjoin=id==quest_to_quest.c.past_quest_id,
        secondaryjoin=id==quest_to_quest.c.next_quest_id,
        backref="past_quests")

    # Triggers Each Quest has a completion trigger. Each trigger can
    # complete multiple quests?
    # One to Many? (Later will be many to many).
    trigger_id = Column(Integer, ForeignKey('trigger.id'))
    completion_trigger = relationship("Trigger", back_poplulates='quests')

    def __init__(self, path_name, description, reward_experience=3,
                 next_quests=[], past_quests=[], completion_trigger=None):
        """Build a new Quest object.
        
        You can link this quest to other quests at initialization or afterwards.
        quest.next_quests.append(quest2) does the same thing.
        """
        
        self.path_name = path_name
        self.description = description
        self.reward_experience = reward_experience
        self.next_quests = next_quests
        self.past_quests = past_quests
        self.completion_trigger = completion_trigger
        
    def get_stage_count(self):
        """Return a guestimate of how many stages are in this quest.
        
        Or well I guess it is the total number of possible paths that are available.
        Though really you can't take all of them because most are mutually
        exclusive.
        NOTE: only works when ran from stage 1.
        """

        if self.next_quests == []:
            return 1
            
        for next_quest in self.next_quests:
            return 1 + next_quest.get_stage_count()
    
    
    def mark_completed(self, hero):
        """Set completed flag and deactivate quest.
        
        Deactivate this quest. Quest is assumed to be active before.
        """
        quest_path = QuestPath.find(self, hero)
        quest_path.completed = True
            
            
    def activate(self, hero):
        """Use to activate the first quest in a series.
        
        I don't even know if this gets used ... though it might be in the future.
        """
        quest_path = QuestPath.find(self, hero)
        assert quest_path != None
        
        if not quest_path.active:
            quest_path.active = True
        
    def add_hero(self, hero):
        """Build a new quest path connecting this quest and hero -> return QuestPath
        
        NOTE: session.commit() required! Error could be thrown during commit!
        NOTE2: Checks if path already exists.
        
        Will be replaced by database method connect_quest(quest_name, hero)
        """
        quest_path = QuestPath.find(self, hero)
        if quest_path:
            return quest_path
        return QuestPath(self, hero)
        

# class Primary_Quest(Quest):
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)

if __name__ == "__main__":        
    quest1 = Quest("Get Acquainted with the Blacksmith", "Go talk to the blacksmith.")
    quest1.next_quests.append(Quest("Get Acquainted with the Blacksmith", "Buy your first item.", reward_experience=7))
    quest2 = Quest("Equipping/Unequipping", "Equip any item.")
    quest2.next_quests.append(Quest("Equipping/Unequipping", "Unequip any item."))
            
    testing_quests = [quest1, quest2] #Which is really 4 quests.
    # pdb.set_trace()

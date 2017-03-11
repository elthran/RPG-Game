"""
Quest object
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
    I am considering allowing:
        quest.quest_paths.append(quest, hero) 
    and having it auto-gen a QuestPath object with these vars.
    or like hero.add_quest(quest)       
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
    Each QuestPath can have Many heroes and Many quests ...
    but each path must have one hero and one quest?
    
    Heroes to Quests Explained:
        Hero object relates to quests via active_quests and completed_quests.
        Hero quests can be either active or completed or neither, but not both.
        
    
        This relationship forms through the QuestPath object.
        Which establishes a manay to many relationship between quests and heroes.
        
    QuestPath provides many special methods such as:
        quest_path.active_heroes(quest, hero) and returns all of the heroes that have this quest
            active.
        active_quests ... does the same for quests.
        
        all_quests and all_heroes do what they sound like. See code :P
        
    Use:
        quest.add_hero(hero) or,
        QuestPath(quest, hero) or,
        quest.quest_paths.append(QuestPath(quest, hero)) or,
        hero.quest_paths.append(QuestPath(quest, hero))
    
    But obviously the first one is fastest to type and use. And the first one uses only TWO
    classes (well 3 but the third is hidden).
    """
    __tablename__ = 'quest_path'
    
    id = Column(Integer, primary_key=True)
    
    stage = Column(Integer)
    stage_count = orm.synonym('stage')
    display_stage = orm.synonym('stage')
    
    stages = Column(Integer)
    
    active = Column(Boolean)
    completed = Column(Boolean)
    
    def __init__(self, quest, hero, active=True):
        self.quest = quest
        self.hero = hero
        
        self.stage = 1
        self.stages = quest.get_stage_count()
        self.active = active
        self.completed = False
        
        
    @validates('active')
    def validate_active(self, key, flag):
        """Prevent quest being both active and completed at the same time.
        """
        assert self.completed != True
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
        
        
    def completed_heroes(quest):
        """Return all heroes that exist in quest.quest_paths and are completed.
        
        for path in quest.quest_paths:
            if path.completed:
                path.hero
        """
     
        return [path.hero for path in quest.quest_paths if path.completed]
        
    
    def all_heroes(quest):
        """Return all heroes that exist in quest.quest_paths.
        
        for path in quest.quest_paths:
            path.hero
        """
     
        return [path.hero for path in quest.quest_paths if path.completed]
        
        
    def find(quest, hero):
        """Return the path connecting quest to hero -> if it exists.
        
        This should maybe be a query?
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
    
    'multiplier' is an internal variable as is 'completed'.
    'multiplier' is a saved and calculated variable, each time a quest is completed
    the next quest in the quest path has this multiplier + 1.
    
    Final stage is when next_quests == [].
    Initial stage is when past_quests == [].
    If quest is added to hero.active quests ... it default finds the initial stage?
    Or should the coder _have_ to add the initial stage?
    
    
    Hero object relates to quests via active_quests and completed_quests.
    Hero quests can be either active or completed?
    @validates functions:
        Prevent quest being both active and completed at the same time.
    
    Relationships are set ... but a commit must occur between adding in each new element.
    """
    __tablename__ = "quest"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    description = Column(String)
    current_description = orm.synonym('description')
    
    reward_xp = Column(Integer)
    
    next_quests = relationship("Quest",
        secondary=quest_to_quest,
        primaryjoin=id==quest_to_quest.c.past_quest_id,
        secondaryjoin=id==quest_to_quest.c.next_quest_id,
        backref="past_quests")
    
    def __init__(self, name, description, reward_xp=3):
        """Build a new Quest object.
        
        Heroes is must be a list. 
        To add a single hero at initialization use:
            Quest('Kill a wolf', 'Find and slay a wolf!', active_heroes=[hero])
        """
        
        self.name = name
        self.description = description
        self.reward_xp = reward_xp
        
    def get_stage_count(self):
        """Return a guestimate of how many stages are in this quest.
        """

        if self.next_quests == []:
            return 1
            
        for next_quest in self.next_quests:
            return 1 + next_quest.get_stage_count()
        
    #Considering:
    #Split this and connected methods between hero object and quest object.
    def advance_quest(self, hero, next_quest=None):
        """Move to the next quest in the quest path.
        
        If there is only one quest in the next_quests attribute
        then 
            and pay out this one
            deactivate this one
            activate that one 
        else you must send in the name of the next quest to be activated.
            search for quest in next_quests
            if there then 
                pay out
                deactivate this one
                activate next one
            else:
                error quest named 'next_quest_name' not in this quest path
                
        Not fully implemented ....
        I need to make it actually use the self.next_quests attribute.
        """
        
        #pdb.set_trace()
        quest_path = QuestPath.find(self, hero)
        if len(self.next_quests) == 0:
            self.reward_hero(quest_path, hero, final=True)
            self.mark_completed(hero)
        elif len(self.next_quest) == 1:
            self.activate_next_quest(next_quest, hero)
                
    def activate_next_quest(self, next_quest, hero):
        """Activate the next quest in the series if possible.
        
        If not hard fail ...? I sugguest improving this to a custom exception at some point.
        I have not idea how to to quest_path.stage and stages ...
        """
        
        quest_path = QuestPath.find(self, hero)
        if next_quest:
            quest_path.stage += 1
            if quest_path.stage > quest_path.stages:
                quest_path.stages = quest_path.stage
            quest_path.quest = next_quest
            
    
    def reward_hero(self, quest_path, hero, final=False):
        """Pay out xp to hero on stage completion.
        """
        if final:
            hero.current_exp += int(self.reward_xp * quest_path.stage * 0.3)
        else:
            hero.current_exp += self.reward_xp
        hero.quest_notification = (self.name, self.reward_xp)
        
                
    def mark_completed(self, hero):
        """Set completed flag and deactivate quest.
        
        Deactivate this quest. Quest is assumed to be active before.
        """
        quest_path = QuestPath.find(self, hero)
        quest_path.completed = True
            
            
    def activate(self, hero):
        """Use to activate the first quest in a series.
        
        """
        quest_path = QuestPath.find(self, hero)
        assert quest_path != None
        
        if not quest_path.active:
            quest_path.active = True
        
            
    def add_hero(self, hero):
        """Build a new quest path connecting this quest and hero -> return QuestPath
        
        NOTE: session.commit() required! Error could be thrown during commit!
        NOTE2: Checks if path already exists.
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
    quest1.next_quests.append(Quest("Get Acquainted with the Blacksmith", "Buy your first item.", reward_xp=7))
    quest2 = Quest("Equipping/Unequipping", "Equip any item.")
    quest2.next_quests.append(Quest("Equipping/Unequipping", "Unequip any item."))
            
    testing_quests = [quest1, quest2] #Which is really 4 quests.
    # pdb.set_trace()

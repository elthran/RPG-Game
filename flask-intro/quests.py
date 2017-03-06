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

Methods:
    A quest must be able to advance to the next _relavant_ stage.
    A quest must be able to pay out when the current stage is completed.
    A quest must be able to pay out [plus the multiplier] at the final stage.

Potentials:
    A quest should be aware of the maximum number of stages?
    A quest must have some kind of display?
    A quest may need to have awareness of all stages and start and completion points?
        Though that could probably be a secondary table? Or metaclass or something?
    A quest may need a special completion method for the final stage?
    
Considering:
    A quest should have a list of triggers? The hero could send in a trigger
        instead of a quest object ... and the trigger would cause a specific
        quest path to be chosen?
        
Promblems:
    active flag will affect all version of a quest. This needs to be changed.
    The hero object will need to maintain an active_quests list.
    This list would be updated instead of changing the active flag ...
    The active flag will be removed.
    
    The same problem will occur with the completed flag ...
    Fix?: maybe something like self.heroes[hero.id].completed_quests[self.name] += 1?
    If heroes and completed_quests are dictionaries?
    And completed quests can keep track of how many times a quest can be completed?
"""

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy import orm

from base_classes import Base
import pdb

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
    
    multiplier = Column(Integer)
    stage_count = orm.synonym('multiplier')
    display_stage = orm.synonym('multiplier')
    
    next_quests = relationship("Quest",
        secondary=quest_to_quest,
        primaryjoin=id==quest_to_quest.c.past_quest_id,
        secondaryjoin=id==quest_to_quest.c.next_quest_id,
        backref="past_quests")
    
    def __init__(self, name, description, active_heroes=[], reward_xp=3, active=False):
        """Build a new Quest object.
        
        Heroes is must be a list. 
        To add a single hero at initialization use:
            Quest('Kill a wolf', 'Find and slay a wolf!', active_heroes=[hero])
        """
        
        self.name = name
        self.description = description
        
        self.active_heroes = active_heroes
        self.reward_xp = reward_xp
        self.multiplier = 1 # Rebuild as multiplier? Counts up from the start?
        
        
    @validates('active_heroes')
    def validate_active_heroes(self, key, hero):
        """Prevent quest being both active and completed at the same time.
        """
        assert hero not in self.completed_heroes
        return hero 

    @validates('completed_heroes')
    def validate_completed_heroes(self, key, hero):
        """Prevent quest being both active and completed at the same time.
        """
        assert hero not in self.active_heroes
        return hero 
        
        
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
                
        
        """
        
        self.reward_hero(hero)
        self.mark_completed(hero)
        self.activate_next_quest(next_quest, hero)
                
    def activate_next_quest(self, next_quest, hero):
        """Activate the next quest in the series if possible.
        
        If not hard fail ...? I sugguest improving this to a custom exception at some point.
        """
        if next_quest:
            quest += self.multiplier
            quest.activate(hero)
            
    
    def reward_hero(self, hero):
        """Pay out xp to hero on stage completion.
        """
        if not self.next_quests:
            hero.current_exp += int(self.reward_xp * self.multiplier * 0.3)
        else:
            hero.current_exp += self.reward_xp
        hero.quest_notification = (self.name, self.reward_xp)
        
                
    def mark_completed(self, hero):
        """Set completed flag and deactivate quest.
        
        Deactivate this quest. Quest is assumed to be active before.
        """
        self.active_heroes.remove(hero)
        self.completed_heroes.append(hero)
            
            
    def activate(self, hero):
        """Use to activate the first quest in a series.
        
        """
        self.active_heroes.append(hero)   
        

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

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

quest_to_quest = Table("quest_to_quest", Base.metadata,
    Column("past_quest_id", Integer, ForeignKey("quest.id"), primary_key=True),
    Column("next_quest_id", Integer, ForeignKey("quest.id"), primary_key=True)
)

class Quest(object):
    """A class to describe quest objects that can be stored in a database.
    
    'multiplier' is an internal variable as is 'completed'.
    'multiplier' is a saved and calculated variable, each time a quest is completed
    the next quest in the quest path has this multiplier + 1.
    
    Considering removing final_stage attribute in favor of calculating final_stage
    as when next_quests == []
    
    Hero object relates to quest via 'quests' list.
    in that list there are:
        'active=True, completed=False' quests (quests the hero can complete)
        'completed=True, activate=False' quests (quests the hero has complete) and
        'active=False, completed=False' quests (quests the hero will be able to do
            when they complete some of their active quests)
    """
    __tablename__ = "quest"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    description = Column(String)
    current_description = orm.synonym('description')
    
    reward_xp = Column(Integer)
    
    multiplier = Column(Integer)
    stage_count = orm.synonym('multiplier')
    display_stage = orm.synonym('multiplier')

    active = Column(Boolean) 
    completed = Column(Boolean)
    
    next_quests = relationship("Quest",
        secondary=quest_to_quest,
        primaryjoin=id==quest_to_quest.c.past_quest_id,
        secondaryjoin=id==quest_to_quest.c.next_quest_id,
        backref="past_quests")
    
    def __init__(self, name, description, heroes=[], reward_xp=3, active=False):
        """Build a new Quest object.
        
        Heroes is must be a list. 
        To add a single hero at initialization use:
            Quest('Kill a wolf', 'Find and slay a wolf!', heroes=[hero])
        """
        
        self.name = name
        self.description = description
        
        self.heroes = heroes
        self.reward_xp = reward_xp
        self.multiplier = 1 # Rebuild as multiplier? Counts up from the start?
        self.active = active
        
        self.completed = False

            
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
                
        Hero object relates to quest via 'quests' list.
        in that list there are:
            'active=True, completed=False' quests (quests the hero can complete)
            'completed=True, activate=False' quests (quests the hero has complete) and
            'active=False, completed=False' quests (quests the hero will be able to do
                when they complete some of their active quests)
        """
        if hero not in self.heroes:
            exit("This hero doesn't have this quest.")
        
        self.reward_hero(hero)
        self.mark_completed()
        self.activate_next_quest(next_quest)
                
    def activate_next_quest(self, quest):
        """Activate the next quest in the series if possible.
        
        If not hard fail ...? I sugguest improving this to a custom exception at some point.
        """
        if quest:
            quest += self.multiplier
            quest.activate()
        elif next_quest not in self.next_quests:
            print("The valid next quests are: {}".format(self.next_quests))
            exit("This is not a valid next quest.")
    
    def reward_hero(self, hero):
        """Pay out xp to hero on stage completion.
        """
        if not self.next_quests:
            hero.current_exp += int(self.reward_xp * self.multiplier * 0.3)
        else:
            hero.current_exp += self.reward_xp
        hero.quest_notification = (self.name, self.reward_xp)
        
                
    def mark_completed(self):
        """Set completed flag and deactivate quest.
        
        Deactivate this quest. Quest is assumed to be active before.
        """
        self.active = False
        self.compteted = True
    
            
    def update_owner(self, hero):
        print("Quest to Hero relationship is now Many to Many.")
        print("Instead of One Hero to Many Quests.")
        exit("Removed in favor of add_hero and remove_hero")
        # self.heroes = [hero]
        
        
    def add_hero(self, hero):
        """Give a hero this quest.
        """
        if hero is None:
            return
        if hero not in self.heroes:
            self.heroes.append(hero)
        else:
            raise Exception("ValueError: Hero already has this ability.")
        
        
    def remove_hero(self, hero):
        """Remove this quest from a hero.
        """
        try:
            self.heroes.remove(hero)
        except ValueError:
            raise Exception("ValueError: Hero doesn't have this ability")
            
            
    def activate(self):
        """Use to activate the first quest in a series.
        
        hero.quests[4].activate()
        Considering:
            maybe should activate_series_by_name
        and quest object should have a series_name attribute
        that is the same for all elements in a series?
        """
        self.active = True    

# class Primary_Quest(Quest):
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)


quest1 = Quest("Get Acquainted with the Blacksmith", myHero, stages=2, stage_descriptions=["Go talk to the blacksmith.", "Buy your first item."], reward_xp=7)
        
testing_quests = [Quest("Get Acquainted with the Blacksmith", myHero, stages=2, stage_descriptions=["Go talk to the blacksmith.", "Buy your first item."], reward_xp=7), Quest("Equipping/Unequipping", myHero, stages=2, stage_descriptions=["Equip any item.", "Unequip any item."])]

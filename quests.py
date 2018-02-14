"""

THIS IS REALLY OUT OF DATE! ASK ME TO UPDATE IT. SAVE ME FROM MYSELF!

How to use:
Quests must be created separately in the prebuilt_objects.py module.
We will really need a quest editor.

#Currently:
To connect a hero to a given quest (only connect to the first quest in the
quest path).
for quest in database.get_default_quests():
    quest.add_hero(hero)

To trigger a quest to advance to the next stage or complete.
for path in hero.journal.quest_paths:
    if path.quest.name == "Get Acquainted with the Blacksmith" and
            path.stage == 1:
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
from sqlalchemy.orm import relationship, validates, column_property
from sqlalchemy import orm
from sqlalchemy.ext.orderinglist import ordering_list

from base_classes import Base
from events import HandlerMixin
from factories import TemplateMixin
import pdb
from pprint import pprint


quest_path_to_quest = Table(
    "quest_path_to_quest",
    Base.metadata,
    Column("quest_path_id", Integer, ForeignKey("quest_path.id")),
    Column("quest_id", Integer, ForeignKey("quest.id"))
)


class QuestPath(TemplateMixin, HandlerMixin, Base):
    """A list of sequential quests that must be completed in order.

    This path can spawn a new path at any point ... a new path may or may not
    end this path. Which may have nothing to do with this path and everything
    to do with events and triggers?

    A QuestPath does not need to be attached to a hero when it is created?
    This is specific to a Template quest?
    Once a normal Path is opened it will be linked to a hero object through
    that hero's Journal.
    """
    __tablename__ = 'quest_path'
    
    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    description = Column(String(200))
    reward_experience = Column(Integer)
    stage = Column(Integer)
    is_default = Column(Boolean)

    # Relationships
    # QuestPath to Journal is Many to One.
    journal_id = Column(Integer, ForeignKey('journal.id'))
    journal = relationship("Journal", back_populates='quest_paths',
                           foreign_keys="[QuestPath.journal_id]")

    notification_id = Column(Integer, ForeignKey("journal.id"))

    # Each Path can be connected to any quest.
    # Each Quest can be connected to multiple paths.
    # The relationship is linear and ordered!
    quests = relationship(
        "Quest",
        order_by="Quest.position",
        collection_class=ordering_list('position'),
        secondary=quest_path_to_quest,
        back_populates="quest_paths",
    )

    def __init__(self, name, description=name, reward_experience=5, stage=0,
                 quests=[], is_default=False, template=True):
        self.name = name
        self.description = description
        self.reward_experience = reward_experience
        self.stage = stage
        self.quests = quests
        self.is_default = is_default
        self.template = template  # See TemplateMixin?

    def build_new_from_template(self):
        return QuestPath(self.name, self.description,
                         self.reward_experience, self.stage, self.quests,
                         template=False)

    @property
    def stages(self):
        return len(self.quests)

    @property
    def current_quest(self):
        return self.quests[self.stage]

    @property
    def total_reward(self):
        return sum((quest.reward_experience for quest in self.quests)) \
               + self.reward_experience

    def get_description(self):
        """Return a description of the of the quest path.

        Description format changes if quest is completed.

        This might be kind of confusing .. maybe I should just have 2 methods?
        """
        class Data:
            pass

        data = Data()
        data.name = self.name
        data.total_reward = self.total_reward

        if self.completed:
            return data

        data.total_reward = None
        data.stage = self.stage + 1
        data.stages = self.stages
        data.current_quest = Data()
        data.current_quest.name = self.current_quest.name
        data.current_quest.reward = self.current_quest.reward_experience
        return data

    def advance(self):
        """Advance this path to the next stage.
        
        Maybe?: Also spawn any new paths and update hero and quest objects as
        necessary to account for path ending. Update hero xp and such.
        """
        
        # Sort of like a failsafe. Active paths should not be advanced.
        # Maybe this should be an assert?
        assert self.completed != True

        if self.stage == self.stages-1:
            self.completed = True
            self.reward_hero(final=True)
        else:
            self.reward_hero()  # Reward must come before stage increase.
            self.stage += 1

        # Potentially spawn a new path? or maybe that would be a trigger
        # in Quests?
        # QuestPath(quest, self.hero, stage=self.stage)

    def reward_hero(self, final=False):
        """Reward the hero on stage completion.
        
        The hero gains a bonus when the final quest stage is completed.
        NOTE: the hero gets a different notification when completing vs.
        advancing for a quest. (quest.name vs path.name)
        """
        
        hero = self.journal.hero
        quest = self.current_quest
        if final:
            hero.gain_experience(quest.reward_experience + self.reward_experience)
        else:
            hero.gain_experience(quest.reward_experience)
        self.journal.notification = self

    def activate(self, hero):
        """Run super's activate using locations of local variables."""
        super().activate(self.current_quest.trigger, hero)

    def run(self):
        """Special handler method over ride.

        In this case run the local 'advance()' method.
        And then handle possible completion which means either
        deactivate if completed or update the current trigger.
        """
        self.advance()
        super().run(self.current_quest.trigger)


class Quest(Base):
    """A class to describe quest objects that can be stored in a database.
    
    
    Final stage is when next_quests == [].
    Initial stage is when past_quests == [].
    
    Useful note: Relationships are set ... but a commit must occur
    between adding in each new element.
    """
    __tablename__ = "quest"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(200))
    reward_experience = Column(Integer)
    position = Column(Integer)

    # Relationships
    # QuestPath many to many
    quest_paths = relationship(
        "QuestPath",
        secondary=quest_path_to_quest,
        back_populates='quests'
    )

    # Triggers Each Quest has a completion trigger. Each trigger can
    # complete multiple quests?
    # One to Many? (Later will be many to many).
    trigger_id = Column(Integer, ForeignKey('trigger.id'))
    trigger = relationship("Trigger")

    def __init__(self, name, description=name, reward_experience=3,
                 trigger=None):
        """Build a new Quest object.
        
        You can link this quest to other quests at initialization or afterwards.
        quest.next_quests.append(quest2) does the same thing.
        """
        
        self.name = name
        self.description = description
        self.reward_experience = reward_experience
        self.trigger = trigger


# class Primary_Quest(Quest):
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)

"""
Journal specification.

A journal should be able to store data on (triggered events).
Such as quest completion or beast encountered or map areas explored.

    A database table linking to object data.
    A comment on each event.

e.g. #1
    Quest Log
    -"Get acquainted with the Blacksmith Quest" completed @ 15:30 - 2017/11/08

    (click quest name to get more info about the quest)

e.g. #2
    Map Log
    -Found Blacksmith in Thornwall @ 15:25 - 2017/11/08

    (Click location names for more info)

So maybe:
    -object
    -info/description of event
    -time + date

Journal is almost a Frontend for lots of other objects?

Project breakdown:

1. Design backend for quests
    -build to allow for type checking/instanceOf checking
    -build to allow quest_path.description property
    -build to describe what happens when you click on the current quest in a
        quest_path. I quest it would bring up info on the current quest?

2. Design backend for persons
3. Design backend for places
4. Design backend for beasts

5. Design frontend for quests
    -pull data from the current quest in the questpath and the questpath itself
6. Design frontend for person
7. Design frontend for places
8. Design frontend for beasts

9. Design event system link-in.
    -Journal entries should be populated by the occurrence of events
"""
from datetime import datetime

from flask import render_template_string
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Boolean, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import orm
from sqlalchemy.orm import column_property
from sqlalchemy import select, and_
from sqlalchemy.ext.orderinglist import ordering_list

from base_classes import Base
from achievements import Achievements
from quests import QuestPath
# For testing
import pdb

# journal_quest_path_association_table = Table(
#     'journal_quest_path_association',
#     Base.metadata,
#     Column('journal_id', Integer, ForeignKey('journal.id',
#                                              ondelete="SET NULL")),
#     Column('quest_path_id', Integer, ForeignKey('quest_path.id',
#                                                 ondelete="SET NULL"))
# )


# I think I can combine the entry and Journal.
# This would give me custom places such as beasts or quests in the Journal
# The add_entry would sort the new objects into the right category.
class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Hero to Journal is One to One
    hero_id = Column(Integer, ForeignKey('hero.id',
                                         ondelete="CASCADE"))
    hero = relationship(
        "Hero",
        back_populates='journal',
        cascade="all, delete-orphan",
        single_parent=True)

    # Journal to QuestPath is One to Many
    # QuestPath provides many special methods.
    quest_paths = relationship("QuestPath", back_populates='journal',
                               cascade="all, delete-orphan",
                               foreign_keys="[QuestPath.journal_id]",
                               order_by="QuestPath.name")

    _current_quest_paths = relationship(
        "QuestPath",
        primaryjoin="and_(Journal.id==QuestPath.journal_id, "
                    "QuestPath.completed==False)",
        cascade="all, delete-orphan",
        order_by="QuestPath.name"
    )

    @property
    def current_quest_paths(self):
        return self._current_quest_paths

    _notifications = relationship(
        "Entry",
        back_populates="journal",
        order_by="Entry.position",
        collection_class=ordering_list('position'),
        cascade="all, delete-orphan")

    @property
    def notifications(self):
        return Journal.MockNotificationOrderingList(self)

    @notifications.setter
    def notifications(self, value):
        """Assign to self._notifications directly.

        I'm not totally sure this is enough. If you passed in a list of items ...
        it might be best to vet them and make sure that they are actually
        Entry objects.
        """
        self._notifications = value

    class MockNotificationOrderingList:
        def __init__(self, journal):
            self.journal = journal

        def append(self, item):
            self.journal._notifications.append(Entry(item))

        def insert(self, index, entity):
            self.journal._notifications.insert(index, Entry(entity))

        def __iter__(self):
            return self.journal._notifications.__iter__()

        def __repr__(self):
            return self.journal._notifications.__repr__()

        def __getattribute__(self, item):
            # pdb.set_trace()
            if item in ['append', 'insert', 'journal']:
                return object.__getattribute__(self, item)
            else:
                return self.journal._notifications.__getattribute__(item)


    # Journal to Achievements is One to One.
    achievements = relationship("Achievements", back_populates="journal",
                                uselist=False,
                                cascade="all, delete-orphan")

    # @property
    # def quest_notification(self):
    #     return self.notification.get_description()

    @validates('quest_paths')
    def validate_quest_path(self, key, quest_path):
        """Overload quest_path assignment.

        Build a new path if current one is a template.
        Activate the current_quest as well.
        """
        if quest_path.template:
            quest_path = quest_path.clone()
        self.notifications.append(quest_path)
        # self.notifications.append(Entry(quest_path))
        return quest_path

    def __init__(self):
        self.achievements = Achievements()

        # This will let you create an entry object using an instantiated journal
        # hero.journal.notifications.append(hero.journal.Entry(some_object))

    # Each journal can have many entries
    # entries = relationship("Entry", back_populates='journal')

    # def add_entry(self, obj):
    #     entry = Entry(obj, datetime.now(), obj.description)
    #     self.entries.append(entry)


class Entry(Base):
    """Various entries into the Journal class.

    For the Notifications:
        each object should have a get_description method.
    So you can do:
    for obj in journal.notifications:
        obj.get_description()
    """
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)

    timestamp = Column(DateTime)
    position = Column(Integer)
    info = Column(String(50))
    name = Column(String(50))
    description = Column(String(200))
    type = Column(String(50))

    # relationships
    journal_id = Column(Integer, ForeignKey('journal.id', ondelete="CASCADE"))
    journal = relationship("Journal", back_populates='_notifications')

    # Each entry can have object (beast, person or place)
    # I may need to build the inverse of the relationship ... not positive
    # though.
    # _beast = relationship()
    # _person = relationship()
    # _place = relationship("Location")
    _beast = Column(String(50))
    _person = Column(String(50))
    _place = Column(String(50))
    _quest_path = relationship("QuestPath")
    _quest_path_id = Column(Integer, ForeignKey('quest_path.id'))

    @hybrid_property
    def obj(self):
        """Return whichever object has a connection with this one."""
        # pdb.set_trace()
        return self._beast or self._person or self._place or self._quest_path

    @obj.setter
    def obj(self, value):
        """Assign object to appropriate column.

        From @elthran - not implemented
        That’s simple. I’m going to do about 4 types:
        - quest
        - achievement
        - friend message
        - generic notice (like level up)
        """
        # dir(value)
        # pdb.set_trace()
        if value.__tablename__ == "beast":
            self._beast = value
            self.type = "beast"
        elif value.__tablename__ == "person":
            self._person = value
            self.type = "person"
        elif value.__tablename__ == "quest_path":
            self._quest_path = value
            self.type = "quest_path"
        else:
            raise "TypeError: 'obj' does not accept " \
                  "__tablename__ '{}':".format(value.type)

    def __init__(self, obj):
        # pdb.set_trace()
        self.obj = obj
        self.name = obj.name
        self.description = obj.description

    # all of these can be way more generic and get there data from files.
    # Could even add this code in the the into the 'obj.setter' code.
    @property
    def header(self):
        header_template = None
        if self.type == "quest_path":
            header_template = """
                {% if quest_notification.total_reward %}
                    {{ quest_notification.name }}
                {% else %}
                    {{ quest_notification.name }} ({{ quest_notification.stage }} / {{ quest_notification.stages }})
                {% endif %}
            """
        return render_template_string(header_template, quest_notification=self.obj.get_description())

    @property
    def body(self):
        body_template = None
        if self.type == "quest_path":
            body_template = """
                {% if quest_notification.total_reward %}
                    Completed!
                {% else %}
                    Required: {{ quest_notification.current_quest.name }}
                {% endif %}
            """

        return render_template_string(body_template,
                                      quest_notification=self.obj.get_description())

    @property
    def footer(self):
        footer_template = None
        if self.type == "quest_path":
            footer_template = """
                {% if quest_notification.total_reward %}
                    Total reward: {{ quest_notification.total_reward }}xp
                {% else %}
                    Reward: {{ quest_notification.current_quest.reward }}xp
                {% endif %}
            """
        return render_template_string(footer_template,
                                      quest_notification=self.obj.get_description())

    @property
    def url(self):
        url_template = "/quest_log"
        return render_template_string(url_template)

    @property
    def redirect_message(self):
        url_template = "Click anywhere in this box to visit your journal."
        return render_template_string(url_template)


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

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from base_classes import Base

# For testing
import pdb


# I think I can combine the entry and Journal.
# This would give me custom places such as beasts or quests in the Journal
# The add_entry would sort the new objects into the right category.
class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Hero to Journal is One to One
    hero = relationship("Hero", uselist=False, back_populates='journal')

    # Journal to QuestPath is One to Many
    # QuestPath provides many special methods.
    quest_paths = relationship("QuestPath", back_populates='journal',
                               foreign_keys="[QuestPath.journal_id]")

    notification = relationship("QuestPath",
                                foreign_keys="[QuestPath.notification_id]",
                                uselist=False)

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
            quest_path = quest_path.build_new_from_template()
        quest_path.activate(self.hero)
        self.notification = quest_path
        return quest_path

    # Each journal can have many entries
    # entries = relationship("Entry", back_populates='journal')

    # def add_entry(self, obj):
    #     entry = Entry(obj, datetime.now(), obj.description)
    #     self.entries.append(entry)


# class Entry(Base):
#     __tablename__ = 'entry'
#
#     id = Column(Integer, primary_key=True)
#
#     timestamp = Column(DateTime)
#     info = Column(String)
#
#     # relationships
#     journal_id = Column(Integer, ForeignKey('journal.id'))
#     journal = relationship("Journal", back_populates='entries')
#
#     # Each entry can have object (beast, person or place)
#     # I may need to build the inverse of the relationship ... not positive
#     # though.
#     _beast = relationship()
#     _person = relationship()
#     _place = relationship("Location")
#     _quest_path = relationship("QuestPath")
#
#     @hybrid_property
#     def obj(self):
#         return self._beast or self._person or self._place or self._quest_path
#
#     @obj.setter
#     def obj(self, value):
#         """Assign object to appropriate column."""
#         dir(value)
#         pdb.set_trace()
#         if value.type == "beast":
#             self._beast = value
#         elif value.type == "person":
#             self._person = value
#         elif value.type == "quest_path":
#             self._quest_path = value
#         else:
#             raise "TypeError: 'obj' does not accept " \
#                   "type '{}':".format(value.type)

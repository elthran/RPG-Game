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
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from base_classes import Base

# For testing
import pdb


class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)

    # Each journal can have many entries
    entries = relationship("Entry", back_populates='journal')

    def add_entry(self, obj):
        entry = Entry(obj, datetime.now(), obj.description)
        self.entries.append(entry)


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)

    timestamp = Column(DateTime)
    info = Column(String)

    # relationships
    journal_id = Column(Integer, ForeignKey('journal.id'))
    journal = relationship("Journal", back_populates='entries')

    # Each entry can have object (beast, person or place)
    # I may need to build the inverse of the relationship ... not positive
    # though.
    _beast = relationship()
    _person = relationship()
    _place = relationship("Location")
    _quest_path = relationship("QuestPath")

    @hybrid_property
    def obj(self):
        return self._beast or self._person or self._place or self._quest_past

    @obj.setter
    def obj(self, value):
        """Assign object to appropriate column."""
        dir(value)
        pdb.set_trace()
        if value.type == "beast":
            self._beast = value
        elif value.type == "person":
            self._person = value
        elif value.type == "quest_path":
            self._quest_path = value
        else:
            raise "TypeError: 'obj' does not accept " \
                  "type '{}':".format(value.type)


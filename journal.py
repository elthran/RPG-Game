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

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from base_classes import Base


class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)

    # Each journal can have many entries
    entry = relationship()

    def add_entry(self, obj):
        self.entry.obj = obj
        self.entry.timestamp = datetime.now()
        self.entry.info = obj.description


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)

    timestamp = Column(DateTime)
    info = Column(String)

    #Each entry can have one beast
    _beast = relationship()

    @property
    def obj(self):
        if obj.type == "Beast":
            self._beast = obj

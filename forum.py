from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True)
    threads = []

    def create_thread(self, thread):
        self.threads.append(thread)

class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    posts = []
    creator = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, title="unnamed thread", creator="None", timestamp="Unknown Time"):
        self.title = title
        self.creator = creator
        self.timestamp = timestamp

    def write_post(self, post):
        self.posts.append(post)

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    def __init__(self, content):
        self.content = content

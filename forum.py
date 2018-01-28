import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Many to One with Thread
    threads = relationship("Thread", back_populates="forum")

    def create_thread(self, thread):
        self.threads.append(thread)


class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    forum_id = Column(Integer, ForeignKey('forum.id'))
    forum = relationship("Forum", back_populates="threads")

    # Many to One with Posts
    posts = relationship("Post", back_populates="thread")

    title = Column(String)
    creator = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, title="unnamed thread", creator="None"):
        self.title = title
        self.creator = creator
        self.timestamp = datetime.datetime.utcnow()

    def write_post(self, post):
        self.posts.append(post)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to Many with Thread.
    thread_id = Column(Integer, ForeignKey('thread.id'))
    thread = relationship("Thread", back_populates="posts")

    content = Column(String)
    author = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, content="Error: Content missing", author="Unknown author"):
        self.content = content
        self.author = author
        self.timestamp = datetime.datetime.utcnow()

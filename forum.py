import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from base_classes import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True)

    name = Column(String(50))

    # Relationships
    # Many to One with Category
    boards = relationship("Board", back_populates="forum",
                          cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def create_board(self, board):
        self.boards.append(board)


class HumanReadableMixin(object):
    def human_readable_time(self):
        """Human readable datetime string.

        See https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior

        Currently returns formatted like:
        Jan. 28 1:17pm
        """
        return self.timestamp.strftime("%b. %d %I:%M%p")


class Board(HumanReadableMixin, Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    forum_id = Column(Integer, ForeignKey('forum.id', ondelete="CASCADE"))
    forum = relationship("Forum", back_populates="boards")

    # Many to One with Threads
    threads = relationship("Thread", back_populates="board",
                           cascade="all, delete-orphan")

    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def create_thread(self, thread):
        self.threads.append(thread)

    def get_post_count(self):
        return sum((len(thread.posts) for thread in self.threads))

    @hybrid_property
    def most_recent_post(self):
        return max((thread.most_recent_post
                    for thread in self.threads
                    if thread.most_recent_post),
                   key=lambda p: p.timestamp, default=None)

    def get_most_recent_post(self):
        """Return a Post object that is the most recent among all threads.

        Should return a Post object. It should query the database for the most
        recent post which is a property of this board
        ie.
        for thread in self.threads:
             for post in thread.posts:
                  find most recent
        """

        return self.most_recent_post


class Thread(HumanReadableMixin, Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    board_id = Column(Integer, ForeignKey('board.id', ondelete="CASCADE"))
    board = relationship("Board", back_populates="threads")

    # Many to One with Posts
    posts = relationship("Post", back_populates="thread",
                         cascade="all, delete-orphan")

    @hybrid_property
    def most_recent_post(self):
        return max((post for post in self.posts), key=lambda p: p.timestamp,
                   default=None)

    name = Column(String(50))
    creator = Column(String(50))
    description = Column(String(200))
    category = Column(String(50))
    timestamp = Column(DateTime)
    views = Column(Integer)

    def __init__(self, name="unnamed thread", creator="None", description="", category="General"):
        self.name = name
        self.creator = creator.title()
        self.description = description
        self.category = category
        self.timestamp = datetime.datetime.utcnow()
        self.views = 0

    def write_post(self, post):
        self.posts.append(post)


class Post(HumanReadableMixin, Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)

    # Relationships
    # One to Many with Thread.
    thread_id = Column(Integer, ForeignKey('thread.id', ondelete="CASCADE"))
    thread = relationship("Thread", back_populates="posts")

    # One to Many with User class.
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    user = relationship("User", back_populates="posts")

    content = Column(String(50))

    @hybrid_property
    def author(self):
        return self.user.username

    timestamp = Column(DateTime)

    def __init__(self, content="Error: Content missing", user=None):
        self.content = content
        self.user = user
        self.timestamp = datetime.datetime.utcnow()


import datetime

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.hybrid

import models


class Forum(models.Base):
    __tablename__ = 'forum'

    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String(50))

    # Relationships
    # Many to One with Category
    boards = sa.orm.relationship("Board", back_populates="forum", cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def create_board(self, board):
        self.boards.append(board)


class Board(models.mixins.HumanReadableTimeMixin, models.Base):
    __tablename__ = "board"

    id = sa.Column(sa.Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    forum_id = sa.Column(sa.Integer, sa.ForeignKey('forum.id', ondelete="CASCADE"))
    forum = sa.orm.relationship("Forum", back_populates="boards")

    # Many to One with Threads
    threads = sa.orm.relationship("Thread", back_populates="board", cascade="all, delete-orphan")

    name = sa.Column(sa.String(50))

    def __init__(self, name):
        self.name = name

    def create_thread(self, thread):
        self.threads.append(thread)

    def get_post_count(self):
        return sum((len(thread.posts) for thread in self.threads))

    @sa.ext.hybrid.hybrid_property
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


class Thread(models.mixins.HumanReadableTimeMixin, models.Base):
    __tablename__ = "thread"

    id = sa.Column(sa.Integer, primary_key=True)

    # Relationships
    # One to many with Forum
    board_id = sa.Column(sa.Integer, sa.ForeignKey('board.id', ondelete="CASCADE"))
    board = sa.orm.relationship("Board", back_populates="threads")

    # Many to One with Posts
    posts = sa.orm.relationship("Post", back_populates="thread", cascade="all, delete-orphan")

    @sa.ext.hybrid.hybrid_property
    def most_recent_post(self):
        return max((post for post in self.posts), key=lambda p: p.timestamp,
                   default=None)

    name = sa.Column(sa.String(50))
    creator = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))
    category = sa.Column(sa.String(50))
    views = sa.Column(sa.Integer)

    def __init__(self, name="unnamed thread", creator="None", description="", category="General"):
        self.name = name
        self.creator = creator.title()
        self.description = description
        self.category = category
        self.timestamp = datetime.datetime.utcnow()
        self.views = 0

    def write_post(self, post):
        self.posts.append(post)


class Post(models.mixins.HumanReadableTimeMixin, models.Base):
    __tablename__ = "post"

    id = sa.Column(sa.Integer, primary_key=True)

    # Relationships
    # One to Many with Thread.
    thread_id = sa.Column(sa.Integer, sa.ForeignKey('thread.id', ondelete="CASCADE"))
    thread = sa.orm.relationship("Thread", back_populates="posts")

    # One to Many with User class.
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id', ondelete="CASCADE"))
    account = sa.orm.relationship("Account", back_populates="posts")

    content = sa.Column(sa.String(50))

    @sa.ext.hybrid.hybrid_property
    def author(self):
        return self.user.username

    def __init__(self, content="Error: Content missing", user=None):
        self.content = content
        self.user = user
        self.timestamp = datetime.datetime.utcnow()

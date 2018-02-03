# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
# Author: Elthran B, Jimmy Zhang                                              #
# Email : jimmy.gnahz@gmail.com                                               #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

"""Objects used in the database and the game.

Suggestion: change name to game_objects.py
"""
import pdb

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base
from inbox import Inbox


class Game(object):
    def __init__(self, hero=None):
        self.hero = hero
        self.has_enemy = False
        self.global_chat_user_list = {}
        self.global_chat = []  # I am not sure if this should goin database? Just very temporary chat log that all users can see

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.has_enemy = True

    def set_hero(self, hero):
        self.hero = hero


class User(Base):
    """User class holds data about the current gamer.

    This is database ready and connects to the Hero class.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    timestamp = Column(DateTime)
    is_admin = Column(Boolean)
    inbox_alert = Column(Boolean)
    prestige = Column(Integer)

    # Relationships
    # Each user can have one inbox. One to One (bidirectional).
    inbox_id = Column(Integer, ForeignKey('inbox.id'))
    inbox = relationship("Inbox", back_populates="user")

    # Many heroes -> one user
    heroes = relationship("Hero", order_by='Hero.character_name',
                          back_populates='user')

    # Many to One with Posts
    posts = relationship("Post", order_by="Post.timestamp.desc()",
                         back_populates="user")

    def __init__(self, username, password, email='', timestamp=None, is_admin=False):
        """Create a new user object.

        The user gets special privileges if it is an admin.
        """

        self.inbox = Inbox()

        self.username = username
        self.password = password
        self.email = email
        self.timestamp = timestamp
        self.is_admin = is_admin
        self.inbox_alert = False
        self.prestige = 0

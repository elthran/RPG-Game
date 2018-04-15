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

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Unicode
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base
from inbox import Inbox

from random import random

class Game(object):
    def __init__(self, hero=None):
        self.hero = hero
        self.has_enemy = False
        # The two below may need to be in the database? I'm not sure. Will need to see how they work with multiple users.
        self.global_chat_user_list = {}
        self.global_chat = []

    def set_hero(self, hero):
        self.hero = hero


class User(Base):
    """User class holds data about the current gamer.

    This is database ready and connects to the Hero class.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(Unicode(200, convert_unicode=False), nullable=False)
    email = Column(Unicode(200, convert_unicode=False))
    reset_key = Column(Unicode(200, convert_unicode=False))
    timestamp = Column(DateTime)
    is_admin = Column(Boolean)
    inbox_alert = Column(Boolean)
    prestige = Column(Integer)
    avatar = Column(String(50))
    signature = Column(String(50))

    # Relationships
    # Each user can have one inbox. One to One (bidirectional).
    inbox = relationship("Inbox", back_populates="user", uselist=False,
                         cascade="all, delete-orphan")

    # Many heroes -> one user
    heroes = relationship("Hero", order_by='Hero.character_name',
                          back_populates='user',
                          cascade="all, delete-orphan")

    # Many to One with Posts
    posts = relationship("Post", order_by="Post.timestamp.desc()",
                         back_populates="user", cascade="all, delete-orphan")

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
        self.avatar = "0"
        self.signature = "No signature"

class Notification(object):
    def send_notification(title="Attention!", content="Something interesting has happened.", url="/home"):
        return None

def round_number_intelligently(number):
    """This will round a number based on its closeness to the next number. So (1.4) has a 40% chance to be rounded to a (2).
    It returns an integer."""
    new_amount = int(number) + (random() < number - int(number))
    return new_amount


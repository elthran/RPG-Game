import sqlalchemy as sa
import sqlalchemy.orm as orm
from . import base_classes
from . import inbox


class Account(base_classes.Base):
    """User class holds data about the current gamer.

    This is database ready and connects to the Hero class.
    """
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    password = sa.Column(sa.Unicode(200, convert_unicode=False), nullable=False)
    email = sa.Column(sa.Unicode(200, convert_unicode=False))
    reset_key = sa.Column(sa.Unicode(200, convert_unicode=False))
    timestamp = sa.Column(sa.DateTime)
    is_admin = sa.Column(sa.Boolean)
    inbox_alert = sa.Column(sa.Boolean)
    prestige = sa.Column(sa.Integer)
    avatar = sa.Column(sa.String(50))
    signature = sa.Column(sa.String(50))

    # Relationships
    # Each user can have one inbox. One to One (bidirectional).
    inbox = orm.relationship("Inbox", back_populates="user", uselist=False,
                         cascade="all, delete-orphan")

    # Many heroes -> one user
    heroes = orm.relationship(
        "Hero", order_by='Hero.character_name',
        back_populates='user',
        cascade="all, delete-orphan")

    # Many to One with Posts
    posts = orm.relationship(
        "Post", order_by="Post.timestamp.desc()",
        back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username, password, email='', timestamp=None, is_admin=False):
        """Create a new user object.

        The user gets special privileges if it is an admin.
        """

        self.inbox = inbox.Inbox()

        self.username = username
        self.password = password
        self.email = email
        self.timestamp = timestamp
        self.is_admin = is_admin
        self.inbox_alert = False
        self.prestige = 0
        self.avatar = "0"
        self.signature = "No signature"

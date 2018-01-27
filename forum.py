from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True)
    all_threads = []
    all_posts = []

    # Relationships
    # Unknown

    # The forum can have many posts One to Many
    # Unknown

    """
    def create_thread(self, thread):
        # Not implemented yet
        self.all_threads.append(thread)
        """

    def write_post(self, thread, content):
        """Create a message between the inbox's user and another user.

        A database commit must take place after this method or the
        message won't stay in existence?

        Basically ... the user is in a current session so when
        you add create a message (with bidirectional relationships)
        The Message is automatically added to both users inboxes.
        To save you need to commit.

        So in app.py you will call:
        user.inbox.send_message(other_user, content)
        """
        self.all_posts.append([thread, content])

class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    posts = []

    # Relationships
    # Each user can send or receive multiple messages. One to Many (bi).
    #...

    def __init__(self, title="unnamed thread"):
        """A message between two users with some content.

        Both the sender and receiver are User objects.
        The content is a (formatted?) string of text.
        """
        self.content = title

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    thread = Column(String)
    content = Column(String)

    # Relationships
    # Each user can send or receive multiple messages. One to Many (bi).
    #...

    def __init__(self, thread, content):
        """A message between two users with some content.

        Both the sender and receiver are User objects.
        The content is a (formatted?) string of text.
        """
        self.thread = thread
        self.content = content

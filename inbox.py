from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base


class Inbox(Base):
    __tablename__ = 'inbox'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Each inbox has a single user. One to One (bidirectional).
    user = relationship("User", uselist=False, back_populates='inbox')

    # Each inbox can have many sent messages One to Many
    sent_messages = relationship("Message", back_populates='sender',
                                 foreign_keys="[Message.sender_id]")
    received_messages = relationship("Message", back_populates='receiver',
                                     foreign_keys="[Message.receiver_id]")

    def get_sent_messages(self):
        """Return a list of all sent messages.

        These methods can be used for additional functionality
        such as sorting. NotImplemented!

        You can just use:
            user.inbox.sent_messages
        """
        return self.sent_messages

    def get_received_messages(self):
        """Return a list of all received messages.

        These methods can be used for additional functionality
        such as sorting. NotImplemented!

        You can just use:
            user.inbox.received_messages
        """
        return self.received_messages

    def send_message(self, receiver, content, time):
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
        Message(self, receiver.inbox, content, time)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    content = Column(String(50))
    unread = Column(Boolean)

    # Relationships
    # Each user can send or receive multiple messages. One to Many (bi).
    sender_id = Column(Integer, ForeignKey('inbox.id'))
    sender = relationship("Inbox", back_populates="sent_messages",
                          foreign_keys="[Message.sender_id]")
    receiver_id = Column(Integer, ForeignKey('inbox.id'))
    receiver = relationship("Inbox", back_populates="received_messages",
                            foreign_keys="[Message.receiver_id]")

    timestamp = Column(String(50))

    def __init__(self, sender, receiver, content, time):
        """A message between two users with some content.

        Both the sender and receiver are User objects.
        The content is a (formatted?) string of text.
        """
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.unread = True
        self.timestamp = time[:19]

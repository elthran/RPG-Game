import sqlalchemy as sa
import sqlalchemy.orm

import services.time
import models


class ChatLog(models.Base):
    games = sa.orm.relationship("Game", back_populates='chat_log')
    chat_messages = sa.orm.relationship("ChatMessage", order_by='ChatMessage.timestamp.desc()')

    # TODO convert this to a query if possible?
    def active_chatters(self):
        names = [message.sender_name for message in self.chat_messages]
        unique_names = []
        for name in names:
            if name not in unique_names:
                unique_names.append(name)
        return sorted(unique_names)


class ChatMessage(models.Base):
    sender_name = sa.Column(sa.String(50))
    message = sa.Column(sa.String(200))
    timestamp = sa.Column(sa.DateTime)

    # Relationships
    sender_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id'))
    sender = sa.orm.relationship("Hero")

    chat_log_id = sa.Column(sa.Integer, sa.ForeignKey('chat_log.id'))

    def __init__(self, sender, message):
        self.sender = sender
        self.sender_name = sender.name
        self.message = message
        self.timestamp = services.time.now()

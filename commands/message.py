import flask

import models


def get_message_content_and_sender_by_id(hero, data):
    """Return the content of a message based on its id."""
    message = models.Message.get(data['id'])
    message.unread = False  # Marks the message as having been seen by the receiver
    return flask.jsonify(messageContent=message.content, messageSender=message.sender.account.username)

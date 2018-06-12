import pdb

import models


def check_messages(hero):
    """Deactivate glowing inbox alert.

    Your inbox alert will no longer glow until a new message is sent to you,
    even if you don't open all your letters.
    """

    hero.account.inbox_alert = False


def delete_messages_by_id(ids):
    """Delete all messages with passed ids.

    I don't understand what synchronize_session="fetch" does ...
    """
    models.Message.query.filter(models.Message.id.in_(ids)).delete(synchronize_session='fetch')


def reply_to_message(sender, message_id, content):
    """Reply to a message by id."""
    message = models.Message.get(message_id)
    receiver = message.sender.account
    sender.account.inbox.send_message(receiver, content)
    receiver.inbox_alert = True


def send_message(sender, receiver_name, content):
    """Send message to other user."""

    receiver = models.Account.filter_by(username=receiver_name).one()
    if receiver:
        sender.account.inbox.send_message(receiver, content)
        receiver.inbox_alert = True
    else:
        raise "Receiver {} does not exist.".format(receiver_name)

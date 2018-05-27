import services.time
import models


def remove_old_messages(outdated_in_minutes=5):
    """Delete chat messages that are older than 5 minutes old."""

    models.ChatMessage.query.filter(models.ChatMessage.timestamp <= services.time.different_from_now_by(minutes=-outdated_in_minutes)).delete()


def add_new_message_to_log(chat_log, sender, message):
    """Inserts at the beginning of the chat list.

    Contains the senders's name and the message.
    Messages is inserted at the beginning so as not to mess up ordering
    by newest timestamp first.
    """
    chat_log.chat_messages.insert(0, models.ChatMessage(sender, message))


def prune_messages(chat_log, maxsize=25):
    """Prune messages when there are more than maxsize.

    Since chat_messages is sorted by timestamp this should delete the oldest
    messages first.
    """
    if len(chat_log.chat_messages) > maxsize:
            entry = chat_log.chat_messages.pop()
            models.ChatMessage.filter_by(id=entry.id).delete()

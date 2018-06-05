from .commands import *
from .message import get_message_content_and_sender_by_id
from .notification import send_notification_data
from .change_tooltip import change_path_tooltip, change_quest_tooltip


def cmd_functions(name):
    """Use to refer to return a function from string of its name.

    Getattr wrapper ...
    """
    return globals()[name]

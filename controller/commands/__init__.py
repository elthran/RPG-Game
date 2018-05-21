from .message import get_message_content_and_sender_by_id
from .commands import *


def cmd_functions(name):
    """Use to refer to return a function from string of its name.

    Getattr wrapper ...
    """
    return globals()[name]

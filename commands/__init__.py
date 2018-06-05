import pdb

from .commands import *
from .message import get_message_content_and_sender_by_id
from .notification import send_notification_data
from .change_tooltip import change_path_tooltip, change_quest_tooltip
from .toggle_equip import toggle_equip


def cmd_functions(name):
    """Use to refer to return a function from string of its name.

    Getattr wrapper ...
    """
    try:
        return globals()[name]
    except KeyError as ex:
        raise Exception("You need to write a function called '{}' in commands/ package and import it into the commands.__init__.py file.".format(name))

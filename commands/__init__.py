import pdb

from .commands import *
from .message import get_message_content_and_sender_by_id
from .notification import send_notification_data
from .change_tooltip import change_path_tooltip, change_quest_tooltip
from .toggle_equip import toggle_equip
from .change_ability_tooltip import change_ability_tooltip
from .update_specialization_tooltip import update_specialization_tooltip
from .update_ability import update_ability
from .update_specialization import update_specialization
from .change_proficiency_tooltip import change_proficiency_tooltip
from .update_proficiency import update_proficiency
from .change_attribute_tooltip import change_attribute_tooltip
from .update_attribute import update_attribute
from .change_avatar import change_avatar
from .change_signature import change_signature
from .verify_password import verify_password
from .verify_email import verify_email


def cmd_functions(name):
    """Use to refer to return a function from string of its name.

    Getattr wrapper ...
    """
    try:
        return globals()[name]
    except KeyError as ex:
        raise Exception("You need to write a function called '{}' in commands/ package and import it into the commands.__init__.py file.".format(name))

import warnings

#
# def clear_quest_notification(hero, database, arg_dict, **kwargs):
#     id = arg_dict.get('data', None, type=int)
#     hero.journal.quest_notification = None
#     return "success"


def temp_temp(hero, arg_dict, **kwargs):
    """Jacobs function which does nothing. I seem to need to have A function, so sometimes I run this blank function."""
    warnings.warn("Instead of using this, do sendToPy(event, jsFunct) or something like that :P maybe use 'null' a few times.", DeprecationWarning)
    return "success"

#
# def send_message_to_user_by_username(hero, database, arg_dict, **kwargs):
#     """Return the content of a message based on its id."""
#     username = arg_dict.get('data', None, type=str)
#     print ("username is: ", username)
#     print("Attempting to generate a reply. Getting user now.")
#     receiver = database.get_user_by_username(username)
#     print("Generating reply to user: ", receiver.username)
#     hero.account.inbox.send_message(receiver, "TEST REPLY!", "55:55:55")
#     print ("Reply is successful. Message sent.")
#     print("Sending message content back to JS.")
#     return "message replied to successfully"

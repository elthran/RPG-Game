import models


def get_user_id(username):
    """Return the id of the user by username from the User's table.

    """
    user = models.Account.filter_by(username=username).first()
    if user is None:
        return None
    return user.id

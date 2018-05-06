import models
import services


def register(username, password, email_address, session={}):
    # See if new_username has a valid input.
    # This only works if they are creating an account
    if not services.fetcher.get_user_id(username):
        user = add_new_user(username, password, email=email_address)
        hero = add_new_hero_to_user(user)
        session['logged_in'] = True
        user.heroes[0].creation_phase = True  # At this point only one hero should exist
        return True
    return False


def add_new_user(username, password, email=''):
    """Create a new user account with this username and password.

    And optional email.

    The password is encrypted with bcrypt.
    The email is encrypted separately with bcrypt.
    """

    # hash and save a password
    user = models.Account(username=username, password=services.secrets.encrypt(password), email=services.secrets.encrypt(email), timestamp=services.time.now())
    models.Base.session.add(user)
    return user


def add_new_hero_to_user(user):
        """Create a new blank character object for a user.

        May not be future proof if a user has multiple heroes.
        """
        hero = models.Hero(user=user)
        models.Base.session.add(hero)
        return hero

import models
import services.fetcher


def register_account(username, password, email_address, session):
    # See if new_username has a valid input.
    # This only works if they are creating an account
    if not services.fetcher.get_user_id(username):
        account = add_new_account(username, password, email=email_address)
        hero = add_new_hero_to_account(account)
        session['logged_in'] = True
        account.heroes[0].creation_phase = True  # At this point only one hero should exist
        return True
    return False


def add_new_account(username, password, email=''):
    """Create a new account with this username and password.

    And optional email.

    The password is encrypted with bcrypt.
    The email is encrypted separately with bcrypt.
    """

    # hash and save a password
    account = models.Account(username=username, password=services.secrets.encrypt(password), email=services.secrets.encrypt(email), timestamp=services.time.now())
    models.Base.session.add(account)
    return account


def add_new_hero_to_account(account):
        """Create a new blank hero object for this account.

        May not be future proof if a user has multiple heroes.
        """
        hero = models.Hero(account=account)
        models.Base.session.add(hero)
        hero.journal.quest_paths = models.QuestPath.filter_by(is_default=True, template=True).all()
        hero.current_world = models.Location.filter_by(name="Htrae", type="map").one()
        hero.current_location = models.Location.filter_by(name="Old Man's Hut", type="building").one()
        return hero


def close_hero_creation_phase(hero):
    """Finalize and close the hero creation phase.

    Prevent the account from returning to the character creation page.
    """
    hero.creation_phase = False
    hero.refresh_character(full=True)

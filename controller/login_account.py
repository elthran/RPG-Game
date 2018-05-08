import services
import models


def login_account(username, password, session):
    """Log the account in if the password matches.

    This updates the session variable.
    NOTE:
        The validate method runs a password migration script internally.
    Check for data_migration 'reset_key' ... if exists use old style
    password validation ... then convert password to new style.
    Otherwise, we are just logging in normally
    """
    if services.validation.validate(username, password):
        session['logged_in'] = True
        session['id'] = models.Account.filter_by(username=username).one().id

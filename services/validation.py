import models
import services.migration
import services.secrets


def validate(username, password):
    """Check if password if valid for user.

    Check for data_migration 'reset_key' ... if exists use old style
    password validation ... then convert password to new style.
    """
    # session.query(User).filter_by
    account = models.Account.filter_by(username=username).first()
    if account is not None:
        services.migration.attempt_password_migration(account, password)
        # check a password
        return services.secrets.check_cypher(password, account.password)
    return None


def validate_email(username, email):
    """Check if the passed email matches the email for this account.

    Email is encrypted separately. You can't decrypt the email even
    if you know the user name. This might be inconvenient at some point.
    """
    user = models.Account.filter_by(username=username).first()
    if user is not None:
        # check a password
        return services.secrets.check_cypher(email, user.email)
    return None

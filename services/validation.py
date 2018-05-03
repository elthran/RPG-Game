import models
import services


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

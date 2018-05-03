import hashlib
import services


def attempt_password_migration(account, password):
    """Update password to new style if valid.

    If account has reset key, and valid old style password.
    """
    if account.reset_key and user.password == hashlib.md5(password.encode()).hexdigest():
        account.password = services.secrets.encrypt(password)
        account.reset_key = None

import os
import base64
import hashlib

import services.validation
import services.sender
import services.time
import services.secrets
import models


def reset_account_via_email(username, email_address, url_root):
    if services.validation.validate_email(username, email_address):
        key = setup_account_for_reset(username)
        services.sender.send_email(username, email_address, key, url_root)
        return True
    return False


def setup_account_for_reset(username):
    """Add a reset key to the account and return it."""
    account = models.Account.filter_by(username=username).first()
    key = os.urandom(256)
    key = base64.urlsafe_b64encode(hashlib.sha256(key).digest())
    urlsafe_key = str(key)[2:-2]
    account.reset_key = urlsafe_key
    account.reset_timeout = services.time.timeout_in(minutes=5)
    return urlsafe_key


def reset_account(username, password):
    """Reset an account. Deactivate reset process."""
    account = models.Account.filter_by(username=username).one()
    account.reset_key = None
    account.reset_timeout = None
    account.password = services.secrets.encrypt(password)

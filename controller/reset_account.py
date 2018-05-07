import os
import base64
import hashlib

import services
import models


def reset_account_via_email(username, email_address, url_root, session):
    if services.validation.validate_email(username, email_address):
        key = setup_account_for_reset(username)
        services.sender.send_email(username, email_address, key, url_root)

        # TODO used for async reset at some point ... somehow.
        session['reset_in_progress'] = True
        # async_process(rest_key_timelock, args=(database, username), kwargs={'timeout': 5})
        return True
    return False


def setup_account_for_reset(username):
    """Add a reset key to the user account and return it."""
    user = models.Account.filter_by(username=username).first()
    key = os.urandom(256)
    key = base64.urlsafe_b64encode(hashlib.sha256(key).digest())
    urlsafe_key = str(key)[2:-2]
    user.reset_key = urlsafe_key
    return urlsafe_key

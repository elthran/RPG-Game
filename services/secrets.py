import os
import base64
import hashlib

import bcrypt


def encrypt(s):
    """Encrypt a string with the builtin hash cost."""
    return bcrypt.hashpw(
        base64.b64encode(hashlib.sha256(s.encode()).digest()),
        bcrypt.gensalt(os.environ.get('PASSWORD_HASH_COST')))


def check_cypher(plain, cypher):
    """Check if a string matches the cypher string.

    You can use this to check if password is valid.
    It encrypts the plain text variant and compares it to the cypher text one.
    """
    return bcrypt.checkpw(
            base64.b64encode(hashlib.sha256(plain.encode()).digest()),
            cypher.encode())

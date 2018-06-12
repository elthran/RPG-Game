import re

import flask


def verify_email(hero, data=None, *args, **kwargs):
    address_to_verify = data['email']
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address_to_verify)
    if match is None:
        print('Bad Syntax')
        success = "no"
        message = "Not a valid email address."
    else:
        print('Good Syntax')
        success= "yes"
        message = "Valid email address."
    return flask.jsonify(success=success, message=message, button="email", field="1", fields=1)

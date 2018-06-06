import flask


def verify_password(hero, data=None, *args, **kwargs):
    field = data['field']
    password = data['password']
    password2 = data['password2']
    if len(password) < 5:
        success = "no"
        message = "Password is too short. It requires a minimum of 5 characters."
    elif password != password2:
        success = "no"
        message = "Passwords don't match. The two new passwords you enter must be exactly the same."
        if field != "2":
            field = "0"
    else:
        success = "yes"
        message = "Passwords match!"
    return flask.jsonify(success=success, message=message, button="password", field=field, fields=2)

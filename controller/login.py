import services


def login(username, password, session={}):
    # The validate method runs a password migration script internally.
    # Check for data_migration 'reset_key' ... if exists use old style
    # password validation ... then convert password to new style.
    # Otherwise, we are just logging in normally
    if services.validation.validate(username, password):
        session['logged_in'] = True

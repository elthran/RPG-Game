import flask as fl
from elthranonline import app
import services


@app.route('/')
def main():
    """Redirects user to a default first page

    Currently the login page.
    """
    return fl.redirect(fl.url_for('login'))


# use decorators to link the function to a url
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # Should prevent contamination between logging in with 2 different
    # accounts.
    fl.session.clear()  # I'm not sure this is still a good idea ..
    # pprint(session)
    # I might remove this later ...
    # This fixed a bug in the server that I have now fixe with
    # if 'logged_in' in session and session['logged_in']
    fl.session['logged_in'] = False

    username = fl.request.form['username'] if 'username' in fl.request.form else ""
    password = fl.request.form['password'] if 'password' in fl.request.form else ""
    email_address = fl.request.form['email'] if 'email' in fl.request.form else ""

    if fl.request.method == 'POST':
        if fl.request.form['type'] == "login":
            # The validate method runs a password migration script internally.
            # Check for data_migration 'reset_key' ... if exists use old style
            # password validation ... then convert password to new style.
            # Otherwise, we are just logging in normally
            import pdb; pdb.set_trace()
            if services.validation.validate(username, password):
                fl.session['logged_in'] = True
            # Marked for upgrade, consider checking if user exists
            # and redirect to account creation page.
            else:
                error = 'Invalid Credentials.'
        elif fl.request.form['type'] == "register":
            # See if new_username has a valid input.
            # This only works if they are creating an account
            if services.fetcher.get_user_id(username):
                error = "Username already exists!"
            else:
                user = database.add_new_user(username, password, email=email_address)
                database.add_new_hero_to_user(user)
                fl.session['logged_in'] = True
                user.heroes[0].creation_phase = True  # At this point only one hero should exist
        elif fl.request.form['type'] == "reset":
            print("Validating email address ...")
            if database.validate_email(username, email_address):
                print("Trying to send mail ...")
                key = database.setup_account_for_reset(username)
                send_email(username, email_address, key)
                # async_process(rest_key_timelock, args=(database, username), kwargs={'timeout': 5})
        else:
            raise Exception("The form of this 'type' doesn't exist!")

        if 'logged_in' in fl.session and fl.session['logged_in']:
            fl.flash("LOG IN SUCCESSFUL")
            user = database.get_user_by_username(username)
            fl.session['id'] = user.id
            # Will barely pause here if only one character exists.
            # Maybe should just go directly to home page.
            return fl.redirect(fl.url_for('choose_character'))

    return fl.render_template('index.html', error=error, username=username)

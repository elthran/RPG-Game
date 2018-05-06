import flask as fl

from elthranonline import app

import services
import controller


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
            controller.login(username, password, fl.session)
            # Marked for upgrade, consider checking if user exists
            # and redirect to account creation page.
            if not fl.session['logged_in']:
                error = 'Invalid Credentials.'
        elif fl.request.form['type'] == "register":
            # See if new_username is a valid input.
            # This only works if they are creating an account
            controller.register(username, password, email_address, fl.session)
            if not fl.session['logged_in']:
                error = "Username already exists!"
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

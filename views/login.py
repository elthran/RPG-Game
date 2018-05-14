import flask

from elthranonline import app
import controller


@app.route('/')
def main():
    """Redirects user to a default first page

    Currently the login page.
    """
    return flask.redirect(flask.url_for('login'))


# use decorators to link the function to a url
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # Should prevent contamination between logging in with 2 different
    # accounts.
    flask.session.clear()  # I'm not sure this is still a good idea ..
    # pprint(session)
    # I might remove this later ...
    # This fixed a bug in the server that I have now fixed with
    # if 'logged_in' in session and session['logged_in']
    flask.session['logged_in'] = False

    username = flask.request.form.get('username', '', type=str)
    password = flask.request.form.get('password', '', type=str)
    email_address = flask.request.form.get('email', '', type=str)

    if flask.request.method == 'POST':
        if flask.request.form['type'] == "login":
            controller.login.login_account(username, password, flask.session)
            # Marked for upgrade, consider checking if user exists
            # and redirect to account creation page.
            if not flask.session['logged_in']:
                error = 'Invalid Credentials.'
        elif flask.request.form['type'] == "register":
            # See if new_username is a valid input.
            # This only works if they are creating an account
            controller.register_account(username, password, email_address, flask.session)
            if not flask.session['logged_in']:
                error = "Username already exists!"
        elif flask.request.form['type'] == "reset":
            print("Validating email address ...")
            resetting = controller.reset_account_via_email(username, email_address, flask.request.url_root, flask.session)
            if resetting:
                print("Trying to send mail ...")
        else:
            raise Exception("The form of this 'type' doesn't exist!")

        if 'logged_in' in flask.session and flask.session['logged_in']:
            flask.flash("LOG IN SUCCESSFUL")
            # Will barely pause here if only one character exists.
            # Maybe should just go directly to home page.
            return flask.redirect(flask.url_for('choose_character'))

    return flask.render_template('index.html', error=error, username=username)

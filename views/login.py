import flask as fl

from elthranonline import app

import services
import controller

import pdb


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

    username = fl.request.form.get('username', '', type=str)
    password = fl.request.form.get('password', '', type=str)
    email_address = fl.request.form.get('email', '', type=str)

    if fl.request.method == 'POST':
        if fl.request.form['type'] == "login":
            controller.login.login_account(username, password, fl.session)
            # Marked for upgrade, consider checking if user exists
            # and redirect to account creation page.
            if not fl.session['logged_in']:
                error = 'Invalid Credentials.'
        elif fl.request.form['type'] == "register":
            # See if new_username is a valid input.
            # This only works if they are creating an account
            controller.register_account(username, password, email_address, fl.session)
            if not fl.session['logged_in']:
                error = "Username already exists!"
        elif fl.request.form['type'] == "reset":
            print("Validating email address ...")
            resetting = controller.reset_account_via_email(username, email_address, fl.request.url_root, fl.session)
            if resetting:
                print("Trying to send mail ...")
        else:
            raise Exception("The form of this 'type' doesn't exist!")

        if 'logged_in' in fl.session and fl.session['logged_in']:
            fl.flash("LOG IN SUCCESSFUL")
            # Will barely pause here if only one character exists.
            # Maybe should just go directly to home page.
            return fl.redirect(fl.url_for('choose_character'))

    return fl.render_template('index.html', error=error, username=username)

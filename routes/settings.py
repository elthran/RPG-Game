import flask

from elthranonline import app
import services.decorators
import services.validation
import services.secrets


@app.route('/settings/<tab>/<choice>', methods=['GET', 'POST'])
@services.decorators.uses_hero
def settings(hero=None, tab="profile", choice="none"):
    message = None
    if flask.request.method == 'POST':
        if flask.request.form['type'] == "update_password":
            if services.validation.validate(hero.account.username, flask.request.form['old_password']):
                new_password = flask.request.form['new_password']
                account = hero.account
                account.password = services.secrets.encrypt(new_password)
                message = "Password changed!"
            else:
                print("wrong password!")
                message = "You entered the wrong password. Password change failed."
        elif flask.request.form['type'] == "update_email":
            email = flask.request.form['new_email']
            hero.account.email = services.secrets.encrypt(email)
            message = "Email address changed to: " + email
    return flask.render_template('settings.html', page_title="Settings", hero=hero, account=hero.account, tab=tab, choice=choice, message=message)

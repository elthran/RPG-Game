import flask

from elthranonline import app
import models
import controller


@app.route('/add_new_character')
def add_new_character():
    account = models.Account.get(flask.session['id'])
    controller.setup_account.add_new_hero_to_account(account)
    return flask.redirect(flask.url_for('choose_character'))

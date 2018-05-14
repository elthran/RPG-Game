import flask

from elthranonline import app
import services.decorators
import services.secrets
import services.validation
import models


@app.route("/reset", methods=["GET", "POST"])
def reset_password():
    if flask.request.method == "GET":
        if services.validation.validate_reset(flask.request.args['account'], flask.request.args['key']):
            return flask.render_template("reset.html", username=flask.request.args['account'], key=flask.request.args['key'])
    elif flask.request.method == "POST":
        if services.validation.validate_reset(flask.request.form['username'], flask.request.form['key']):
            account = models.Account.filter_by(username=flask.request.form['username']).one()
            if account.reset_key:
                account.reset_key = None
                account.password = services.secrets.encrypt(flask.request.form['password'])
                return flask.redirect(flask.url_for('login'), code=307)
    return flask.redirect(flask.url_for('login'))


@app.route('/reset_character/<stat_type>')
@services.decorators.login_required
@services.decorators.uses_hero
def reset_character(stat_type, hero=None):
    hero.age = 7
    hero.experience = 0
    hero.experience_maximum = 10
    hero.renown = 0
    hero.virtue = 0
    hero.devotion = 0
    hero.gold = 5000
    hero.basic_ability_points = 5
    hero.archetype_ability_points = 5
    hero.calling_ability_points = 5
    hero.pantheon_ability_points = 5
    hero.attribute_points = 10
    hero.proficiency_points = 10
    return flask.redirect(flask.url_for('home'))  # return a string

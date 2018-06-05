import flask

from elthranonline import app
import services.decorators
import services.secrets
import services.validation
import controller
import models


@app.route("/reset", methods=["GET", "POST"])
def reset_password():
    if flask.request.method == "GET":
        return flask.render_template("reset.html", username=flask.request.args['account'], key=flask.request.args['key'])
    elif flask.request.method == "POST":
        # Maybe make account auto reset after 3 failed tries too?
        if services.validation.validate_reset(flask.request.form['username'], flask.request.form['key']):
            controller.reset_account(flask.request.form['username'], flask.request.form['password'])
            return flask.redirect(flask.url_for('login'), code=307)
    return flask.redirect(flask.url_for('login'))


@app.route('/reset_character/<stat_type>')
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

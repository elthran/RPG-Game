import flask

from elthranonline import app
import models
import controller
import services.decorators
import services.filters


@app.route('/choose_character', methods=['GET', 'POST'])
@services.decorators.login_required
def choose_character():
    account = models.Account.get(flask.session['id'])
    # print(account)
    # exit("testing choose character.")
    hero = None
    if len(account.heroes) == 1:
        hero = account.heroes[0]
    elif flask.request.method == 'POST':
        hero = models.Hero.get(flask.request.form['hero_id'])
    else:
        return flask.render_template('choose_character.html', account=account)

    controller.login.login_hero(hero, flask.session)
    flask.flash(hero.login_alerts)
    hero.login_alerts = ""
    # If it's a new character, send them to create_character url
    # pdb.set_trace()
    if hero.creation_phase:
        return flask.redirect(flask.url_for('create_character'))
    # If the character already exist go straight the main home page!
    return flask.redirect(flask.url_for('home'))

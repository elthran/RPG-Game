import flask

from elthranonline import app
import services.decorators


@app.route('/spar/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def spar(name='', hero=None, location=None):
    """Spar with local?

    Routes from barracks.
    """
    spar_cost = 50
    spar_benefit = 5
    if hero.gold < spar_cost:
        location.display.page_heading = "You do not have enough gold to spar."
    else:
        hero.gold -= spar_cost

        # This gives you experience and also returns how much
        # experience you gained
        modified_spar_benefit = hero.gain_experience(spar_benefit)
        hero.base_proficiencies['endurance'].current -= 1
        location.display.page_heading = \
            "You spend some time sparring with the trainer at the barracks." \
            " You spend {} gold and gain {} experience.".format(
                spar_cost, modified_spar_benefit)
    return flask.render_template('generic_location.html', hero=hero)  # return a string

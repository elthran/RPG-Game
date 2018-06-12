import flask

from elthranonline import app
import services.decorators


@app.route('/proficiencies', methods=['GET', 'POST'])
@services.decorators.uses_hero
def proficiencies(hero=None):
    """This gets called anytime you have secondary attribute points to spend
    Currently I send "proficiencies=True" so that the html knows to highlight
    the bar and show that you are on this page.

    This page is literally just a html page with tooltips and proficiency
    level up buttons. No python code is needed. Python only tells html which
    page to load.
    """
    return flask.render_template('profile_proficiencies.html', page_title="Proficiencies", hero=hero, all_attributes=hero.attributes, all_proficiencies=hero.base_proficiencies)

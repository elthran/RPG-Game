import flask

from elthranonline import app
import services.decorators


@app.route('/attributes', methods=['GET', 'POST'])
@services.decorators.uses_hero
def attributes(hero=None):
    """This gets called anytime you have attribute points to spend

    Currently I send "attributes=True" so that the html knows to highlight
    the bar and show that you are on this page
    """

    return flask.render_template('profile_attributes.html', page_title="Attributes", hero=hero, all_attributes=hero.attributes)

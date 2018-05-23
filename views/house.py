import flask

from elthranonline import app
import services.decorators
import models


@app.route('/house/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
def house(name='', hero=None):
    """A web page for a house.

    Returns a rendered html page.
    """
    location = models.Location.filter_by(name=name).one()
    return flask.render_template('generic_location.html', hero=hero)

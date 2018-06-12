import flask

from elthranonline import app
import services.decorators


@app.route('/under_construction')
@services.decorators.uses_hero
def under_construction(hero=None):
    page_title = "Under Construction"
    return flask.render_template('layout.html', page_title=page_title, hero=hero)

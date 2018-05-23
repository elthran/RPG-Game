import pdb

import flask

from elthranonline import app
import services.decorators
import models


@app.route('/gate/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
def leave_town(name='', hero=None):
    location = models.Location.filter_by(name=name).one()
    # conversation = [
    #     ("City Guard: ", "You are too young to be out on your own.")]
    # page_links = [
    #     ("Return to the ", "/Town/" + hero.current_city.name, "city", ".")]
    pdb.set_trace()
    return flask.render_template('gate.html', hero=hero, page_heading=location.display.page_heading)  #, conversation=conversation, page_links=page_links)  # return a string

import flask

from elthranonline import app
import services.decorators
import services.fetcher


@app.route('/map/<name>')
@app.route('/town/<name>')
@app.route('/dungeon/<name>')
@app.route('/explorable/<name>')
@services.decorators.update_current_location
def move(name='', hero=None, location=None):
    """Set up a directory for the hero to move to.

    Arguments are in the form of a url and are sent by the data that can be
    found with the 'view page source' command in the browser window.
    """
    if location.type == 'map':
        # location.pprint() # Why do we have this? For debugging :P
        other_heroes = []
    else:
        other_heroes = services.fetcher.get_other_heroes_at_current_location(hero)

    return flask.render_template(
        'move.html',
        hero=hero,
        page_title=location.display.page_title,
        page_heading=location.display.page_heading,
        page_image=location.display.page_image,
        paragraph=location.display.paragraph,
        people_of_interest=other_heroes,
        places_of_interest=location.places_of_interest)

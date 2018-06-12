import flask

from elthranonline import app
import services.decorators


@app.route('/home')
@services.decorators.uses_hero
def home(hero=None):
    """Build the home page and return it as a string of HTML.

    render_template uses Jinja2 markup.
    """

    # Is this supposed to update the time of all hero objects?
    # database.update_time(hero)

    # Not implemented. Control user moves on map.
    # Sets up initial valid moves on the map.
    # Should be a list of urls ...
    # session['valid_moves'] \
    #  = hero.current_world.show_directions(hero.current_location)
    # session['valid_moves'].append(hero.current_location.id)

    return flask.render_template(
        'profile_home.html', page_title="Profile", hero=hero, profile=True,
        proficiencies=hero.get_summed_proficiencies())

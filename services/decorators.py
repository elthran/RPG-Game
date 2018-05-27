import functools

import flask

import models
import services.event_service


def login_required(f):
    """Set certain pages as requiring a login to visit.

    This should redirect you to the login page."""

    @functools.wraps(f)
    def wrap_login(*args, **kwargs):
        if 'logged_in' in flask.session and flask.session['logged_in']:
            return f(*args, **kwargs)
        else:
            flask.flash('You need to login first.')
            return flask.redirect(flask.url_for('login'))

    return wrap_login


def uses_hero(f):
    """Preload hero object and save it afterwards.

    Note: KeyError occurs when this method is called before login method
    has been run. Also after a POST request before page reload.
    Seems wipe the session cookie temporarily? Fine after normal page load
    Only fails if view page source after POST.
    """

    @functools.wraps(f)
    def wrap_uses_hero(*args, **kwargs):
        try:
            # print("Currently at the uses_hero function!")
            hero = models.Hero.get(flask.session["hero_id"])
        except KeyError as ex:
            if not flask.session:
                # After making a POST request with AJAX the session
                # gets cleared? Until you make a new GET request?
                # This is a request for the Page Source and it occurs
                # in a new blank session.
                return "After POST request reload the page to view source."
            else:
                raise ex
        return f(*args, hero=hero, **kwargs)
    return wrap_uses_hero


def update_current_location(f):
    """Load the location object and set it to hero.current_location.

    NOTE: this must come after "@uses_hero"
    Adds a keyword argument 'location' to argument list.

    Example usage:
    @app.route('/barracks/<name>')
    @login_required
    @uses_hero
    @update_current_location
    def barracks(name='', hero=None, location=None):
        if hero.proficiencies.health.current <= 0:
            location.display.page_heading = "Your hero is currently dead."
    """

    @functools.wraps(f)
    def wrap_current_location(*args, **kwargs):
        hero = kwargs['hero']
        location = models.locations.Location.query.filter_by(name=kwargs['name']).one()
        hero.current_location = location

        # TODO make a controller function.
        if location not in hero.journal.known_locations:
            hero.journal.known_locations.append(location)

        services.event_service.spawn(
            'move_event',
            hero,
            description="{} visits {}.".format(hero.name, location.url)
        )
        return f(*args, location=location, **kwargs)

    return wrap_current_location

import flask

from elthranonline import app
import services.decorators


@app.route('/barracks/<name>')
@services.decorators.update_current_location
def barracks(name='', hero=None, location=None):
    # This will be removed soon.
    # Dead heroes wont be able to move on the map and will immediately get
    # moved to a hospital until they heal. So locations won't need to factor
    # in the "if"of the hero being dead
    places_of_interest = location.places_of_interest
    if hero.base_proficiencies['health'].current <= 0:
        page_heading = "Your hero is currently dead."
        page_image = "dead.jpg"
        places_of_interest['children'] = None
        places_of_interest['siblings'] = None
        places_of_interest['parent'] = hero.last_city
        paragraph = "You have no health."
    else:
        page_heading = "Welcome to the barracks {}!".format(
            hero.name)
        page_image = "barracks.jpg"
        paragraph = "Battle another player."

    return flask.render_template('generic_location.html', page_heading=page_heading, page_image=page_image, places_of_interest=places_of_interest, paragraph=paragraph, hero=hero)

import flask

from elthranonline import app
import services.decorators
import services.fetcher
import controller.questing


@app.route('/building/<name>')
@services.decorators.update_current_location
def building(name='', hero=None, location=None):
    """Currently runs old man's hut"""
    other_heroes = services.fetcher.get_other_heroes_at_current_location(hero)
    if name == "Old Man's Hut":  # TODO this should be a trigger/event
        controller.questing.add_quest_path_to_hero(hero, "Get Acquainted with the Blacksmith")
    return flask.render_template('move.html', hero=hero, page_title=location.display.page_title, page_heading=location.display.page_heading, page_image=location.display.page_image, paragraph=location.display.paragraph, people_of_interest=other_heroes, places_of_interest=location.places_of_interest)

import flask

from elthranonline import app
import services.decorators
import services.fetcher


@app.route('/building/<name>')
@services.decorators.update_current_location
def building(name='', hero=None, location=None):
    """Currently runs old man's hut"""
    other_heroes = services.fetcher.get_other_heroes_at_current_location(hero)
    if name == "Old Man's Hut":
        blacksmith_path_name = "Get Acquainted with the Blacksmith"
        if not services.fetcher.hero_has_quest_path_named(hero, blacksmith_path_name):
            print("Adding new quests!")
            blacksmith_path = services.fetcher.get_quest_path_template(blacksmith_path_name)
            hero.journal.quest_paths.append(blacksmith_path)
        else:
            print("Hero has path of that name, ignoring ..")

    return flask.render_template('move.html', hero=hero, page_title=location.display.page_title, page_heading=location.display.page_heading, page_image=location.display.page_image, paragraph=location.display.paragraph, people_of_interest=other_heroes, places_of_interest=location.places_of_interest)

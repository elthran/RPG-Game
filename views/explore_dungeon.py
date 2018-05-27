import random

import flask

from elthranonline import app
import services.decorators
import services.generators
import models


@app.route('/explore_dungeon/<name>/<extra_data>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon(name='', hero=None, location=None, extra_data=None):
    """
    NOTE: @elthran You shouldn't modify location data as this will modify it for all heroes/users in the game.
    Instead just pass this data to the template directly.
    (Marlen)

    Routes from '/inside_dungeon'
    """

    # For convenience
    page_heading = "Current Floor of dungeon: " + str(hero.journal.achievements.current_dungeon_floor)
    if extra_data == "Entering":  # You just arrived into the dungeon
        page_heading += "You explore deeper into the dungeon!"
        page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
        return flask.render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links, page_heading=page_heading)
    if extra_data == "Item":
        # The problem here is that when you see an item .. you have already
        # picked it up.
        # I think you need to use a different order of operations.
        # Like put the "add item" after the "pick up item" part
        discovered_item = services.generators.get_random_item()
        page_heading = "You find an item in the dungeon! It's a {}".format(discovered_item.name)
        hero.inventory.add_item(discovered_item)
        page_links = [("Pick up the ", "/explore_dungeon/Explore%20Dungeon/None", "item", ".")]
        return flask.render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links, page_heading=page_heading)
    encounter_chance = random.randint(0, 100)
    if hero.random_encounter_monster:  # You have a monster waiting for you from before
        page_heading += "The monster paces in front of you."
        monsters = models.Hero.filter_by(is_monster=True).all()  # This should be a saved monster and not re-generated :(
        monster = services.generators.generate_monster(monsters)
        page_links = [("Attack the ", "/battle/monster", "monster", "."),
                      ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
    else:  # You continue exploring
        hero.journal.achievements.current_dungeon_floor_progress += 1
        if encounter_chance > (100 - (hero.journal.achievements.current_dungeon_floor_progress*4)):
            hero.journal.achievements.current_dungeon_floor += 1
            if hero.journal.achievements.current_dungeon_floor > hero.journal.achievements.deepest_dungeon_floor:
                hero.journal.achievements.deepest_dungeon_floor = hero.journal.achievements.current_dungeon_floor
            hero.journal.achievements.current_dungeon_floor_progress = 0
            page_heading = "You descend to a deeper level of the dungeon!! Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
            page_links = [("Start ", "/explore_dungeon/Explore%20Dungeon/None", "exploring", " this level of the dungeon.")]
        elif encounter_chance > 35:  # You find a monster! Oh no!
            monsters = models.Hero.filter_by(is_monster=True).all()
            monster = services.generators.generate_monster(monsters)

            page_heading += "You come across a terrifying monster lurking in the shadows."
            hero.current_dungeon_monster = True
            page_links = [("Attack the ", "/battle/monster", "monster", "."),
                          ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
        elif encounter_chance > 15:  # You find an item!
            page_heading += "You find something shiny in a corner of the dungeon."
            page_links = [("", "/explore_dungeon/Explore%20Dungeon/Item", "Investigate", " the light's source.")]
        else:
            page_heading += " You explore deeper into the dungeon!"
            page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
    page_heading += " Current progress on this floor: {}".format(hero.journal.achievements.current_dungeon_floor_progress)
    return flask.render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links, page_heading=page_heading)  # return a string

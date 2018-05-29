import random

import flask

from elthranonline import app
import services.decorators
import services.generators
import models


# From /dungeon
@app.route('/dungeon_entrance/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def dungeon_entrance(name='', hero=None, location=None):
    hero.journal.achievements.current_dungeon_floor = 0
    hero.current_dungeon_progress = 0
    hero.random_encounter_monster = False
    # explore_dungeon = database.get_object_by_name('Location', 'Explore Dungeon')
    # location.children = [explore_dungeon]
    return flask.render_template('generic_location.html', hero=hero, game=hero.game)  # return a string


@app.route('/explore_dungeon/<name>/entering')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon_entering(name='', hero=None, location=None):
    """Entering the dungeon."""
    page_heading = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
    page_heading += " You explore deeper into the dungeon!"
    page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading)


@app.route('/explore_dungeon/<name>/item/<action>/<int:id>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon_item(name='', hero=None, location=None, action=None, id_=None):
    """Approaching, finding and picking up an item."""

    page_heading = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)

    if action == 'approaching':  # Approaching item.
        page_heading += "You find something shiny in a corner of the dungeon."
        page_links = [("", "/explore_dungeon/Explore%20Dungeon/item", "Investigate", " the light's source.")]
    elif action == 'finding':  # Finding item.
        discovered_item = services.generators.get_random_item()
        page_heading = "You find an item in the dungeon! It's a {}".format(discovered_item.name)
        page_links = [("Pick up the ", "/explore_dungeon/Explore%20Dungeon/item/picking_up/{}".format(discovered_item.id), "item", ".")]
    elif action == 'picking_up':  # picking up item
        # The problem here is that when you see an item .. you have already
        # picked it up.
        # I think you need to use a different order of operations.
        # Like put the "add item" after the "pick up item" part
        discovered_item = models.Item.get(id_)
        hero.inventory.add_item(discovered_item)
        return flask.redirect(flask.url_for('explore_dungeon'))
    else:
        raise Exception("Route '{}' doesn't exist.".format(action))
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading)


@app.route('/explore_dungeon/<name>/encounter')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon_encounter(name='', hero=None, location=None, extra_data=None):
    """Encountering a new or old monster."""
    page_heading = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
    if hero.random_encounter_monster:  # You have a monster waiting for you from before
        page_heading += "The monster paces in front of you."
        monsters = models.Hero.filter_by(is_monster=True).all()  # This should be a saved monster and not re-generated :(
        monster = services.generators.generate_monster(monsters)
        page_links = [("Attack the ", "/battle/monster", "monster", "."),
                      ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
    else:
        monsters = models.Hero.filter_by(is_monster=True).all()
        monster = services.generators.generate_monster(monsters)

        page_heading += "You come across a terrifying monster lurking in the shadows."
        hero.current_dungeon_monster = True
        page_links = [("Attack the ", "/battle/monster", "monster", "."),
                      ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading)


@app.route('/explore_dungeon/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon(name='', hero=None, location=None):
    """Visualize exploring a dungeon.

    NOTE: @elthran You shouldn't modify location data as this will modify it for all heroes/users in the game.
    Instead just pass this data to the template directly.
    (Marlen)

    Routes from '/inside_dungeon'
    """
    page_heading = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)

    encounter_chance = random.randint(0, 100)

    # You continue exploring
    achieve = hero.journal.achievements

    # Refactor first if and else clause ... seem the same?
    if encounter_chance > (100 - achieve.current_dungeon_floor_progress*4):
        achieve.current_dungeon_floor += 1
        achieve.deepest_dungeon_floor = max(achieve.deepest_dungeon_floor, achieve.current_dungeon_floor)
        page_heading = "You descend to a deeper level of the dungeon!! Current Floor of dungeon: {}".format(achieve.current_dungeon_floor)
        page_links = [("Start ", "/explore_dungeon/Explore%20Dungeon/None", "exploring", " this level of the dungeon.")]
    elif encounter_chance > 35:  # You find a monster! Oh no!
        return flask.redirect(flask.url_for('explore_dungeon_encounter'))
    elif encounter_chance > 15:  # You find an item!
        return flask.redirect(flask.url_for('explore_dungeon_item'))
    else:  # You explore but don't find a lower level ..?
        page_heading += " You explore deeper into the dungeon!"
        page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]

    # Not sure where this should go?
    page_heading += " Current progress on this floor: {}".format(hero.journal.achievements.current_dungeon_floor_progress)
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading)  # return a string

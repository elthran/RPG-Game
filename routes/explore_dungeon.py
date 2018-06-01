import pdb
import random

import flask

from elthranonline import app
import services.decorators
import services.generators
import controller.explore_dungeon
import models


# From /dungeon
@app.route('/dungeon_entrance/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def dungeon_entrance(name='', hero=None, location=None):
    dialogues = controller.explore_dungeon.setup_explore_dungeon(hero)
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, dialogues=dialogues)  # return a string


# Considering removing entirely ...
@app.route('/explore_dungeon/<name>/entering')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon_entering(name='', hero=None, location=None):
    """Entering the dungeon."""

    page_heading = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
    page_heading += " You explore deeper into the dungeon!"
    page_links = [("Walk deeper into the", "{}".format(hero.current_location.url), "dungeon", ".")]
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading)


@app.route('/explore_dungeon/item/<action>/<int:id_>')
@services.decorators.login_required
@services.decorators.uses_hero
def explore_dungeon_item(hero=None, action=None, id_=None):
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


@app.route('/explore_dungeon/encounter/<monster_name>')
@services.decorators.login_required
@services.decorators.uses_hero
def explore_dungeon_encounter(hero=None, monster_name=None):
    """Encountering a new or old monster."""
    page_heading = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
    if hero.random_encounter_monster:  # You have a monster waiting for you from before
        paragraph = "The monster paces in front of you."
        monsters = models.Hero.filter_by(is_monster=True).all()  # This should be a saved monster and not re-generated :(
        monster = services.generators.generate_monster(monsters)
    else:
        paragraph = "You come across a terrifying monster lurking in the shadows."
        monsters = models.Hero.filter_by(is_monster=True).all()
        monster = services.generators.generate_monster(monsters)
        hero.current_dungeon_monster = True
    page_links = [("Attack the ", "/battle/monster", "monster", "."), ("Attempt to ", hero.current_location.parent.url, "flee", ".")]
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading, paragraph=paragraph)


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
    achieve.current_floor_progress += 1  # Always explore more ..

    # Refactor first if and else clause ... seem the same?
    if encounter_chance > (100 - achieve.current_floor_progress*4):
        achieve.current_dungeon_floor += 1
        achieve.deepest_dungeon_floor = max(achieve.deepest_dungeon_floor, achieve.current_dungeon_floor)
        page_heading = "You descend to a deeper level of the dungeon!! Current Floor of dungeon: {}".format(achieve.current_dungeon_floor)
        page_links = [("Start ", "/explore_dungeon/Explore%20Dungeon/None", "exploring", " this level of the dungeon.")]
    elif encounter_chance > 35:  # You find a monster! Oh no!
        return flask.redirect(flask.url_for('explore_dungeon_encounter', monster_name="generate"))
    elif encounter_chance > 15:  # You find an item!
        return flask.redirect(flask.url_for('explore_dungeon_item', name=name, action='approaching', id_=0))
    else:  # You explore but don't find a lower level ..?
        page_heading += " You explore deeper into the dungeon!"
        page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon", "dungeon", ".")]

    # Not sure where this should go?
    page_heading += " Current progress on this floor: {}".format(hero.journal.achievements.current_floor_progress)
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, page_links=page_links, page_heading=page_heading)  # return a string

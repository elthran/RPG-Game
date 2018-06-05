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


@app.route('/explore_dungeon/item/<action>')
@services.decorators.login_required
@services.decorators.uses_hero
def explore_dungeon_item(hero=None, action=None):
    """Approaching, finding and picking up an item."""

    progress, dialogues = controller.explore_dungeon.explore_item(hero, action)
    if not dialogues:
        return flask.redirect(flask.url_for('explore_dungeon', name=hero.current_location.name))
    return flask.render_template('dungeon_exploring.html', hero=hero, game=hero.game, dialogues=dialogues, progress=progress)


@app.route('/explore_dungeon/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def explore_dungeon(name='', hero=None, location=None):
    """Visualize exploring a dungeon."""

    progress, dialogues = controller.explore_dungeon.explore_dungeon(hero)
    if not dialogues:
        return flask.redirect(flask.url_for('explore_dungeon_item', action='approaching', id_=0))
    return flask.render_template('dungeon_exploring.html', hero=hero, dialogues=dialogues, paragraph=progress)  # return a string

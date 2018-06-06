import flask

import models


def update_proficiency(hero, data=None, *args, **kwargs):
    """Raise proficiency level, decrement proficiency_points.

    Return status of: success, hide_all, hide_this.
    "success" means hide none ... maybe I should call it that instead?
    """
    proficiency_id = data['id']
    proficiency = models.proficiencies.Proficiency.get(proficiency_id)

    # Defensive coding: command buttons should be hidden by JavaScript
    # when no longer valid due to the return values of this function.
    # If for some reason they are still clickable return error to
    # JS console.
    if hero.proficiency_points <= 0 or proficiency.is_max_level:
        return "error: no proficiency_points or proficiency is at max level."

    hero.proficiency_points -= 1
    proficiency.level_up()
    return flask.jsonify(tooltip=proficiency.tooltip, pointsRemaining=hero.proficiency_points, level=proficiency.level)

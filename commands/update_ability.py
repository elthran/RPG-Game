import flask

import models


def update_ability(hero, data=None, *args, **kwargs):
    ability_id = data['id']
    ability = models.abilities.Ability.get(ability_id)
    points_remaining = 0
    if ability.tree == "Basic":
        if hero.basic_ability_points <= 0 or ability.is_max_level():
            return "error: no basic_ability_points or ability is at max level."
        hero.basic_ability_points -= 1
        points_remaining = hero.basic_ability_points
    elif ability.tree == "Archetype":
        if hero.archetype_ability_points <= 0 or ability.is_max_level():
            return "error: no archetype_ability_points or ability is at max level."
        hero.archetype_ability_points -= 1
        points_remaining = hero.archetype_ability_points
    else:
        return "error: code not built for ability.tree == {}".format(ability.type)
    ability.level += 1 # Should be a level_up() function instead?
    return flask.jsonify(tooltip=ability.tooltip, pointsRemaining=points_remaining, level=ability.level)

import flask

import models


def change_ability_tooltip(hero, data=None, *args, **kwargs):
    ability = models.abilities.Ability.get(data['id'])
    return flask.jsonify(tooltip=ability.tooltip)

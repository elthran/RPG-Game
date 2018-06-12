import flask

import models


def change_proficiency_tooltip(hero, data=None, *args, **kwargs):
    prof_id = data['id']
    proficiency = models.proficiencies.Proficiency.get(prof_id)
    return flask.jsonify(tooltip=proficiency.tooltip)

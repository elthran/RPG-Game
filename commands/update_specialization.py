from pprint import pprint

import flask

import models


def update_specialization(hero, data=None, *args, **kwargs):
    spec_id = data['id']
    specialization = models.Specialization.get(spec_id)
    hsa = hero.specialization_access[spec_id]
    if hsa.disabled:
        return "error: Attempted to add locked specialization to hero."
    # spec.level += 1 or something?

    # You can ignore templating here as hero takes care of it.
    hero.specializations = specialization
    pprint(hero.specializations)
    # spec = data['spec']
    # PLEASE MAKE THE ABOVE PRINT STATEMENT TRUE!!!!!!!!!!!!!!!!!!!!!!!
    # specialization = database.get_object_by_name("Specialization", choice)
    # setattr(hero.specializations, choice, specialization)
    return flask.jsonify(tooltip="Temp", pointsRemaining=0, level=0)

import flask

import models


def update_specialization_tooltip(hero, data=None, *args, **kwargs):
    if data['id']:
        spec = models.Specialization.get(data['id'])
        if data['id'] in hero.specialization_access:
            hsa = hero.specialization_access[data['id']]
            if hsa.disabled:
                hsa.disabled = hsa.check_locked(hero)
        else:
            hsa = None
        return flask.jsonify(description=spec.description, requirements=spec.requirements, disabled=hsa.disabled if hsa else True, id=spec.id)
    return flask.jsonify(description="Unknown", requirements="Unknown", disabled=True, id=0)

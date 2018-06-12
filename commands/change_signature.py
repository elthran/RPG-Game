import flask


def change_signature(hero, data=None, *args, **kwargs):
    signature = data['signature']
    name = data['name']
    hero.account.signature = signature
    return flask.jsonify(name=name)

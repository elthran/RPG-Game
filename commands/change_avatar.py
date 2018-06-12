import flask


def change_avatar(hero, data=None, *args, **kwargs):
    avatar = data['id']
    name = data['name']
    hero.account.avatar = avatar
    return flask.jsonify(name=name)

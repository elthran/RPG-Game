import flask

import models


# This should be combined with function below when I know how to pass a path.id
# I don't think these should be combined ... I'm trying to work out how to restrict Player access to the database ... (Marlen)
def change_path_tooltip(hero, data=None, *args, **kwargs):
    path = models.QuestPath.get(data['id'])
    return flask.jsonify(description=path.description, reward=path.total_reward)


def change_quest_tooltip(hero, data=None, *args, **kwargs):
    quest = models.Quest.get(data['id'])
    return flask.jsonify(description=quest.description, reward=quest.reward_experience)

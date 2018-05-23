import flask

import models


def send_notification_data(hero, data, *args, **kwargs):
    """Return the quest notification data as a JSON

    Maybe this should be a decorator?
    It would wrap any function and tack the "activate notification button"
    function and data on the end of any Json capable response?
    """
    notice = models.Entry.get(data['id'])
    data = flask.jsonify(header=notice.header, body=notice.body, footer=notice.footer, url=notice.url, redirect=data['redirect'])

    # print("Sending Notice content to JS.")
    # pprint(data)

    # Clear quest notification
    # Should delete this notice when it has been viewed.
    notice.journal = None
    return data

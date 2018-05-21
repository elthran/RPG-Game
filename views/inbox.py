import pdb

import flask

from elthranonline import app
import services.decorators
import controller.inbox


@app.route('/inbox/<outbox>', methods=['GET', 'POST'])
@services.decorators.uses_hero
def inbox(outbox, hero=None):
    controller.inbox.check_messages(hero)
    outbox = True if outbox == "outbox" else False
    if flask.request.method == 'POST':
        if flask.request.is_json:
            data = flask.request.get_json()
            # TODO add security to this! Otherwise a malicious user could delete messages from an account they didn't own!
            controller.inbox.delete_messages_by_id(data['ids'])
            return "success"
        else:
            if "replyToMessage" in flask.request.form:
                controller.inbox.reply_to_message(hero, flask.request.form.get('message_id', None, type=int), flask.request.form.get("replyContent", None, type=str))
            else:
                controller.inbox.send_message(hero, flask.request.form.get("receiver", None, type=str), flask.request.form.get("newMessageContent", None, type=str))
    return flask.render_template('inbox.html', page_title="Inbox", hero=hero, outbox=outbox)

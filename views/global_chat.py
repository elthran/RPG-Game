import flask

from elthranonline import app
import services.decorators
import services.time
import controller.chatter


@app.route('/global_chat', methods=['GET', 'POST'])
@services.decorators.uses_hero
def global_chat(hero=None):
    """View general user communication channel.

    This channel only keeps 25 messages and deletes messages older than
    5 minutes old.

    A handy date format function is:
    strftime https://docs.python.org/3.5/library/datetime.html
    current_time = services.time.now().strftime("%H:%M:%S")
    e.g. current_time == "03:05:04"
    """
    chat_log = hero.game.chat_log
    if flask.request.method == 'POST':
        message = flask.request.form.get("message", default=None, type=str)

        controller.chatter.remove_old_messages(outdated_in_minutes=5)
        controller.chatter.add_new_message_to_log(chat_log, hero, message)
        controller.chatter.prune_messages(chat_log, maxsize=15)

        return flask.render_template('global_chat.html', hero=hero, chat_messages=chat_log.chat_messages, active_chatters=chat_log.active_chatters())
    return flask.render_template('global_chat.html', page_title="Chat", hero=hero, chat_messages=chat_log.chat_messages, active_chatters=chat_log.active_chatters())

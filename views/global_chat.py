import flask

from elthranonline import app
import services.decorators
import services.time
import models


@app.route('/global_chat', methods=['GET', 'POST'])
@services.decorators.uses_hero
def global_chat(hero=None):
    chat_log = hero.game.chat_log
    if flask.request.method == 'POST':
        message = flask.request.form["message"]

        models.ChatMessage.query().filter(models.ChatMessage.timestamp < services.time.different_from_now_by(minutes=-5)).delete()
        # models.Base.save()

        # There is -> strftime https://docs.python.org/3.5/library/datetime.html
        # current_time = services.time.now().strftime("%H:%M:%S")

        chat_log.chat_messages.insert(0, models.ChatMessage(hero, message))  # Currently it just appends tuples to the chat list, containing the hero's name and the message
        if len(chat_log.chat_messages) > 25:  # After it reaches 5 messages, more messages will delete the oldest ones
            chat_log.chat_messages.pop()
            # entry = chat_log.pop()
            # del entry

        return flask.render_template('global_chat.html', hero=hero, chat_messages=chat_log.chat_messages, active_chatters=chat_log.active_chatters())
    return flask.render_template('global_chat.html', page_title="Chat", hero=hero, chat_messages=chat_log.chat_messages, active_chatters=chat_log.active_chatters())

"""
message = request.form["message"]
# THERE MUST BE A BETTER WAY TO FORMAT THE TIME
itsnow = EZDB.now()
the_hour = str((itsnow.hour + 17) % 24)
the_minute = str(itsnow.minute)
the_second = str(itsnow.second)
users_needing_to_be_removed = []
for user, time_stamp in game.global_chat_user_list.items():
    if ((int(the_minute) - time_stamp) % 60 >= 5):
        users_needing_to_be_removed.append(user)
for user in users_needing_to_be_removed:
    try:
        del game.global_chat_user_list[user]
    except:
        print("Attempting to delete user '" + user + "' from chat list, but user not found.")
if len(the_hour) < 2:
    the_hour = "0" + the_hour
if len(the_minute) < 2:
    the_minute = "0" + the_minute
if len(the_second) < 2:
    the_second = "0" + the_second
printnow = the_hour + ":" + the_minute + ":" + the_second
game.global_chat.append((printnow, hero.name, message))  # Currently it just appends tuples to the chat list, containing the hero's name and the message
game.global_chat_user_list[hero.user.username] = int(the_minute)
if len(game.global_chat) > 15:  # After it reaches 15 messages, more messages will delete the oldest ones
    game.global_chat = game.global_chat[1:]
return render_template('global_chat.html', hero=hero, chat=game.global_chat, users_in_chat=game.global_chat_user_list)
return render_template('global_chat.html', page_title="Chat", hero=hero, chat=game.global_chat, users_in_chat=game.global_chat_user_list)
"""

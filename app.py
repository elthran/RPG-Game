# ///////////////////////////////////////////////////////////////////////////#
#                                                                            #
#  Author: Elthran B, Jimmy Zhang                                            #
#  Email : jimmy.gnahz@gmail.com                                             #
#                                                                            #
# ///////////////////////////////////////////////////////////////////////////#


from flask import (
    Flask, redirect, url_for, session)
from flask_sslify import SSLify

from models.game import Game
# Marked for restructure! Avoid use of import * in production code.
# from events import Event
# MUST be imported _after_ all other game objects but
# _before_ any of them are used.
from models.database.old_database import EZDB
from engine import Engine

# INIT AND LOGIN FUNCTIONS
# for server code swap this over:
# database = EZDB("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@elthran.mysql.pythonanywhere-services.com/elthran$rpg_database", debug=False)
database = EZDB("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database", debug=False)
engine = Engine(database)

# Disable will need to be restructured (Marlen)
# initialization
game = Game()


def create_app():
    # create the application object
    app = Flask(__name__)
    # pdb.set_trace()

    # async_process(game_clock, args=(database,))
    return app


app = create_app()
sslify = SSLify(app)

# Should replace on server with custom (not pushed to github).
# import os
# os.urandom(24)
# '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.secret_key = 'starcraft'


@app.route('/add_new_character')
def add_new_character():
    user = database.get_object_by_id("User", session['id'])
    database.add_new_hero_to_user(user)
    return redirect(url_for('choose_character'))

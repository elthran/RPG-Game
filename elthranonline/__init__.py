import socket

import flask as fl
import flask_sslify

# import services.filters  # Not sure where to import this ... maybe I only need it in the view that uses it?


def create_app():
    # create the application object
    app_ = fl.Flask(__name__)
    app_.config.from_object('private_config')

    if 'liveweb' not in socket.gethostname():  # Running on local machine.
        # Shouldn't run when not testing.
        app_.jinja_env.trim_blocks = True
        app_.jinja_env.lstrip_blocks = True
        app_.jinja_env.auto_reload = True
    # async_process(game_clock, args=(database,))
    return app_


app = create_app()
# Must import routes after app created http://flask.pocoo.org/docs/0.12/patterns/packages/
# noinspection PyUnresolvedReferences
import routes

sslify = flask_sslify.SSLify(app)

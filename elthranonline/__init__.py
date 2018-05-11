import flask as fl
import flask_sslify


def create_app():
    # create the application object
    app_ = fl.Flask(__name__)
    app_.config.from_object('private_config')

    # async_process(game_clock, args=(database,))
    return app_


app = create_app()
# Must import views after app created http://flask.pocoo.org/docs/0.12/patterns/packages/
# noinspection PyUnresolvedReferences
import views

sslify = flask_sslify.SSLify(app)

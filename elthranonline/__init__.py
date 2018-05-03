import flask as fl
import flask_sslify
import sendgrid

import game
import services

# For testing
engine = services.event_service.Engine()

# Disable will need to be restructured (Marlen)
# initialization
game = game.Game()


def create_app():
    # create the application object
    app_ = fl.Flask(__name__)
    app_.config.from_object('private_config')

    # async_process(game_clock, args=(database,))
    return app_


app = create_app()
sslify = flask_sslify.SSLify(app)

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
sg = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])

# Must after app created http://flask.pocoo.org/docs/0.12/patterns/packages/
# noinspection PyUnresolvedReferences
import views

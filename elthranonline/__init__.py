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
# noinspection SpellCheckingInspection
sslify = flask_sslify.SSLify(app)


# noinspection PyUnresolvedReferences
def import_routes():
    import routes.about
    import routes.admin
    import routes.arena
    import routes.battle
    import routes.choose_character
    import routes.command
    import routes.create_character
    import routes.display_accounts
    import routes.gate
    import routes.global_chat
    import routes.home
    import routes.hooks
    import routes.house
    import routes.icon
    import routes.inbox
    import routes.login
    import routes.logout
    import routes.market
    import routes.spar
    import routes.reset
    import routes.tavern
    import routes.explore_dungeon
    import routes.barracks
    import routes.building
    import routes.store
    import routes.move
    import routes.under_construction
    import routes.forum
    import routes.achievements
    import routes.atlas
    import routes.people


import_routes()

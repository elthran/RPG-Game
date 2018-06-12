import flask

from elthranonline import app
import services.decorators


@app.route('/about')
@services.decorators.uses_hero
def about_page(hero=None):
    info = "The game is being created by Elthran and Haldon, with some help " \
           "from Gnahz. Any inquiries can be made to elthranRPG@gmail.com"
    return flask.render_template('about.html', hero=hero, page_title="About",
                           gameVersion="2018.05.23", info=info)

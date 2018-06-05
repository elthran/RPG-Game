import flask

from elthranonline import app
import services.decorators


@app.route('/quest_log')
@services.decorators.uses_hero
def quest_log(hero=None):
    page_title = "Quest Log"
    return flask.render_template('journal.html', hero=hero, quest_log=True, page_title=page_title)

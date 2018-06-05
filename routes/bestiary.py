import flask

from elthranonline import app
import services.decorators
import models


@app.route('/bestiary/<int:monster_id>')
@services.decorators.uses_hero
def bestiary(hero=None, monster_id=0):
    page_title = "Bestiary"
    all_monsters = models.Hero.filter_by(is_monster=True, template=True).all()
    display_monster = models.Hero.get(monster_id)
    return flask.render_template('journal.html', hero=hero, bestiary=True, page_title=page_title, all_monsters=all_monsters, display_monster=display_monster)

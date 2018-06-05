import flask

from elthranonline import app
import services.decorators
import models


@app.route('/achievements/<achievement_id>')
@services.decorators.uses_hero
def achievements_log(hero=None, achievement_id=0):
    achieve = hero.journal.achievements
    all_achievements = achieve.achievements
    page_title = "Achievements"

    if achievement_id == "0":
        display_achievement = None
    else:
        display_achievement = models.Achievement.get(achievement_id)

    return flask.render_template('journal.html', hero=hero, achievement_log=True, all_achievements=all_achievements, display_achievement=display_achievement, completed_achievements=achieve.completed_achievements, page_title=page_title)

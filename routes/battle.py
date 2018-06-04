import flask

from elthranonline import app
import services.decorators
import services.fetcher
import services.generators
import controller.battle


@app.route('/battle/<enemy>')
@services.decorators.login_required
@services.decorators.uses_hero
def battle(enemy=None, hero=None):
    """This gets called if you fight in the arena."""
    page_links = [("Return to your ", "/home", "profile", " page.")]

    enemy = services.fetcher.fetch_hero_by_username(enemy)

    battle_log, enemy = controller.battle.battle(hero, enemy)
    if hero.is_alive():
        page_links = [("Return to where you ", hero.current_location.url, "were", ".")]
    return flask.render_template('battle.html', battle_log=battle_log, hero=hero, enemy=enemy, page_links=page_links)

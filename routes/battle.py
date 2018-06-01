import flask

from elthranonline import app
import services.decorators
import services.fetcher
import services.generators
import controller.battle


@app.route('/battle/<enemy_user>')
@services.decorators.login_required
@services.decorators.uses_hero
def battle(enemy_user=None, hero=None):
    """This gets called if you fight in the arena."""
    page_links = [("Return to your ", "/home", "profile", " page.")]

    if enemy_user == "monster":  # Ideally if this is an integer then search for a monster with that ID.
        monsters = services.fetcher.get_all_monsters_by_hero_terrain(hero)
        enemy = services.generators.generate_monster(monsters)
    else:  # If it's not an integer, then it's a username. Search for that user's hero.
        enemy = services.fetcher.fetch_hero_by_username(enemy_user)

    battle_log, enemy = controller.battle.battle(hero, enemy)
    if hero.is_alive():
        page_links = [("Return to where you ", hero.current_location.url, "were", ".")]
    return flask.render_template('battle.html', battle_log=battle_log, hero=hero, enemy=enemy, page_links=page_links)

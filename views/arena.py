import flask

from elthranonline import app
import bestiary
import services.decorators


@app.route('/arena/<name>')
@services.decorators.login_required
@services.decorators.uses_hero
@services.decorators.update_current_location
def arena(name='', hero=None, location=None):
    """Set up a battle between the player and a random monster.

    NOTE: partially uses new location/display code.
    """
    # If I try to check if the enemy has 0 health and there is no enemy,
    # I randomly get an error

    enemy = bestiary.monster_generator(hero.age - 6)
    # if enemy.name == "Wolf":
    #     enemy.items_rewarded.append((QuestItem("Wolf Pelt", hero, 50)))
    # if enemy.name == "Scout":
    #     enemy.items_rewarded.append((QuestItem("Copper Coin", hero, 50)))
    # if enemy.name == "Spider":
    #     enemy.items_rewarded.append((QuestItem("Spider Leg", hero, 50)))
    location.display.page_title = "War Room"
    location.display.page_heading = "Welcome to the arena " + hero.name + "!"
    location.display.page_image = str(enemy.name) + '.jpg'

    profs = enemy.proficiencies

    conversation = [("Name: ", str(enemy.name), "Enemy Details"),
                    ("Level: ", str(enemy.level), "Combat Details"),
                    ("Health: ", str(profs.health.current) + " / " + str(
                        profs.health.final)),
                    ("Damage: ", str(profs.damage.base) + " - " + str(
                        profs.damage.final)),
                    ("Attack Speed: ", str(profs.speed.final)),
                    ("Accuracy: ", str(profs.accuracy.final) + "%"),
                    ("First Strike: ", str(profs.first_strike.final) + "%"),
                    ("Critical Hit Chance: ", str(profs.killshot.base) + "%"),
                    ("Critical Hit Modifier: ", str(profs.killshot.modifier)),
                    ("Defence: ", str(profs.defence.final) + "%"),
                    ("Evade: ", str(profs.evade.final) + "%"),
                    ("Parry: ", str(profs.parry.final) + "%"),
                    ("Riposte: ", str(profs.riposte.final) + "%"),
                    ("Block Chance: ", str(profs.block.base) + "%"),
                    ("Block Reduction: ", str(profs.block.modifier) + "%")]

    page_links = [("Challenge the enemy to a ", "/battle/monster", "fight", "."),
                  ("Go back to the ", "/barracks/Barracks", "Barracks", ".")]
    return flask.render_template('building_default.html', page_title=location.display.page_title, page_heading=location.display.page_heading, page_image=location.display.page_image, hero=hero, game=hero.game, page_links=page_links, enemy_info=conversation)

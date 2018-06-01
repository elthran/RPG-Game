import random

import services.fetcher
import services.generators
import models.dialogue


def setup_explore_dungeon(hero):
    """Setup the hero"""
    hero.journal.achievements.current_dungeon_floor = 0
    hero.journal.achievements.current_floor_progress = 0
    hero.random_encounter_monster = None

    dialogue = models.dialogue.WebDialogue("Walk deeper into the", hero.current_location.children[0].url, "ruin")
    return [dialogue]


def descend_level(hero, progress, dialogues):
    achieve = hero.journal.achievements
    achieve.current_dungeon_floor += 1
    achieve.deepest_dungeon_floor = max(achieve.deepest_dungeon_floor, achieve.current_dungeon_floor)
    progress += " You descend to a deeper level of the dungeon!! Current Floor of dungeon: {}".format(achieve.current_dungeon_floor)
    dialogues.append(models.dialogue.WebDialogue("Start ", hero.current_location.url, "exploring", " this level of the dungeon."))
    return progress, dialogues


def explore_dungeon(hero, location, setup=False):
    """Allow the hero to explore a given dungeon.

    This function is progressive.
    i.e. If you run it successive times you will get different results.
    """
    if setup is True:
        return setup_explore_dungeon(hero)

    dialogues = []
    encounter_chance = random.randint(0, 100)
    progress = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
    # You continue exploring
    achieve = hero.journal.achievements
    achieve.current_floor_progress += 1  # Always explore more ..

    # if hero.game.random_encounter_monster is None:
    #     monsters = services.fetcher.get_all_monsters_by_hero_terrain(hero)
    #     monster = services.generators.generate_monster(monsters)
    #     hero.game.random_encounter_monster = monster

    if encounter_chance > (100 - achieve.current_floor_progress*4):
        progress, dialogues = descend_level(hero, progress, dialogues)
    elif encounter_chance > 35:  # You find a monster! Oh no!
        return flask.redirect(flask.url_for('explore_dungeon_encounter', monster_name="generate"))
    elif encounter_chance > 15:  # You find an item!
        return flask.redirect(flask.url_for('explore_dungeon_item', name=name, action='approaching', id_=0))
    else:  # You explore but don't find a lower level ..?
        progress += " You explore farther in but find nothing!"
        dialogues.append(models.dialogue.WebDialogue("Walk deeper into the", hero.current_location.url, "dungeon"))

    # Not sure where this should go?
    progress += " Current progress on this floor: {}".format(hero.journal.achievements.current_floor_progress)
    return progress, dialogues


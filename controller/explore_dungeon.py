import pdb
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


def meet_monster(hero, progress, dialogues):
    """Encountering a new or old monster."""

    monster = None
    if hero.game.random_encounter_monster:  # You have a monster waiting for you from before
        progress += " Your past foe paces in front of you."
        monster = hero.game.random_encounter_monster
    else:
        # monsters = services.fetcher.get_all_monsters_by_hero_terrain(hero)
        # monster = services.generators.generate_monster(monsters)
        # hero.game.random_encounter_monster = monster
        progress += " You come across a terrifying monster lurking in the shadows."
        monsters = services.fetcher.get_all_monsters_by_hero_terrain(hero)
        monster = services.generators.generate_monster(monsters)
        hero.game.random_encounter_monster = monster
    dialogues.append(models.dialogue.WebDialogue("Attack the ", "/battle/{}".format(monster.name), monster.name))
    dialogues.append(models.dialogue.WebDialogue("Attempt to ", hero.current_location.parent.url, "flee"))
    return progress, dialogues


def explore_item(hero, action):
    """Approaching, finding and picking up an item."""

    dialogues = []
    progress = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)

    if action == 'approaching':  # Approaching item.
        progress += " You find something shiny in a corner of the dungeon."
        dialogues.append(models.dialogue.WebDialogue("", "{}/item".format(hero.current_location.url), "Investigate", " the light's source."))
    elif action == 'finding':  # Finding item.
        if not hero.game.discovered_item:
            hero.game.discovered_item = services.generators.get_random_item()
        discovered_item = hero.game.discovered_item
        progress += " You find an item in the dungeon! It's a {}".format(discovered_item.name)
        dialogues.append(("Pick up the ", "{}/item/pick_up".format(hero.current_location.url), "item"))
    elif action == 'picking_up':  # picking up item
        hero.inventory.add_item(hero.game.discovered_item)
        return progress, []
    else:
        raise Exception("Route '{}' doesn't exist.".format(action))
    return progress, dialogues


def explore_dungeon(hero, setup=False):
    """Allow the hero to explore a given dungeon.

    This function is progressive.
    i.e. If you run it successive times you will get different results.
    """
    if setup is True or hero.journal.achievements.current_dungeon_floor is None:
        return setup_explore_dungeon(hero)

    dialogues = []
    encounter_chance = random.randint(0, 100)
    progress = "Current Floor of dungeon: {}".format(hero.journal.achievements.current_dungeon_floor)
    paragraph = ""
    # You continue exploring
    achieve = hero.journal.achievements
    achieve.current_floor_progress += 1  # Always explore more ..

    # You explore and find a lower level!
    if encounter_chance > (100 - achieve.current_floor_progress*4):
        progress, dialogues = descend_level(hero, progress, dialogues)
    elif encounter_chance > 35:  # You find a monster! Oh no!
        progress, dialogues = meet_monster(hero, progress, dialogues)
    elif encounter_chance > 15:  # You find an item!
        return progress, []
    else:  # You explore but don't find a lower level ..
        progress += " You explore farther in but find nothing!"
        dialogues.append(models.dialogue.WebDialogue("Walk deeper into the", hero.current_location.url, "dungeon"))

    # Not sure where this should go?
    progress += " Current progress on this floor: {}".format(hero.journal.achievements.current_floor_progress)
    return progress, dialogues


from random import randint

from flask import render_template

from app import app, game, database
from services.decorators import login_required, uses_hero, \
    update_current_location
from services.generators import generate_monster


@app.route('/explore_dungeon/<name>/<extra_data>')
@login_required
@uses_hero
@update_current_location
def explore_dungeon(name='', hero=None, location=None, extra_data=None):
    """
    NOTE: @elthran You shouldn't modify location data as this will modify it for all heroes/users in the game.
    Instead just pass this data to the template directly.
    (Marlen)

    # From /inside_dungeon
    """

    # For convenience
    # location.display.page_heading = "Current Floor of dungeon: " + str(hero.journal.achievements.current_dungeon_floor)
    if extra_data == "Entering":  # You just arrived into the dungeon
        # location.display.page_heading += "You explore deeper into the dungeon!"
        page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
        return render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links)
    if extra_data == "Item":
        # The problem here is that when you see an item .. you have already
        # picked it up.
        # I think you need to use a different order of operations.
        # Like put the "add item" after the "pick up item" part
        discovered_item = database.get_random_item()
        #location.display.page_heading = "You find an item in the dungeon! It's a " + discovered_item.name
        hero.inventory.add_item(discovered_item)
        page_links = [("Pick up the ", "/explore_dungeon/Explore%20Dungeon/None", "item", ".")]
        return render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links)
    encounter_chance = randint(0, 100)
    if hero.random_encounter_monster: # You have a monster waiting for you from before
        #location.display.page_heading += "The monster paces in front of you."
        monsters = database.get_all_monsters(hero) # This should be a saved monster and not re-generated :(
        monster = generate_monster(hero, monsters)
        page_links = [("Attack the ", "/battle/monster", "monster", "."),
                      ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
    else: # You continue exploring
        hero.journal.achievements.current_dungeon_floor_progress += 1
        if encounter_chance > (100 - (hero.journal.achievements.current_dungeon_floor_progress*4)):
            hero.journal.achievements.current_dungeon_floor += 1
            if hero.journal.achievements.current_dungeon_floor > hero.journal.achievements.deepest_dungeon_floor:
                hero.journal.achievements.deepest_dungeon_floor = hero.journal.achievements.current_dungeon_floor
            hero.journal.achievements.current_dungeon_floor_progress = 0
            #location.display.page_heading = "You descend to a deeper level of the dungeon!! Current Floor of dungeon: " + str(hero.journal.achievements.current_dungeon_floor)
            page_links = [("Start ", "/explore_dungeon/Explore%20Dungeon/None", "exploring", " this level of the dungeon.")]
        elif encounter_chance > 35: # You find a monster! Oh no!
            monsters = database.get_all_monsters(hero)
            monster = generate_monster(hero, monsters)

            #location.display.page_heading += "You come across a terrifying monster lurking in the shadows."
            hero.current_dungeon_monster = True
            page_links = [("Attack the ", "/battle/monster", "monster", "."),
                          ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
        elif encounter_chance > 15: # You find an item!
            #location.display.page_heading += "You find something shiny in a corner of the dungeon."
            page_links = [("", "/explore_dungeon/Explore%20Dungeon/Item", "Investigate", " the light's source.")]
        else:
            #location.display.page_heading += " You explore deeper into the dungeon!"
            page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
    #location.display.page_heading += " Current progress on this floor: " + str(hero.journal.achievements.current_dungeon_floor_progress)
    return render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links)  # return a string

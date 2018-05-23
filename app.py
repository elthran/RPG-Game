# ///////////////////////////////////////////////////////////////////////////#
#                                                                            #
#  Author: Elthran B, Jimmy Zhang                                            #
#  Email : jimmy.gnahz@gmail.com                                             #
#                                                                            #
# ///////////////////////////////////////////////////////////////////////////#

from math import ceil
from socket import gethostname

from flask import (
    Flask, render_template, request)
from flask_sslify import SSLify

from models.game import Game
import combat_simulator
# Marked for restructure! Avoid use of import * in production code.
from bestiary import *
# from events import Event
# MUST be imported _after_ all other game objects but
# _before_ any of them are used.
from services.event_service import Engine
from models.forum import Board, Thread, Post
from models.bestiary2 import create_monster, MonsterTemplate
import services

# For testing
from services.decorators import login_required, uses_hero, update_current_location

engine = Engine()

# Disable will need to be restructured (Marlen)
# initialization
game = Game()


def create_app():
    # create the application object
    app = Flask(__name__)
    app.config.from_object('private_config')

    # async_process(game_clock, args=(database,))
    return app


app = create_app()
sslify = SSLify(app)


@app.route('/spellbook')
@uses_hero
def spellbook(hero=None):
    spells = []
    for ability in hero.abilities:
        if ability.castable and ability.level > 0:
            spells.append(ability)
    max_pages = max(ceil(len(spells)/8), 1)
    first_index = (hero.spellbook_page - 1) * 8
    if len(spells) <= first_index + 8:
        last_index = first_index + ((len(spells) - 1) % 8) + 1
    else:
        last_index = first_index + 8
    return render_template('spellbook.html', page_title="Spellbook", hero=hero, spells=spells[first_index:last_index], max_pages=max_pages)

@app.route('/settings/<tab>/<choice>', methods=['GET', 'POST'])
@uses_hero
def settings(hero=None, tab="profile", choice="none"):
    message = None
    if request.method == 'POST':
        if request.form['type'] == "update_password":
            if database.validate(hero.account.username, request.form['old_password']):
                new_password = request.form['new_password']
                user = hero.user
                user.password = services.secrets.encrypt(new_password)
                message = "Password changed!"
            else:
                print("wrong password!")
                message = "You entered the wrong password. Password change failed."
        elif request.form['type'] == "update_email":
            email = request.form['new_email']
            hero.account.email = services.secrets.encrypt(email)
            message = "Email address changed to: " + email
    return render_template('settings.html', hero=hero, user=hero.user, tab=tab, choice=choice, message=message)


# PROFILE PAGES (Basically the home page of the game with your character
# display and stats)


# This gets called anytime you have  attribute points to spend
# Currently I send "attributes=True" so that the html knows to highlight
# the bar and show that you are on this page
@app.route('/attributes', methods=['GET', 'POST'])
@login_required
@uses_hero
def attributes(hero=None):
    return render_template('profile_attributes.html', page_title="Attributes", hero=hero, all_attributes=hero.attributes)

# This gets called anytime you have secondary attribute points to spend
# Currently I send "proficiencies=True" so that the html knows to highlight
# the bar and show that you are on this page
@app.route('/proficiencies', methods=['GET', 'POST'])
@login_required
@uses_hero
def proficiencies(hero=None):
    # This page is literally just a html page with tooltips and proficiency level up buttons. No python code is needed. Python only tells html which page to load.
    return render_template('profile_proficiencies.html', page_title="Proficiencies", hero=hero, all_attributes=hero.attributes, all_proficiencies=hero.base_proficiencies)


@app.route('/ability_tree/<spec>')
@login_required
@uses_hero
def ability_tree(spec, hero=None):
    # for prof in hero.get_summed_proficiencies():
    #     if prof.name == "stealth" or prof.name == "health":
    #         print(prof,"\n")
    if spec == "archetype" and hero.specializations.archetype is None: # On the archetype pagebut the hero doesn't have one!
        becomeType = "archetype"
        spec_choices = database.get_all_objects("Archetype")
    elif spec == "calling" and hero.specializations.calling is None: # On the archetype pagebut the hero doesn't have one!
        becomeType = "calling"
        spec_choices = database.get_all_objects("Calling")
    elif spec == "pantheon" and hero.specializations.pantheon is None: # On the archetype pagebut the hero doesn't have one!
        becomeType = "pantheon"
        spec_choices = database.get_all_objects("Pantheon")
    else:
        becomeType = None
        spec_choices = []

    all_abilities = []
    for ability in hero.abilities:
        if ability.hidden == False and ability.tree == spec.title(): # This checks if the ability is the correct basic/archetpe/calling/pantheon
            if spec == "basic": # If its basic thenit passed and always gets added
                all_abilities.append(ability)
            elif spec == "archetype" and hero.specializations.archetype: # If it's archetype and the hero has chosen an archetype...
                if hero.specializations.archetype.name == ability.tree_type: # If the chosen archetype matches the ability's archetype add it
                    all_abilities.append(ability)

    return render_template('profile_ability.html', hero=hero, ability_tree=spec,
                           all_abilities=all_abilities, becomeType=becomeType,
                           spec_choices=spec_choices)


@app.route('/inventory_page')
@login_required
@uses_hero
def inventory_page(hero=None):
    page_title = "Inventory"
    # for item in hero.inventory:
    #     if item.wearable:
    #         item.check_if_improvement()
    return render_template(
        'inventory.html', hero=hero, page_title=page_title,
        isinstance=isinstance, getattr=getattr)

@app.route('/quest_log')
@login_required
@uses_hero
def quest_log(hero=None):
    page_title = "Quest Log"
    return render_template('journal.html', hero=hero, quest_log=True, page_title=page_title)

@app.route('/bestiary/<monster_id>')
@login_required
@uses_hero
def bestiary(hero=None, monster_id=0):
    page_title = "Bestiary"
    all_monsters = database.session.query(MonsterTemplate).filter().all()
    if monster_id == "0":
        display_monster = None
    else:
        display_monster = database.get_object_by_id("MonsterTemplate", int(monster_id))
    return render_template('journal.html', hero=hero, bestiary=True, page_title=page_title,
        all_monsters=all_monsters, display_monster=display_monster)


@app.route('/people_log/<npc_id>')
@login_required
@uses_hero
def people_log(hero=None, npc_id=0):
    page_title = "People"
    all_npcs = [NPC(1, "Old Man", "Human", 87), NPC(2, "Blacksmith", "Human", 53)] # Temp
    #all_npcs = database.session.query(NPCS).filter().all()
    try:
        display_npc = database.get_object_by_id("NPCS", int(npc_id))
    except:
        display_npc = None
    #BELOW IS JUST FOR TESTING
    if npc_id == "1":
        display_npc = all_npcs[0]
    elif npc_id == "2":
        display_npc = all_npcs[1]
    #ABOVEIS JUST FOR TESTING
    return render_template('journal.html', hero=hero, people_log=True, page_title=page_title,
                           all_npcs=all_npcs, display_npc=display_npc)  # return a string

@app.route('/atlas/<map_id>')
@login_required
@uses_hero
def atlas(hero=None, map_id=0):
    page_title = "Map"
    # Below is temporary map code as it's not currently set up
    all_maps = [database.get_object_by_id("Location", 1)]
    if map_id == "0":
        display_map = None
    else:
        display_map = database.get_object_by_id("Location", int(map_id))
    return render_template('journal.html', hero=hero, atlas=True, page_title=page_title,
                           all_maps=all_maps, display_map=display_map)  # return a string

@app.route('/achievements/<achievement_id>')
@login_required
@uses_hero
def achievements(hero=None, achievement_id=0):
    """
def achievement_log(hero=None):
    achievements = hero.journal.achievements
    page_title = "Achievements"
    return render_template(
        'journal.html', hero=hero, achievement_log=True,
        completed_achievements=achievements.completed_achievements,
        kill_achievements=achievements.kill_achievements,
        kill_quests={},
        page_title=page_title)  # return a string
    """
    page_title = "Achievements"
    all_achievements = [(1, "Kill 3 Wolves", 5)]
    if achievement_id == "0":
        display_achievement = None
    else:
        display_achievement = all_achievements[0]
    return render_template('journal.html', hero=hero, achievement_log=True, page_title=page_title,
                           all_achievements=all_achievements, display_achievement=display_achievement)  # return a string

@app.route('/forum/<board_id>/<thread_id>', methods=['GET', 'POST'])
@login_required
@uses_hero
def forum(hero=None, board_id=0, thread_id=0):
    page_title = "Forum"
    # Checking current forum. Currently it's always on this forum as we only have 1
    current_forum = database.get_object_by_id("Forum", 1)
    # Letting python/html know which board/thread you are reading. Will be simpler with database and get_thread_by_id ;)
    try:
        current_board = database.get_object_by_id("Board", int(board_id))
    except:
        current_board = None
    try:
        current_thread = database.get_object_by_id("Thread", int(thread_id))
        current_thread.views += 1
    except:
        current_thread = None

    if request.method == 'POST':
        form_type = request.form["form_type"]
        if form_type == "new_board": # If starting new board
            board_name = request.form["board_name"]
            new_board = Board(board_name)
            current_forum.create_board(new_board)
        elif form_type == "new_thread": # If starting new thread
            thread_name = request.form["thread_name"]
            thread_description = request.form["thread_description"]
            thread_board = database.get_object_by_name("Board", request.form["thread_board"])
            new_thread = Thread(thread_name, hero.account.username, thread_description)
            thread_board.create_thread(new_thread)
            if len(request.form["thread_post"]) > 0: # If they typed a new post, add it to the new thread
                new_post = Post(request.form["thread_post"], hero.user)
                new_thread.write_post(new_post)
        else: # If repyling
            post_content = request.form["post_content"]
            new_post = Post(post_content, hero.user)
            current_thread.write_post(new_post)
            hero.account.prestige += 1 # Give the user prestige. It's used to track meta activities and is unrelated to gameplay

    return render_template('forum.html', hero=hero,
                           current_forum=current_forum, current_board=current_board, current_thread=current_thread,
                           page_title=page_title, get_author=database.get_user_by_username)  # return a string

@app.route('/under_construction')
@login_required
@uses_hero
def under_construction(hero=None):
    page_title = "Under Construction"
    return render_template('layout.html', page_title=page_title, hero=hero)  # return a string


@app.route('/map/<name>')
@app.route('/town/<name>')
@app.route('/dungeon/<name>')
@app.route('/explorable/<name>')
@login_required
@uses_hero
@update_current_location
# @policies.url_protect
def move(name='', hero=None, location=None):
    """Set up a directory for the hero to move to.

    Arguments are in the form of a url and are sent by the data that can be
    found with the 'view page source' command in the browser window.
    """
    # pdb.set_trace()
    hero.current_terrain = location.terrain # Set the hero's terrain to the terrain type of the place he just moved to.
    if location.type == 'map':
        # location.pprint() # Why do we have this?
        other_heroes = []
    else:
        other_heroes = hero.get_other_heroes_at_current_location()

    return render_template(
        'move.html', hero=hero,
        page_title=location.display.page_title,
        page_heading=location.display.page_heading,
        page_image=location.display.page_image,
        paragraph=location.display.paragraph,
        people_of_interest=other_heroes,
        places_of_interest=location.places_of_interest)

# Currently runs blacksmith and marketplace
@app.route('/store/<name>')
@login_required
@uses_hero
@update_current_location
def store(name, hero=None, location=None):
    # print(hero.current_city)
    if name == "Blacksmith":
        dialogue = "I have the greatest armoury in all of Thornwall!" # This should be pulled from pre_built objects
        items_for_sale = database.get_all_store_items()
    elif name == "Marketplace":
        dialogue = "I have trinkets from all over the world! Please take a look."
        items_for_sale = database.get_all_marketplace_items()
    else:
        error = "Trying to get to the store but the store name is not valid."
        render_template('broken_page_link', error=error)
    return render_template('store.html', hero=hero,
                           dialogue=dialogue,
                           items_for_sale=items_for_sale,
                           page_title=location.display.page_title)

# Currently runs old man's hut
@app.route('/building/<name>')
@login_required
@uses_hero
@update_current_location
def building(name='', hero=None, location=None):
    other_heroes = hero.get_other_heroes_at_current_location()
    if name == "Old Man's Hut":
        blacksmith_path_name = "Get Acquainted with the Blacksmith"
        if not database.hero_has_quest_path_named(hero, blacksmith_path_name):
            print("Adding new quests!")
            blacksmith_path = database.get_quest_path_template(blacksmith_path_name)
            hero.journal.quest_paths.append(blacksmith_path)
        else:
            print("Hero has path of that name, ignoring ..")

    return render_template(
        'move.html', hero=hero,
        page_title=location.display.page_title,
        page_heading=location.display.page_heading,
        page_image=location.display.page_image,
        paragraph=location.display.paragraph,
        people_of_interest=other_heroes,
        places_of_interest=location.places_of_interest)

@app.route('/barracks/<name>')
@login_required
@uses_hero
@update_current_location
def barracks(name='', hero=None, location=None):
    # This will be removed soon.
    # Dead heros wont be able to move on the map and will immediately get
    # moved to ahospital until they heal. So locations won't need to factor
    # in the "if"of the hero being dead
    if hero.get_summed_proficiencies('health').current <= 0:
        location.display.page_heading = "Your hero is currently dead."
        location.display.page_image = "dead.jpg"
        location.children = None
        location.display.paragraph = "You have no health."
    else:
        location.display.page_heading = "Welcome to the barracks {}!".format(
            hero.name)
        location.display.page_image = "barracks.jpg"
        location.display.paragraph = "Battle another player."

        arena = database.get_object_by_name('Location', 'Arena')
        arena.display.paragraph = "Compete in the arena."

        spar = database.get_object_by_name('Location', 'Spar')
        spar.display.paragraph = "Spar with the trainer."
        location.children = [arena, spar]

    return render_template('generic_location.html', hero=hero)

# From /dungeon
@app.route('/dungeon_entrance/<name>')
@login_required
@uses_hero
@update_current_location
def dungeon_entrance(name='', hero=None, location=None):
    location.display.page_heading = " You are in the dungeon and exploring!"
    hero.journal.achievements.current_dungeon_floor = 0
    hero.current_dungeon_progress = 0
    hero.random_encounter_monster = False
    explore_dungeon = database.get_object_by_name('Location', 'Explore Dungeon')
    explore_dungeon.display.paragraph = "Take a step into the dungeon."
    location.children = [explore_dungeon]
    return render_template('generic_location.html', hero=hero, game=game)  # return a string

# From /inside_dungeon
@app.route('/explore_dungeon/<name>/<extra_data>')
@login_required
@uses_hero
@update_current_location
def explore_dungeon(name='', hero=None, location=None, extra_data=None):
    # For convenience
    location.display.page_heading = "Current Floor of dungeon: " + str(hero.journal.achievements.current_dungeon_floor)
    if extra_data == "Entering": # You just arrived into the dungeon
        location.display.page_heading += "You explore deeper into the dungeon!"
        page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
        return render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links)
    if extra_data == "Item":
        # The problem here is that when you see an item .. you have already
        # picked it up.
        # I think you need to use a different order of operations.
        # Like put the "add item" after the "pick up item" part
        discovered_item = database.get_random_item()
        location.display.page_heading = "You find an item in the dungeon! It's a " + discovered_item.name
        hero.inventory.add_item(discovered_item)
        page_links = [("Pick up the ", "/explore_dungeon/Explore%20Dungeon/None", "item", ".")]
        return render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links)
    encounter_chance = randint(0, 100)
    if hero.random_encounter_monster == True: # You have a monster waiting for you from before
        location.display.page_heading += "The monster paces in front of you."
        enemy = monster_generator(hero.journal.achievements.current_dungeon_floor + 1) # This should be a saved monster and not re-generated :(
        page_links = [("Attack the ", "/battle/monster", "monster", "."),
                      ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
    else: # You continue exploring
        hero.journal.achievements.current_dungeon_floor_progress += 1
        if encounter_chance > (100 - (hero.journal.achievements.current_dungeon_floor_progress*4)):
            hero.journal.achievements.current_dungeon_floor += 1
            if hero.journal.achievements.current_dungeon_floor > hero.journal.achievements.deepest_dungeon_floor:
                hero.journal.achievements.deepest_dungeon_floor = hero.journal.achievements.current_dungeon_floor
            hero.journal.achievements.current_dungeon_floor_progress = 0
            location.display.page_heading = "You descend to a deeper level of the dungeon!! Current Floor of dungeon: " + str(hero.journal.achievements.current_dungeon_floor)
            page_links = [("Start ", "/explore_dungeon/Explore%20Dungeon/None", "exploring", " this level of the dungeon.")]
        elif encounter_chance > 35: # You find a monster! Oh no!
            # Not sure how to move the session query to the database as I need to pull the terrain attribute first
            terrain = getattr(MonsterTemplate, hero.current_terrain)
            monsters = database.session.query(MonsterTemplate).filter(terrain == True).all()
            m = choice(monsters)  # Randomly choose a monster from the list
            monster = create_monster(name=m.name, level=hero.age,
                                     agility=m.agility, charisma=m.charisma, divinity=m.divinity, resilience=m.resilience,
                                     fortuity=m.fortuity, pathfinding=m.pathfinding, quickness=m.quickness, willpower=m.willpower,
                                     brawn=m.brawn, survivalism=m.survivalism, vitality=m.vitality, intellect=m.intellect)
            print("If you were running the new bestiary code, you would be fighting a " + monster.name + " (level " + str(monster.level) + "), because you are in terrain type " + hero.current_terrain + ".")

            location.display.page_heading += "You come across a terrifying monster lurking in the shadows."
            enemy = monster_generator(hero.journal.achievements.current_dungeon_floor+1)
            hero.current_dungeon_monster = True
            page_links = [("Attack the ", "/battle/monster", "monster", "."),
                          ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
        elif encounter_chance > 15: # You find an item!
            location.display.page_heading += "You find something shiny in a corner of the dungeon."
            page_links = [("", "/explore_dungeon/Explore%20Dungeon/Item", "Investigate", " the light's source.")]
        else:
            location.display.page_heading += " You explore deeper into the dungeon!"
            page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
    location.display.page_heading += " Current progress on this floor: " + str(hero.journal.achievements.current_dungeon_floor_progress)
    return render_template('dungeon_exploring.html', hero=hero, game=game, page_links=page_links)  # return a string

# From /barracks
@app.route('/spar/<name>')
@login_required
@uses_hero
@update_current_location
def spar(name='', hero=None, location=None):
    spar_cost = 50
    spar_benefit = 5
    if hero.gold < spar_cost:
        location.display.page_heading = "You do not have enough gold to spar."
    else:
        hero.gold -= spar_cost

        # This gives you experience and also returns how much
        # experience you gained
        modified_spar_benefit = hero.gain_experience(spar_benefit)
        hero.base_proficiencies['endurance'].current -= 1
        location.display.page_heading = \
            "You spend some time sparring with the trainer at the barracks." \
            " You spend {} gold and gain {} experience.".format(
                spar_cost, modified_spar_benefit)
    return render_template('generic_location.html', hero=hero, game=game)  # return a string


# From /barracks
@app.route('/arena/<name>')
@login_required
@uses_hero
@update_current_location
def arena(name='', hero=None, location=None):
    """Set up a battle between the player and a random monster.

    NOTE: partially uses new location/display code.
    """
    # If I try to check if the enemy has 0 health and there is no enemy,
    # I randomly get an error

    enemy = monster_generator(hero.age - 6)
        # if enemy.name == "Wolf":
        #     enemy.items_rewarded.append((QuestItem("Wolf Pelt", hero, 50)))
        # if enemy.name == "Scout":
        #     enemy.items_rewarded.append((QuestItem("Copper Coin", hero, 50)))
        # if enemy.name == "Spider":
        #     enemy.items_rewarded.append((QuestItem("Spider Leg", hero, 50)))
    location.display.page_title = "War Room"
    location.display.page_heading = "Welcome to the arena " + hero.name + "!"
    location.display.page_image = str(enemy.name) + '.jpg'

    profs = enemy.get_summed_proficiencies()

    conversation = [("Name: ", str(enemy.name), "Enemy Details"),
                    ("Level: ", str(enemy.level), "Combat Details"),
                    ("Health: ", str(profs.health.get_base()) + " / " + str(
                        profs.health.final)),
                    ("Damage: ", str(profs.damage.final) + " - " + str(
                        profs.damage.final)),
                    ("Attack Speed: ", str(profs.speed.final)),
                    ("Accuracy: ", str(profs.accuracy.final) + "%"),
                    ("First Strike: ", str(profs.first_strike.final) + "%"),
                    ("Critical Hit Chance: ", str(profs.killshot.final) + "%"),
                    ("Critical Hit Modifier: ", str(profs.killshot.final)),
                    ("Defence: ", str(profs.defence.final) + "%"),
                    ("Evade: ", str(profs.evade.final) + "%"),
                    ("Parry: ", str(profs.parry.final) + "%"),
                    ("Riposte: ", str(profs.riposte.final) + "%"),
                    ("Block Chance: ", str(profs.block.final) + "%"),
                    ("Block Reduction: ", str(profs.block.final) + "%")]

    page_links = [("Challenge the enemy to a ", "/battle/monster", "fight", "."),
                  ("Go back to the ", "/barracks/Barracks", "Barracks", ".")]
    return render_template(
        'building_default.html', page_title=location.display.page_title,
        page_heading=location.display.page_heading,
        page_image=location.display.page_image, hero=hero, game=game,
        page_links=page_links, enemy_info=conversation)


# this gets called if you fight in the arena
@app.route('/battle/<enemy_user>')
@login_required
@uses_hero
def battle(enemy_user=None, hero=None):
    page_links = [("Return to your ", "/home", "profile", " page.")]
    if enemy_user == "monster": # Ideally if this is an integer then search for a monster with that ID.
        pass
    else:   # If it's not an integer, then it's a username. Search for that user's hero.
        enemy = database.fetch_hero_by_username(enemy_user)
        # enemy.login_alerts += "You have been attacked!-"     This will be changed to the new notification system.
        enemy.experience_rewarded = enemy.age # For now you just get 1 experience for each level the other hero was
        enemy.items_rewarded = []   # Currently you get no items for killing another user
    battle_log = combat_simulator.battle_logic(hero, enemy) # Not sure if the combat sim should update the database or return the heros to be updated here
    hero.current_dungeon_monster = False # Whether you win or lose, the monster will now be gone.
    if hero.base_proficiencies['health'].current == 0: # First see if the player died.
        location = database.get_object_by_name('Location', hero.last_city.name) # Return hero to last visited city
        hero.current_location = location
        hero.current_dungeon_monster = False  # Reset any progress in any dungeon he was in
        hero.journal.achievements.deaths += 1  # Record that the hero has another death
        battle_log.append("You were defeated. You gain no experience and your account should be deleted.")
        if enemy_user != "monster":
            enemy.journal.achievements.player_kills += 1
            pass
    else:  # Ok, the hero is not dead. Currently that means he won! Since we don't have ties yet.
        experience_gained = str(hero.gain_experience(enemy.experience_rewarded)) # This works PERFECTLY as intended!
        if enemy_user == "monster": # This needs updating. If you killed a monster then the next few lines should differ from a user
            hero.journal.achievements.monster_kills += 1
            pass
        else: # Ok, you killed a user!
            hero.journal.achievements.player_kills += 1  # You get a player kill score!
            enemy.journal.achievements.deaths += 1  # Make sure they get their death recorded!
            location = database.get_object_by_name('Location', enemy.last_city.name) # Send them to their last visited city
            enemy.current_location = location
        if len(enemy.items_rewarded) > 0: # Give the hero any items earned! This probably should be completely redone.
            for item in enemy.items_rewarded:
                if not any(items.name == item.name for items in hero.inventory):
                    hero.inventory.append(item)
                else:
                    for items in hero.inventory:
                        if items.name == item.name:
                            items.amount_owned += 1
                battle_log.append("You have defeated the " + enemy.name + " and gained " + experience_gained + " experience!")
        page_links = [("Return to where you ", hero.current_location.url, "were", ".")]
    return render_template('battle.html', battle_log=battle_log, hero=hero, enemy=enemy, page_links=page_links)

# @app.route('/tavern')
@app.route('/tavern/<name>', methods=['GET', 'POST'])
@login_required
@uses_hero
def tavern(name='', hero=None):
    tavern = True
    page_title = "Tavern"
    page_heading = "You enter the Red Dragon Inn."
    page_image = "bartender"
    paragraph = None
    dialogue_options = None
    """
    if "Become an apprentice at the tavern." in hero.completed_quests:
        paragraph = "Welcome, my apprentice!"
    else:
        paragraph = "Greetings traveler! What can I get for you today?"
    page_links = [("Return to ", "/tavern", "tavern", ".")]  # I wish it looked like this
    dialogue_options = {"Drink": "Buy a drink for 25 gold. (This fully heals you)"}
    if "Collect 2 Wolf Pelts for the Bartender" not in hero.errands and "Collect 2 Wolf Pelts for the Bartender" not in hero.completed_quests:
        dialogue_options["Jobs"] = "Ask if there are any jobs you can do."
    if "Collect 2 Wolf Pelts for the Bartender" in hero.errands:
        if any(item.name == "Wolf Pelt" and item.amount_owned >= 2 for item in hero.inventory):
            dialogue_options["HandInQuest"] = "Give the bartender 2 wolf pelts."
        else:
            dialogue_options["QuestNotFinished"] = "I'm still looking for the 2 wolf pelts."
    if "Collect 2 Wolf Pelts for the Bartender" in hero.completed_quests:
        if any(quest[0] == "Become an apprentice at the tavern." and quest[2] == 1 for quest in hero.current_quests):
            if any(item.name == "Copper Coin" and item.amount_owned >= 2 for item in hero.inventory):
                dialogue_options["HandInQuest2"] = "Give the bartender 2 copper coins."
            else:
                dialogue_options["QuestNotFinished"] = "I'm still looking for the two copper coins."
        elif any(quest[0] == "Become an apprentice at the tavern." and quest[2] == 2 for quest in hero.current_quests):
            if any(item.name == "Spider Leg" and item.amount_owned >= 1 for item in hero.inventory):
                dialogue_options["HandInQuest3"] = "Give the bartender a spider leg."
            else:
                dialogue_options["QuestNotFinished"] = "I'm still looking for the spider leg."
        elif "Become an apprentice at the tavern." not in hero.completed_quests:
            dialogue_options["Jobs2"] = "Do you have any other jobs you need help with?"
    if request.method == 'POST':
        tavern = False
        paragraph = ""
        dialogue_options = {}
        tavern_choice = request.form["tavern_choice"]
        if tavern_choice == "Drink":
            if hero.gold >= 25:
                hero.health = hero.health_maximum
                hero.gold -= 25
                page_heading = "You give the bartender 25 gold and he pours you a drink. You feel very refreshed!"
            else:
                page_heading = "Pay me 25 gold first if you want to see your drink."
        elif tavern_choice == "Jobs":
            hero.errands.append("Collect 2 Wolf Pelts for the Bartender")
            page_heading = "The bartender has asked you to find 2 wolf pelts!"
            page_image = ""
        elif tavern_choice == "HandInQuest":
            hero.gold += 5000
            hero.errands = [(name, stage) for name, stage in hero.current_quests if
                            name != "Collect 2 Wolf Pelts for the Bartender"]
            hero.completed_quests.append(("Collect 2 Wolf Pelts for the Bartender"))
            page_heading = "You have given the bartender 2 wolf pelts and completed your quest! He has rewarded you with 5000 gold."
        elif tavern_choice == "QuestNotFinished":
            page_heading = "Don't take too long!"
        elif tavern_choice == "Jobs2":
            page_heading = "Actually, I could use a hand with something if you are interested in becoming my apprentice. First I will need 2 copper coins. Some of the goblins around the city are carrying them."
            hero.current_quests.append(["Become an apprentice at the tavern.",
                                        "You need to find two copper coins and give them to the blacksmith", 1])
        elif tavern_choice == "HandInQuest2":
            hero.current_quests[0][1] = "Now the bartender wants you to find a spider leg."
            hero.current_quests[0][2] += 1
            page_heading = "Fantastic! Now I just need a spider leg."
        elif tavern_choice == "HandInQuest3":
            hero.current_quests = [quest for quest in hero.current_quests if
                                   quest[0] != "Become an apprentice at the tavern."]
            hero.completed_quests.append("Become an apprentice at the tavern.")
            page_heading = "You are now my apprentice!"
            """
    return render_template(
        'tavern.html', hero=hero, page_title=page_title,
        page_heading=page_heading, page_image=page_image, paragraph=paragraph,
        tavern=tavern, dialogue_options=dialogue_options)  # return a string


@app.route('/marketplace/<inventory>')
@login_required
@uses_hero
def marketplace(inventory, hero=None):
    if inventory == "shopping":
        items_for_sale = database.get_all_marketplace_items()
        dialogue = "Anything catch your fancy?"
    else:
        items_for_sale = []
        dialogue = "Welcome to the Thornwall market. We have goods from all over the eastern coast. Come in and take a look."
    return render_template('store.html', hero=hero, items_for_sale=items_for_sale, dialogue=dialogue)  # return a string


@app.route('/house/<name>')
@login_required
@uses_hero
def house(name='', hero=None):
    """A web page for a house.

    Returns a rendered html page.
    """
    location = database.get_object_by_name('Location', name)
    return render_template('generic_location.html', hero=hero)


# END OF STARTING TOWN FUNCTIONS


# start the server with the 'run()' method
if __name__ == '__main__':
    # import os

    # Set Current Working Directory (CWD) to the home of this file.
    # This should make all other files import relative to this file fixing the Database doesn't exist problem.

    # os.chdir(os.path.dirname(os.path.abspath(__file__)))


    # Not implemented ... should be moved to prebuilt_objects.py and implemented in
    # connect_to_database.py as get_default_quests()
    # Quest aren't actually implement yet but they will be soon!
    # Super temporary while testing quests
    # hero.inventory.append(QuestItem("Wolf Pelt", hero, 50))
    # hero.inventory.append(QuestItem("Spider Leg", hero, 50))
    # hero.inventory.append(QuestItem("Copper Coin", hero, 50))
    # for item in hero.inventory:
    #     item.amount_owned = 5
    if 'liveweb' not in gethostname():  # Running on local machine.
        # Remove when not testing.
        app.jinja_env.trim_blocks = True
        app.jinja_env.lstrip_blocks = True
        app.jinja_env.auto_reload = True
        app.run(debug=True)

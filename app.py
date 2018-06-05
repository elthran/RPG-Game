# ///////////////////////////////////////////////////////////////////////////#
#                                                                            #
#  Author: Elthran B, Jimmy Zhang                                            #
#  Email : jimmy.gnahz@gmail.com                                             #
#                                                                            #
# ///////////////////////////////////////////////////////////////////////////#


from flask import (
    Flask, render_template, redirect, url_for, request, session)
from flask_sslify import SSLify

from models.game import Game
# Marked for restructure! Avoid use of import * in production code.
# from events import Event
# MUST be imported _after_ all other game objects but
# _before_ any of them are used.
from models.database.old_database import EZDB
from engine import Engine
from math import ceil
from services.decorators import login_required, uses_hero

# INIT AND LOGIN FUNCTIONS
# for server code swap this over:
# database = EZDB("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@elthran.mysql.pythonanywhere-services.com/elthran$rpg_database", debug=False)
database = EZDB("mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database", debug=False)
engine = Engine(database)

# Disable will need to be restructured (Marlen)
# initialization
game = Game()


def create_app():
    # create the application object
    app = Flask(__name__)
    # pdb.set_trace()

    # async_process(game_clock, args=(database,))
    return app


app = create_app()
sslify = SSLify(app)

# Should replace on server with custom (not pushed to github).
# import os
# os.urandom(24)
# '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.secret_key = 'starcraft'


@app.route('/add_new_character')
def add_new_character():
    user = database.get_object_by_id("User", session['id'])
    database.add_new_hero_to_user(user)
    return redirect(url_for('choose_character'))


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
            if database.validate(hero.user.username, request.form['old_password']):
                new_password = request.form['new_password']
                user = hero.user
                user.password = database.encrypt(new_password)
                message = "Password changed!"
            else:
                print("wrong password!")
                message = "You entered the wrong password. Password change failed."
        elif request.form['type'] == "update_email":
            email = request.form['new_email']
            hero.user.email = database.encrypt(email)
            message = "Email address changed to: " + email
    return render_template('settings.html', page_title="Settings", hero=hero, user=hero.user, tab=tab, choice=choice, message=message)


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
        page_title = "Archetype Abilities"
        becomeType = "archetype"
        spec_choices = database.get_all_objects("Archetype")

        # For testing!
        if not hero.specialization_access:
            philosopher = database.get_object_by_name("Archetype", "Philosopher")
            hero.set_specialization_access(philosopher)
            hero.specialization_access[philosopher.id].hidden = False
            database.session.commit()

    elif spec == "calling" and hero.specializations.calling is None: # On the archetype pagebut the hero doesn't have one!
        page_title = "Calling Abilities"
        becomeType = "calling"
        spec_choices = database.get_all_objects("Calling")
    elif spec == "pantheon" and hero.specializations.pantheon is None: # On the archetype pagebut the hero doesn't have one!
        page_title = "Pantheon Abilities"
        becomeType = "pantheon"
        spec_choices = database.get_all_objects("Pantheon")
    else:
        page_title = "Basic Abilities"
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

    return render_template('profile_ability.html', page_title=page_title, hero=hero, ability_tree=spec,
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
    all_monsters = database.get_all_monsters()
    if monster_id == "0":
        display_monster = None
    else:
        display_monster = database.get_monster_by_id(monster_id)
    return render_template('journal.html', hero=hero, bestiary=True, page_title=page_title,
        all_monsters=all_monsters, display_monster=display_monster)



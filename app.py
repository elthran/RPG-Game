# ///////////////////////////////////////////////////////////////////////////#
#                                                                            #
#  Author: Elthran B, Jimmy Zhang                                            #
#  Email : jimmy.gnahz@gmail.com                                             #
#                                                                            #
# ///////////////////////////////////////////////////////////////////////////#


import pdb  # For testing!
from pprint import pprint  # For testing!
from functools import wraps
from random import choice
import os

from flask import (
    Flask, render_template, redirect, url_for, request, session,
    flash, send_from_directory)

import werkzeug

from game import Game
import combat_simulator
from attributes import \
    ATTRIBUTE_INFORMATION  # Since attribute information was hand typed out in both modules, it was causing bugs. Seems cleaner to import it and then only edit it in one place
# Marked for restructure! Avoid use of import * in production code.
from bestiary import *
from commands import Command
# from events import Event
# MUST be imported _after_ all other game objects but
# _before_ any of them are used.
from database import EZDB
from engine import Engine
from forum import Board, Thread, Post
from bestiary2 import create_monster, MonsterTemplate

# INIT AND LOGIN FUNCTIONS
database = EZDB('sqlite:///static/database.db', debug=False)
engine = Engine(database)

# Disable will need to be restructured (Marlen)
# initialization
game = Game()

# create the application object
app = Flask(__name__)
app.secret_key = 'starcraft'

ALWAYS_VALID_URLS = [
    '/login', '/home', '/about', '/inventory_page', '/quest_log',
    '/attributes', '/proficiencies', '/ability_tree/*', '/bestiary/*',
    '/people_log/*', '/map_log', '/quest_log', '/display_users/*',
    '/inbox', '/logout',
]


# Work in progress.
# Control user moves on map. Rename too 'url_protect' because it sounds _sick_.
def url_protect(f):
    """Redirects to last page if hero can't travel here.

    I need to update the location.py code to deal more with urls.
    """

    @wraps(f)
    def wrap_url(*args, **kwargs):
        #Currently disabled ... does nothing.
        return f(*args, **kwargs)


        # Break immediately if server is just being set up.
        # Everything after this will run just before the function
        # runs but not during function setup.
        # There is probably cleaner way?
        try:
            session['logged_in']
        except RuntimeError:
            return f(*args, **kwargs)

        # pprint(app.url_map)
        # pprint(args)
        # pprint(kwargs)
        # pprint(session)
        # print(dir(session))
        # f(*args, **kwargs)
        # print('after app.route')
        # print(dir(request.url_rule))
        # print("url rule", request.url_rule)
        # print("rule", request.url_rule.rule)
        # print("arguments", request.url_rule.arguments)
        # pprint(request)
        # print(dir(request))
        # print("Path requested: ", request.path)

        # Build requested move from rule and arguemts.
        valid_urls = ALWAYS_VALID_URLS

        hero = kwargs['hero']
        if hero.user.is_admin:
            valid_urls.append('/admin')

        # print("Hero current location url: ", hero.current_location.url)
        valid_urls.append(hero.current_location.url)
        valid_urls.append(hero.current_location.parent.url)
        for location in hero.current_location.adjacent:
            valid_urls.append(location.url)
        # Add this in later? Unless I can find out how
        # to do it another way.
        # local_places = hero.current_location.display.places_of_interest
        # print(hero.current_location)
        # pprint(hero.current_location.display.places_of_interest)
        # valid_urls += [] #all places of places_of_interest

        # This may work ... it will need more testing.
        # It may need additional parsing.
        requested_move = request.path
        # pdb.set_trace()
        if requested_move in valid_urls or hero.user.is_admin:
            # print("url is valid")
            session['last_url'] = request.path
            return f(*args, **kwargs)
        else:
            flash("You can't access '{}' from there.".format(requested_move))
            print("Possibly a bug in 'url_protect' .. possibly intended.")
            return redirect(session['last_url'])
    return wrap_url


@app.template_filter()
def validate_hero_image(hero):
    """Used to handle an expected/possible error in the template.

    See https://codenhagen.wordpress.com/2015/08/20/custom-jinja2-template-filters-and-flask/
    """
    # pdb.set_trace()
    image_name = ''
    try:
        image_name = "archetype_{}.jpg".format(hero.archetype.lower())
    except AttributeError:
        image_name = "character.jpg"
    return image_name


@app.template_filter()
def validate_hero_name(hero):
    return hero.name if hero.name else "UnNamed"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


def login_required(f):
    """Set certain pages as requiring a login to visit.

    This should redirect you to the login page."""

    @wraps(f)
    def wrap_login(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap_login


# This runs after every @app.route before returning a response.
# It even runs if there is an error.
# I am unsure of this approach. Myabe '@app.after_request' would be a better
# fit as this wouldn't write data that caused an error.
@app.after_request
def update_after_request(response):
    database.update()
    # print("Database updated.")
    # print(response.data)
    return response


# @app.before_request
# def handle_redirect_session_bug():
#     print("Before Request session status")
#     print(database.session.new)
#     print(database.session.dirty)


# Untested (Marlen)
def uses_hero(f):
    """Preload hero object and save it afterwards.

    Note: KeyError occurs when this method is called before login method
    has been run. Also after a POST request before page reload.
    Seems wipe the session cookie temporarily? Fine after normal page load
    Only fails if view page source after POST.
    """

    @wraps(f)
    def wrap_uses_hero(*args, **kwargs):
        try:
            # print("Currently at the uses_hero function!")
            hero = database.get_object_by_id("Hero", session["hero_id"])
        except KeyError as ex:
            if not session:
                # After making a POST request with AJAX the session
                # gets cleared? Until you make a new GET request?
                # This is a request for the Page Source and it occurs
                # in a new blank session.
                return "After POST request reload the page to view source."
            else:
                raise ex
        return f(*args, hero=hero, **kwargs)
    return wrap_uses_hero


def update_current_location(f):
    """Load the location object and set it to hero.current_location.

    NOTE: this must come after "@uses_hero"
    Adds a keyword argument 'location' to argument list.

    Example usage:
    @app.route('/barracks/<name>')
    @login_required
    @uses_hero
    @update_current_location
    def barracks(name='', hero=None, location=None):
        if hero.proficiencies.health.current <= 0:
            location.display.page_heading = "Your hero is currently dead."
    """

    @wraps(f)
    def wrap_current_location(*args, **kwargs):
        hero = kwargs['hero']
        location = database.get_object_by_name('Location', kwargs['name'])
        hero.current_location = location
        engine.spawn(
            'move_event',
            hero,
            description="{} visits {}.".format(hero.name, location.url)
        )
        return f(*args, location=location, **kwargs)

    return wrap_current_location


# use decorators to link the function to a url
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # Should prevent contamination between logging in with 2 different
    # accounts.
    session.clear()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if request.form['type'] == "login":
            # Otherwise, we are just logging in normally
            if database.validate(username, password):
                session['logged_in'] = True
            # Marked for upgrade, consider checking if user exists
            # and redirect to account creation page.
            else:
                error = 'Invalid Credentials. Please try again.'
        elif request.form['type'] == "register":
            # See if new_username has a valid input.
            # This only works if they are creating an account
            if database.get_user_id(username):
                error = "Username already exists!"
            else:
                user = database.add_new_user(username, password)
                database.add_new_hero_to_user(user)
                session['logged_in'] = True
        else:
            raise Exception("The form of this 'type' doesn't exist!")

        if session['logged_in']:
            flash("LOG IN SUCCESSFUL")
            user = database.get_user_by_username(username)
            session['id'] = user.id
            # Will barely pause here if only one character exists.
            # Maybe should just go directly to home page.
            return redirect(url_for('choose_character'))

    return render_template('index.html', error=error)


# route for handling the account creation page logic
# @app.route('/password_recovery', methods=['GET', 'POST'])
# def password_recovery():
#     error = "Password Not Found"
#
#     if request.method == 'POST':
#         username = request.form['username']
#
#         con = sqlite3.connect('static/user.db')
#         with con:
#             cur = con.cursor()
#             cur.execute("SELECT * FROM Users")
#             rows = cur.fetchall()
#             for row in rows:
#                 if row[0] == username:
#                     error = "We found your password, but it was hashed into"
#                         "this: " + row[1] + ". We are unable to decode the"
#                         " jargon. Sorry, please restart the game!"
#         con.close()
#     return render_template('index.html', error=error, password_recovery=True)


# route for handling the account creation page logic
"""
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.get_user_id(username):
            error = "Username already exists!"
        else:
            user = database.add_new_user(username, password)
            database.add_new_hero_to_user(user)
            # database.add_world_map_to_hero() maybe?
            return redirect(url_for('login'))
    return render_template('index.html', error=error, create_account=True)
    """


@app.route('/add_new_character')
def add_new_character():
    user = database.get_object_by_id("User", session['id'])
    database.add_new_hero_to_user(user)
    return redirect(url_for('choose_character'))


# this gets called if you press "logout"
@app.route('/logout')
@login_required
@uses_hero
def logout(hero=None):
    hero.refresh_character()
    session.pop('logged_in', None)
    flash("Thank you for playing! Your have successfully logged out.")
    return redirect(url_for('login'))

# this gets called if you are logged in and there is no character info stored
@app.route('/create_character', methods=['GET', 'POST'])
@login_required
@uses_hero
def create_character(hero=None):
    if len(hero.journal.quest_paths) == 0:
        hero.journal.quest_paths = database.get_default_quest_paths()

    if hero.current_world is None:
        hero.current_world = database.get_default_world()
        hero.current_location = database.get_default_location()

    if hero.background is not None:
        hero.background = "Barbarian"

    if hero.name is None:
        page_image = "beached"
        generic_text =  "You awake to great pain and confusion as you hear footsteps " \
                    "approaching in the sand. Unsure of where you are, you quickly look " \
                    "around for something to defend yourself. A firm and inquisitive voice " \
                    "pierces the air."
        npc_text = [("Stranger", "Who are you and what are you doing here?")]
        user_action = "get text"
        user_response = "...I don't remember what happened. My name is"
        user_text_placeholder = "Character Name"
        if request.method == 'POST':
            hero.name = request.form["get_data"].title()
            page_image = "blacksmith"
            generic_text = ""
            npc_text = [("Stranger", "Where do you come from, child?")]
            user_action = "make choice"
            user_response = [
                ("My father was a great warlord from the north.", "Gain <ul><li>+1 Brawn</li></ul>", "Barbarian"),
                ("My father was a great missionary traveling to the west.", "Gain <ul><li>+1 Intellect</li></ul>", "Missionary")]
            user_text_placeholder = ""
    elif hero.background == "":
        # This is needed if the user names there hero but leaves the page and returns later. But I will write it out later.
        pass
    else:
        hero.refresh_character(full=True)
        return redirect(url_for('home'))
    return render_template('generic_dialogue.html', page_image=page_image,
                           generic_text=generic_text, npc_text=npc_text, user_action=user_action, user_response=user_response,
                           user_text_placeholder=user_text_placeholder)

@app.route('/choose_character', methods=['GET', 'POST'])
@login_required
def choose_character():
    user = database.get_object_by_id("User", session['id'])
    # print(user)
    # exit("testing choose character.")
    hero = None
    if len(user.heroes) == 1:
        hero = user.heroes[0]
    elif request.method == 'POST':
        hero = database.get_object_by_id("Hero", request.form['hero_id'])
    else:
        return render_template('choose_character.html', user=user)

    # Below is code for daily login reward. It's temporary as I am just trying to play with and learn about timestamps and whatnot.
    hero.check_daily_login_reward(str(EZDB.now()))
    # End of daily login reward code (Elthran)
    session['hero_id'] = hero.id
    # Now I need to work out how to make game not global *sigh*
    # (Marlen)
    game.set_hero(hero)
    game.set_enemy(monster_generator(hero.age))
    flash(hero.login_alerts)
    hero.login_alerts = ""
    # If it's a new character, send them to create_character url
    if hero.character_name is None: # Whats the difference between character_name and name?
        return redirect(url_for('create_character'))
    # If the character already exist go straight the main home page!
    return redirect(url_for('home'))


# An admin button that lets you reset your character. Currently doesnt reset attributes/proficiencies, nor inventory and other stuff. Should be rewritten as something
# like deleting the current hero and rebuilding the admin hero. I commented out the beginning of that but I cant get it to work
@app.route('/reset_character/<stat_type>')
@login_required
@uses_hero
def reset_character(stat_type, hero=None):
    hero.age = 7
    hero.experience = 0
    hero.experience_maximum = 10
    hero.renown = 0
    hero.virtue = 0
    hero.devotion = 0
    hero.gold = 5000
    hero.basic_ability_points = 5
    hero.archetype_ability_points = 5
    hero.calling_ability_points = 5
    hero.pantheon_ability_points = 5
    hero.attribute_points = 10
    hero.proficiency_points = 10
    return redirect(url_for('home'))  # return a string


# this is a temporary page that lets you modify any attributes for testing
@app.route('/admin/<path>', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
@login_required
@uses_hero
def admin(path=None, hero=None):
    admin = None
    if path == "edit_database":
        pass
    elif path == "modify_self":
        page_title = "Admin"
        if request.method == 'POST':
            hero.age = int(request.form["Age"])
            hero.experience = int(request.form["Experience"])
            hero.experience_maximum = int(request.form["Experience_maximum"])
            hero.renown = int(request.form["Renown"])
            hero.virtue = int(request.form["Virtue"])
            hero.devotion = int(request.form["Devotion"])
            hero.gold = int(request.form["Gold"])
            hero.basic_ability_points = int(request.form["Basic_ability_points"])
            hero.archetype_ability_points = int(request.form["Archetype_ability_points"])
            hero.calling_ability_points = int(request.form["Calling_ability_points"])
            hero.pantheon_ability_points = int(request.form["Pantheon_ability_points"])
            hero.attribute_points = int(request.form["Attribute_points"])
            hero.proficiency_points = int(request.form['Proficiency_Points'])
            hero.refresh_character(full=True)
            return redirect(url_for('home'))

        admin = [
            ("Age", hero.age),
            ("Experience", hero.experience),
            ("Experience_maximum", hero.experience_maximum),
            ("Renown", hero.renown),
            ("Virtue", hero.virtue),
            ("Devotion", hero.devotion),
            ("Gold", hero.gold),
            ("Basic_ability_points", hero.basic_ability_points),
            ("Archetype_ability_points", hero.archetype_ability_points),
            ("Calling_ability_points", hero.calling_ability_points),
            ("Pantheonic_ability_points", hero.pantheon_ability_points),
            ("Attribute_points", hero.attribute_points),
            ("Proficiency_Points", hero.proficiency_points)]
    return render_template('admin.html', hero=hero, admin=admin, path=path)  # return a string


# The if statement works and displays the user page as normal. Now if you
# click on a user it should run the else statement and pass in the user's
# username (which is unique).
# Now, I am having trouble sending the user to HTML. I can't seem to
# understand how to store the user information as a variable.
@app.route('/display_users/<page_type>/<page_detail>', methods=['GET', 'POST'])
@uses_hero
def display_user_page(page_type, page_detail, hero=None):
    descending = False
    if page_detail == hero.clicked_user_attribute:
        hero.clicked_user_attribute = ""
        descending = True
    else:
        hero.clicked_user_attribute = page_detail

    if page_type == "display":
        sorted_heroes = database.fetch_sorted_heroes(page_detail, descending)
        return render_template(
            'users.html', page_title="Users", hero=hero,
            page_detail=page_detail, all_heroes=sorted_heroes)
    elif page_type == "see_user":
        this_user = database.get_user_by_username(page_detail)
        this_hero = database.fetch_hero_by_username(page_detail)
        # Below code is just messing with inbox
        if request.method == 'POST':
            this_message = request.form['message']
            if len(this_message) > 1:
                hero.user.inbox.send_message(this_user, this_message, str(EZDB.now()))
                confirmation_message = "Message sent!"
            else:
                confirmation_message = "Please type your message"
            return render_template('profile_other_user.html', hero=hero, page_title=str(this_user.username),
                                   enemy_hero=this_hero, confirmation=confirmation_message)
        # Above this is inbox nonsense
        return render_template(
            'profile_other_user.html', hero=hero, page_title=str(this_user.username),
            enemy_hero=this_hero)


@app.route('/global_chat', methods=['GET', 'POST'])
@uses_hero
def global_chat(hero=None):
    if request.method == 'POST':
        message = request.form["message"]
        # MUST BE A BETTER WAY TO FORMAT THE TIME
        itsnow = EZDB.now()
        the_hour = str((itsnow.hour + 17) % 24)
        the_minute = str(itsnow.minute)
        the_second = str(itsnow.second)
        game.global_chat_user_list[hero] = int(the_minute)
        users_needing_to_be_removed = []
        for user, time_stamp in game.global_chat_user_list.items():
            if (int(the_minute) - time_stamp) % 60 > 5:
                users_needing_to_be_removed.append(user)
        for user in users_needing_to_be_removed:
            del game.global_chat_user_list[user]
        if len(the_hour) < 2:
            the_hour = "0" + the_hour
        if len(the_minute) < 2:
            the_minute = "0" + the_minute
        if len(the_second) < 2:
            the_second = "0" + the_second
        printnow = the_hour + ":" + the_minute + ":" + the_second
        # END OF SHITTY TIME FORMAT. TOOK 11 LINES OF CODE TO TURN IT INTO A DECENT PICTURE
        game.global_chat.append((printnow, hero.name,
                                 message))  # Currently it just appends tuples to the chat list, containing the hero's name and the message
        if len(game.global_chat) > 25:  # After it reaches 5 messages, more messages will delete theoldest ones
            game.global_chat = game.global_chat[1:]
        return render_template('global_chat.html', hero=hero, chat=game.global_chat, users_in_chat=game.global_chat_user_list)
    return render_template('global_chat.html', page_title="Chat", hero=hero, chat=game.global_chat, users_in_chat=game.global_chat_user_list)


@app.route('/inbox/<outbox>', methods=['GET', 'POST'])
@uses_hero
def inbox(outbox, hero=None):
    hero.user.inbox_alert = False # Your inbox alert will no longer glow until a new message is sent to you, even if you dont open all your letters
    if outbox == "outbox":
        outbox = True
    else:
        outbox = False
    if request.method == 'POST':
        # pprint(request.form)
        if request.is_json:
            data = request.get_json()
            ids_to_delete = data['ids']
            try:
                for message_id in ids_to_delete:
                    database.delete_object_by_id("Message", message_id)
                return "success"
            except IndexError as ex:
                return "error: {}".format(ex)
        else:
            if "replyToMessage" in request.form:
                message = database.get_object_by_id("Message", request.form['message_id'])
                content = request.form["replyContent"]
                receiver = message.sender.user
                hero.user.inbox.send_message(receiver, content, str(EZDB.now()))
                receiver.inbox_alert = True
            else:
                content = request.form["newMessageContent"]
                receiver = request.form["receiver"]
                receiver = database.get_user_by_username(receiver)
                try:
                    hero.user.inbox.send_message(receiver, content, str(EZDB.now()))
                    receiver.inbox_alert = True
                except AttributeError:
                    print("Message failed to send: the username does not exist")
    return render_template('inbox.html', page_title="Inbox", hero=hero, outbox=outbox)


@app.route('/spellbook')
@uses_hero
def spellbook(hero=None):
    return render_template('spellbook.html', page_title="Spellbook", hero=hero)



# PROFILE PAGES (Basically the home page of the game with your character
# display and stats)
@app.route('/home')
@login_required
@uses_hero
def home(hero=None):
    """Build the home page and return it as a string of HTML.

    render_template uses Jinja2 markup.
    """

    # Is this supposed to update the time of all hero objects?
    database.update_time(hero)

    # Not implemented. Control user moves on map.
    # Sets up initial valid moves on the map.
    # Should be a list of urls ...
    # session['valid_moves'] \
    #  = hero.current_world.show_directions(hero.current_location)
    # session['valid_moves'].append(hero.current_location.id)

    return render_template(
        'profile_home.html', page_title="Profile", hero=hero, profile=True)


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
    return render_template('profile_proficiencies.html', page_title="Proficiencies", hero=hero, all_attributes=hero.attributes
                           ,all_proficiencies=hero.proficiencies)


@app.route('/ability_tree/<spec>')
@login_required
@uses_hero
def ability_tree(spec, hero=None):
    all_abilities = []
    becomeType = None
    all_type_choices = []
    if spec == "basic":
        points_remaining = hero.basic_ability_points
    elif spec == "archetype":
        points_remaining = hero.archetype_ability_points
        if hero.specializations.archetype is None:
            becomeType = "archetype"

            # all_specializations = database.get_all_specializations()
            # see EZDB.get_all_users() -- maybe sort by name?
            all_type_choices = [("brute", "A character who uses strength and combat to solve problems. Proficient with many types of weapons."),
                                ("scoundrel", "A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery."),
                                ("ascetic", "A character who focuses on disciplining mind and body. They use a combination of combat and intellect."),
                                ("survivalist", "A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration."),
                                ("philosopher", "A character who uses intellect to solve problems. Excels at any task requiring powers of the mind."),
                                ("opportunist", "A character who solves problems using speech and dialogue.")]
    elif spec == "calling":
        points_remaining = hero.calling_ability_points
        if hero.calling == None:
            becomeType = "archetype"
            all_type_choices = [("thief", "A character who specializes in thievery and stealth.")]
    elif spec == "pantheon":
        points_remaining = hero.pantheon_ability_points
        if hero.pantheon == None:
            becomeType = "pantheon"
            all_type_choices = [("ashari'", "Goddess of the sun")]
    for ability in hero.abilities:
        if ability.hidden == False and ability.tree == spec:
            all_abilities.append(ability)
    return render_template('profile_ability.html', page_title="Abilities", hero=hero, ability_tree=spec,
                           all_abilities=all_abilities, points_remaining=points_remaining, becomeType=becomeType,
                           all_type_choices=all_type_choices)


@app.route('/inventory_page')
@login_required
@uses_hero
def inventory_page(hero=None):
    page_title = "Inventory"
    total_armour = 0
    for armour in hero.inventory:
        if armour.inventory_unequipped == None:
            try:
                total_armour += armour.armour_value
            except AttributeError:
                pass  # item might not have an armour value.
       # if not armour.unequipped:
      #      total_armour += armour.armour_value
    # for item in hero.inventory:
    #     if item.wearable:
    #         item.check_if_improvement()
    return render_template(
        'inventory.html', hero=hero, page_title=page_title,
        isinstance=isinstance, getattr=getattr, test_value=total_armour)

@app.route('/quest_log')
@login_required
@uses_hero
def quest_log(hero=None):
    page_title = "Quest Log"
    return render_template('journal.html', hero=hero, quest_log=True, page_title=page_title)

@app.route('/bestiary/<current_monster_id>')
@login_required
@uses_hero
def bestiary(current_monster_id, hero=None):
    if current_monster_id == "default":
        current_monster = None
    else:
        for monster in bestiary_data:
            if monster.monster_id == current_monster_id:
                current_monster = monster
                break
    page_title = "Bestiary"
    return render_template(
        'journal.html', hero=hero, bestiary=True, page_title=page_title,
        bestiary_data=bestiary_data, current_monster=current_monster)


@app.route('/people_log/<current_npc>')
@login_required
@uses_hero
def people_log(current_npc, hero=None):
    if current_npc == "default":
        current_npc = None
    else:
        for npc in npc_data:
            if npc.npc_id == current_npc:
                current_npc = npc
                break
    page_title = "People"
    return render_template('journal.html', hero=hero, people_log=True, page_title=page_title, npc_data=npc_data,
                           current_npc=current_npc)  # return a string

@app.route('/map_log')
@login_required
@uses_hero
def map_log(hero=None):
    page_title = "Map"
    return render_template('journal.html', hero=hero, map_log=True, page_title=page_title)  # return a string

@app.route('/achievement_log')
@login_required
@uses_hero
def achievement_log(hero=None):
    page_title = "Achievements"
    return render_template('journal.html', hero=hero, achievement_log=True,
                           completed_achievements=hero.completed_achievements, page_title=page_title)  # return a string

@app.route('/forum/<board_id>/<thread_id>', methods=['GET', 'POST'])
@login_required
@uses_hero
def forum(hero=None, board_id=0, thread_id=0):
    # Not sure how to move the session query to the database as I need to pull the terrain attribute first
    terrain = getattr(MonsterTemplate, "forest")
    monsters = database.session.query(MonsterTemplate).filter(terrain == True).all()
    monster_template = choice(monsters) # Randomly choose a monster from the list
    monster = create_monster(name=monster_template.name, level=hero.age)

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
            new_thread = Thread(thread_name, hero.user.username, thread_description)
            current_board.create_thread(new_thread)
        else: # If repyling
            post_content = request.form["post_content"]
            new_post = Post(post_content, hero.user.username)
            current_thread.write_post(new_post)
            hero.user.prestige += 1 # Give the user prestige. It's used to track meta activities and is unrelated to gameplay

    return render_template('forum.html', hero=hero, current_forum=current_forum, current_board=current_board, current_thread=current_thread, page_title=page_title)  # return a string

@app.route('/under_construction')
@login_required
@uses_hero
def under_construction(hero=None):
    page_title = "Under Construction"
    return render_template('layout.html', page_title=page_title, hero=hero)  # return a string


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


@app.route('/map/<name>')
@app.route('/town/<name>')
@app.route('/dungeon/<name>')
@app.route('/explorable/<name>')
@login_required
@uses_hero
@update_current_location
@url_protect
def move(name='', hero=None, location=None):
    """Set up a directory for the hero to move to.

    Arguments are in the form of a url and are sent by the data that can be
    found with the 'view page source' command in the browser window.
    """
    # pdb.set_trace()
    if location.type == 'map':
        location.pprint()
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

@app.route('/barracks/<name>')
@login_required
@uses_hero
@update_current_location
def barracks(name='', hero=None, location=None):
    # This will be removed soon.
    # Dead heros wont be able to move on the map and will immediately get
    # moved to ahospital until they heal. So locations won't need to factor
    # in the "if"of the hero being dead
    if hero.proficiencies.health.current <= 0:
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
    hero.current_dungeon_floor = 0
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
    location.display.page_heading = "Current Floor of dungeon: " + str(hero.current_dungeon_floor)
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
        enemy = monster_generator(hero.current_dungeon_floor + 1) # This should be a saved monster and not re-generated :(
        game.set_enemy(enemy)
        page_links = [("Attack the ", "/battle/monster", "monster", "."),
                      ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
    else: # You continue exploring
        hero.current_dungeon_floor_progress += 1
        if encounter_chance > (100 - (hero.current_dungeon_floor_progress*4)):
            hero.current_dungeon_floor += 1
            if hero.current_dungeon_floor > hero.deepest_dungeon_floor:
                hero.deepest_dungeon_floor = hero.current_dungeon_floor
            hero.current_dungeon_floor_progress = 0
            location.display.page_heading = "You descend to a deeper level of the dungeon!! Current Floor of dungeon: " + str(hero.current_dungeon_floor)
            page_links = [("Start ", "/explore_dungeon/Explore%20Dungeon/None", "exploring", " this level of the dungeon.")]
        elif encounter_chance > 35: # You find a monster! Oh no!
            location.display.page_heading += "You come across a terrifying monster lurking in the shadows."
            enemy = monster_generator(hero.current_dungeon_floor+1)
            hero.current_dungeon_monster = True
            game.set_enemy(enemy)
            page_links = [("Attack the ", "/battle/monster", "monster", "."),
                          ("Attempt to ", "/dungeon_entrance/Dungeon%20Entrance", "flee", ".")]
        elif encounter_chance > 15: # You find an item!
            location.display.page_heading += "You find something shiny in a corner of the dungeon."
            page_links = [("", "/explore_dungeon/Explore%20Dungeon/Item", "Investigate", " the light's source.")]
        else:
            location.display.page_heading += " You explore deeper into the dungeon!"
            page_links = [("Walk deeper into the", "/explore_dungeon/Explore%20Dungeon/None", "dungeon", ".")]
    location.display.page_heading += " Current progress on this floor: " + str(hero.current_dungeon_floor_progress)
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
        modified_spar_benefit, level_up = hero.gain_experience(spar_benefit)
        hero.proficiencies.endurance.current -= 1
        location.display.page_heading = \
            "You spend some time sparring with the trainer at the barracks." \
            " You spend {} gold and gain {} experience.".format(
                spar_cost, modified_spar_benefit)
        if level_up:
            location.display.page_heading += " You level up!"
    # page_links = {
    #     "Compete in the arena.": "/arena",
    #     "Spar with the trainer.": "/spar",
    #     "Battle another player.": None
    # }
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
    if not game.has_enemy:
        enemy = monster_generator(hero.age - 6)
        if enemy.name == "Wolf":
            enemy.items_rewarded.append((QuestItem("Wolf Pelt", hero, 50)))
        if enemy.name == "Scout":
            enemy.items_rewarded.append((QuestItem("Copper Coin", hero, 50)))
        if enemy.name == "Spider":
            enemy.items_rewarded.append((QuestItem("Spider Leg", hero, 50)))
        game.set_enemy(enemy)
    location.display.page_title = "War Room"
    location.display.page_heading = "Welcome to the arena " + hero.name + "!"
    location.display.page_image = str(game.enemy.name) + '.jpg'
    conversation = [("Name: ", str(game.enemy.name), "Enemy Details"),
                    ("Level: ", str(game.enemy.level), "Combat Details"),
                    ("Health: ", str(game.enemy.proficiencies.health.current) + " / " + str(
                        game.enemy.proficiencies.health.maximum)),
                    ("Damage: ", str(game.enemy.proficiencies.damage.minimum) + " - " + str(
                        game.enemy.proficiencies.damage.maximum)),
                    ("Attack Speed: ", str(game.enemy.proficiencies.speed.speed)),
                    ("Accuracy: ", str(game.enemy.proficiencies.accuracy.accuracy) + "%"),
                    ("First Strike: ", str(game.enemy.proficiencies.first_strike.chance) + "%"),
                    ("Critical Hit Chance: ", str(game.enemy.proficiencies.killshot.chance) + "%"),
                    ("Critical Hit Modifier: ", str(game.enemy.proficiencies.killshot.modifier)),
                    ("Defence: ", str(game.enemy.proficiencies.defence.modifier) + "%"),
                    ("Evade: ", str(game.enemy.proficiencies.evade.chance) + "%"),
                    ("Parry: ", str(game.enemy.proficiencies.parry.chance) + "%"),
                    ("Riposte: ", str(game.enemy.proficiencies.riposte.chance) + "%"),
                    ("Block Chance: ", str(game.enemy.proficiencies.block.chance) + "%"),
                    ("Block Reduction: ", str(game.enemy.proficiencies.block.modifier) + "%")]
    page_links = [("Challenge the enemy to a ", "/battle/monster", "fight", "."),
                  ("Go back to the ", "/barracks/Barracks", "Barracks", ".")]
    return render_template(
        'building_default.html', page_title=location.display.page_title,
        page_heading=location.display.page_heading,
        page_image=location.display.page_image, hero=hero, game=game,
        page_links=page_links, enemy_info=conversation, enemy=game.enemy)


# this gets called if you fight in the arena
@app.route('/battle/<this_user>')
@login_required
@uses_hero
def battle(this_user=None, hero=None):
    page_title = "Battle"
    page_heading = "Fighting"
    print("running function: battle2")
    page_links = [("Return to your ", "/home", "profile", " page.")]
    if this_user == "monster":
        pass
    else:
        enemy = database.fetch_hero_by_username(this_user)
        enemy.login_alerts += "You have been attacked!-"
        game.set_enemy(enemy)
        game.enemy.experience_rewarded = 5
        game.enemy.items_rewarded = []
    hero.proficiencies.health.current, game.enemy.proficiencies.health.current, battle_log = combat_simulator.battle_logic(hero, game.enemy) # This should return the full heroes, not just their health
    game.has_enemy = False
    if hero.proficiencies.health.current == 0:
        page_title = "Defeat!"
        page_heading = "You have died."
        location = database.get_object_by_name('Location', hero.last_city.name)
        hero.current_location = location
        hero.current_dungeon_monster = False
        hero.deaths += 1
    else:
        """
        for item in hero.equipped_items:
            item.durability -= 1
            if item.durability <= 0:
                item.broken = True
        # This code is for the bestiary and should add one to your kill count for that species of monster. If it's a new species it shouls add it to your book.
        newMonster = True
        for key, value in hero.kill_quests.items():
            if key == game.enemy.species:
                hero.kill_quests[key] += 1
                if hero.kill_quests[key] == 2:
                    for achievement in hero.completed_achievements:
                        if achievement[0] == "Kill a " + game.enemy.species:
                            hero.completed_achievements.remove(achievement)
                            break
                    hero.completed_achievements.append(("Kill two " + game.enemy.species_plural, "10"))
                    hero.experience += 10
                newMonster = False
                break
        if newMonster is not None:
            #hero.kill_quests[game.enemy.species] = 1
            hero.completed_achievements.append(("Kill a " + game.enemy.species, "5"))
            for monster in bestiary_data:
                if monster.name == game.enemy.name:
                    hero.bestiary.append(monster)
            hero.experience += 5
        """
        experience_gained,level_up = hero.gain_experience(game.enemy.experience_rewarded)  # * hero.experience_gain_modifier  THIS IS CAUSING A WEIRD BUG? I don't know why
        if this_user == "monster":
            hero.monster_kills += 1
        else:
            hero.player_kills += 1
            game.enemy.deaths += 1
            location = database.get_object_by_name('Location', game.enemy.last_city.name)
            game.enemy.current_location = location
        if len(game.enemy.items_rewarded) > 0:
            for item in game.enemy.items_rewarded:
                if not any(items.name == item.name for items in hero.inventory):
                    hero.inventory.append(item)
                else:
                    for items in hero.inventory:
                        if items.name == item.name:
                            items.amount_owned += 1
        page_title = "Victory!"
        page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(
            experience_gained) + " experience!"
        page_links = [("Return to where you ", hero.current_location.url, "were", ".")]
        hero.current_dungeon_monster = False
        if level_up:
            page_heading += " You have leveled up! You should return to your profile page to advance in skill."
            page_links = [("Return to your ", "/home", "profile", " page and distribute your new attribute points."),
                          ("Return to where you ", "/explore_dungeon/Explore%20Dungeon/Entering", "were", ".")]

    # Return an html page built from a Jinja2 form and the passed data.
    return render_template(
        'battle.html', page_title=page_title, page_heading=page_heading,
        battle_log=battle_log, hero=hero, enemy=game.enemy,
        page_links=page_links)


# a.k.a. "Blacksmith"
@app.route('/store/<name>')
@login_required
@uses_hero
@update_current_location
# @spawns_event
def store(name, hero=None, location=None):
    page_title = "Store"
    items_for_sale = []
    if name == "Blacksmith":
        page_links = [("Take a look at the ", "/store/armoury", "armour", "."), ("Let's see what ", "/store/weaponry", "weapons", " are for sale.")]
        return render_template('store.html', hero=hero, page_title=page_title, page_links=page_links)  # return a string
    elif name == "armoury":
        page_links = [("Let me see the ", "/store/weaponry", "weapons", " instead.")]
        for item in database.get_all_store_items():
            if item.garment or item.jewelry:
                items_for_sale.append(item)
    elif name == "weaponry":
        page_links = [("I think I'd rather look at your ", "/store/armoury", "armour", " selection.")]
        for item in database.get_all_store_items():
            if item.weapon:
                items_for_sale.append(item)
    return render_template('store.html', hero=hero, items_for_sale=items_for_sale, page_title=page_title,
                           page_links=page_links)  # return a string



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
    page_title = "Marketplace"
    items_for_sale = []
    if inventory == "Marketplace":
        page_links = [("Take a look at our ", "/marketplace/general", "selection", "."), ("Return to ", hero.current_city.url, "town", ".")]
        return render_template('store.html', hero=hero, page_title=page_title, page_links=page_links)  # return a string
    elif inventory == "general":
        page_links = [("Let me go back to the ", "/marketplace/Marketplace", "marketplace", " instead.")]
        items_for_sale = database.get_all_marketplace_items()
    return render_template('store.html', hero=hero, items_for_sale=items_for_sale, page_title=page_title,
                           page_links=page_links)  # return a string


@app.route('/house/<name>')
@login_required
@uses_hero
def house(name='', hero=None):
    """A web page for a house.

    Returns a rendered html page.
    """
    location = database.get_object_by_name('Location', name)
    return render_template('generic_location.html', hero=hero)


@app.route('/gate/<name>')
@login_required
@uses_hero
def leave_town(name='', hero=None):
    location = database.get_object_by_name('Location', name)
    conversation = [
        ("City Guard: ", "You are too young to be out on your own.")]
    page_links = [
        ("Return to the ", "/Town/" + hero.current_city.name, "city", ".")]
    return render_template('gate.html', hero=hero,
                           page_heading=location.display.page_heading,
                           conversation=conversation,
                           page_links=page_links)  # return a string
# END OF STARTING TOWN FUNCTIONS


# This gets called anytime a button gets clicked in html using
# <button class="command", value="foo">. "foo" is what gets sent to this
# Python code.
# need to make sure this doesn't conflict with other routes
@app.route('/command/<cmd>', methods=['GET', 'POST'])
@uses_hero
def command(cmd=None, hero=None):
    """Accept a string from HTML button code -> send back a response.

    The response must be in the form: "key=value" (at this time.)
    See the Command class in the commands.py module.
    cmd is equal to the value of the value field in the html code
    i.e. <button value='foo'> -> cmd == 'foo'

    Extra data can be sent in request.args (which is accessible from within this namespace).

    args are sent in the form "/" + command + "?key=value&&key2=value2".
    Where the value of command == cmd and
    args == {key: value, key2: value2} (well it isn't a real dict but it mostly acts like one).

    Or you could sent the data as a file ... or raw or some XML or something
    and then parse it on this end based on the headers. But that is more complicated
    than I need right now.
    """

    testing = False  # True/False
    if testing:
        print('request is:', repr(request))
        # print('request data:', repr(request.data))
        # print("request form:", repr(request.form))
        print('request view_args:', repr(request.view_args))
        print('request args:', repr(request.args))
        print('cmd is:', repr(cmd))

    # event = Event(request.args)
    # event.add["hero"] = hero
    # event.add["database"] = database

    response = None
    try:
        # command_function = getattr(Command, <cmd>)
        # response = command_function(hero, database,
        #   javascript_kwargs_from_html)
        command_function = Command.cmd_functions(cmd)
    except AttributeError as ex:
        if str(ex) == "type object 'Command' has no attribute '{}'".format(
                cmd):
            print("You need to write a static function called '{}' in "
                  "commands.py in the Command class.".format(cmd))
            raise ex
        raise ex

    if request.method == 'POST' and request.is_json:
        try:
            data = request.get_json()
        except werkzeug.exceptions.BadRequest as ex:
            # This might be a terrible idea as maybe it lets people crash
            # the server by sending invalid data?
            # I figure that this error shouldn't pass silently with no idea
            # what caused it.
            raise Exception(str(ex))
        response = command_function(hero, database, data=data,
                                    engine=engine)
    else:
        response = command_function(hero, database=database,
                                arg_dict=request.args, engine=engine)
    # pdb.set_trace()
    return response


@app.route('/about')
@uses_hero
def about_page(hero=None):
    info = "The game is being created by Elthran and Haldon, with some help " \
           "from Gnahz. Any inquiries can be made to elthranRPG@gmail.com"
    return render_template('about.html', hero=hero, page_title="About",
                           gameVersion="0.00.02", about_info=info)


###testing by Marlen ####
@app.route('/')
def main():
    """Redirects user to a default first page

    Currently the login page.
    """
    return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    # import os

    # Set Current Working Directory (CWD) to the home of this file.
    # This should make all other files import relative to this file fixing the Database doesn't exist problem.

    # os.chdir(os.path.dirname(os.path.abspath(__file__)))


    # Not implemented ... should be moved to prebuilt_objects.py and implemented in
    # database.py as get_default_quests()
    # Quest aren't actually implement yet but they will be soon!
    # Super temporary while testing quests
    # hero.inventory.append(QuestItem("Wolf Pelt", hero, 50))
    # hero.inventory.append(QuestItem("Spider Leg", hero, 50))
    # hero.inventory.append(QuestItem("Copper Coin", hero, 50))
    # for item in hero.inventory:
    #     item.amount_owned = 5

    # Remove when not testing.
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.auto_reload = True
    app.run(debug=True)

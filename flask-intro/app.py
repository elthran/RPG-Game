#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

# from game import * #Must go before login method???
from game import Hero, Game
# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from combat_simulator import *
from bestiary import *
import database
from items import Quest_Item
from commands import Command

#MUST be imported after all other game objects but before any of them are used.
import complex_relationships 

#Last module to be imported (of our custom ones)

#Marked for restructure: probably should only be used in Hero object (in game.py) directly.
#If it is needed elsewhere the method should be moved to the Hero object.
from secondary_attributes import * 
import sqlite3
import hashlib

#For testing!
import pdb

# INIT AND LOGIN FUNCTIONS

# create the application object
app = Flask(__name__)
app.secret_key = 'starcraft'

def login_required(f):
    """Set certain pages as requiring a login to visit.

    This should redirect you to the login page."""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#Not implemented. Control user moves on map.    
def prevent_url_typing(f):
    """Set certain pages as requiring a login to visit.

    This should redirect you to the login page.
    This needs a lot more work. It should be dealing with actual URLs ...
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            requested_move = set([kwargs['location_id']])
        except KeyError:
            pass
        try: 
            requested_move = set([kwargs['cave_name']])
        except KeyError:
            pass
        try:
            requested_move = set([kwargs['town_name']])
        except KeyError:
            pass
        pdb.set_trace()    
        if 'valid_moves' in session and any(move in session['valid_moves'] for move in requested_move):
            return f(*args, **kwargs)
        else:
            flash("You can't access that location from here.")
            return redirect(url_for(f))
    return wrap

# use decorators to link the function to a url
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Allow user to login if username and password match.

    Access data from the static/user.db using the EasyDatabase class.
    """
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.validate(username, password):
            session['logged_in'] = True
            flash("LOG IN SUCCESSFUL")
            session['id'] = database.get_user_id(username)
            
            #I recommend a dialogue here to select the specific hero that the user wants to play with.
            #Or a page redirect whatever ...
            session['hero_id'] = database.fetch_hero(username).id #Gets the hero's id.
            
            return redirect(url_for('home'))
        #Marked for upgrade, consider checking if user exists and redirect to account creation page.
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('index.html', error=error, login=True)

# route for handling the account creation page logic
@app.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    error = "Password Not Found"

    if request.method == 'POST':
        username = request.form['username']

        con = sqlite3.connect('static/user.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Users")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    error = "We found your password, but it was hashed into this: " + row[1] + ". We are unable to decode the jargon. Sorry, please restart the game!"
        con.close()
    return render_template('index.html', error=error, password_recovery=True)

# route for handling the account creation page logic
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.get_user_id(username):
            error = "Username already exists!"
        else:
            database.add_new_user(username, password)
            database.add_new_character(username_or_id=username)
            # database.add_world_map_to_hero() maybe?
            return redirect(url_for('login'))
    database.update()
    return render_template('index.html', error=error, create_account=True)

# this gets called if you press "logout"
@app.route('/logout')
@login_required
def logout():
    # pdb.set_trace()
    myHero.refresh_character()
    database.update() ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    session.pop('logged_in', None)
    flash("Thank you for playing! Your have successfully logged out.")
    return redirect(url_for('login'))

# this gets called if you are logged in and there is no character info stored
@app.route('/create_character', methods=['GET', 'POST'])
@login_required
def create_character():
    display = True
    fathers_job = None
    page_title = "Create Character"
    page_heading = "A New Beginning"
    page_image = "beached"
    paragraph = "You awake to great pain and confusion as you hear footsteps approaching in the sand. Unsure of where you are, you quickly look around for something to defend yourself. A firm and inquisitive voice pierces the air."
    conversation = [("Stranger: ", "Who are you and what are you doing here?")]
    if len(myHero.quest_paths) == 0:
        #pdb.set_trace()
        for quest in database.get_default_quests():
            quest.add_hero(myHero)
    if request.method == 'POST' and myHero.name == None:
        myHero.name = request.form["name"]
        page_image = "old_man"
        paragraph = None
        conversation = [("Stranger: ", "Where do you come from, child?")]
        display = False
    elif request.method == 'POST' and fathers_job == None:
        fathers_job = request.form["archetype"]
        if fathers_job == "Brute":
            myHero.primary_attributes["Strength"] += 3
        elif fathers_job == "Scholar":
            myHero.primary_attributes["Wisdom"] += 3
        elif fathers_job == "Hunter":
            myHero.primary_attributes["Survivalism"] += 3
        elif fathers_job == "Merchant":
            myHero.primary_attributes["Charisma"] += 2
            myHero.gold += 50
        elif fathers_job == "Priest":
            myHero.primary_attributes["Divinity"] += 3
    if myHero.character_name != None and fathers_job != None:
        myHero.archetype = fathers_job
        database.update()
        return redirect(url_for('home'))
    else:
        database.update()
        return render_template('create_character.html', page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, conversation=conversation, display=display)  # render a template

# this is a temp button that can call this to erase your chracter information and redirect you to the create character page
@app.route('/reset_character')
@login_required
def reset_character():
    myHero = create_random_hero()
    game = Game(myHero)
    return redirect(url_for('home'))  # return a string

# this is a temporary page that lets you modify any attributes for testing
@app.route('/admin',methods=['GET', 'POST'])
@login_required
def admin():
    page_title = "Admin"
    if request.method == 'POST':
        # pdb.set_trace()
        myHero.age = convert_input(request.form["Age"])
        myHero.current_exp = convert_input(request.form["Current_exp"])
        myHero.max_exp = convert_input(request.form["Max_exp"])
        myHero.renown = convert_input(request.form["Renown"])
        myHero.virtue = convert_input(request.form["Virtue"])
        myHero.devotion = convert_input(request.form["Devotion"])
        myHero.gold = convert_input(request.form["Gold"])
        myHero.ability_points = convert_input(request.form["Ability_points"])
        # myHero.basic_ability_points = convert_input(request.form["Basic_ability_points"])
        # myHero.archetype_ability_points = convert_input(request.form["Archetype_ability_points"])
        # myHero.specialization_ability_points = convert_input(request.form["Specialization_ability_points"])
        # myHero.pantheonic_ability_points = convert_input(request.form["Pantheonic_ability_points"])
        myHero.attribute_points = convert_input(request.form["Attribute_points"])
        myHero.proficiency_points = convert_input(request.form['Proficiency_Points'])
        myHero.primary_attributes["Agility"] = convert_input(request.form["Agility"])
        myHero.primary_attributes["Fortitude"] = convert_input(request.form["Fortitude"])
        myHero.update_secondary_attributes()
        myHero.refresh_character()
        database.update()
        return redirect(url_for('home'))

    admin = [("Age", myHero.age),
        ("Current_exp", myHero.current_exp),
        ("Max_exp", myHero.max_exp),
        ("Renown", myHero.renown),
        ("Virtue", myHero.virtue),
        ("Devotion", myHero.devotion),
        ("Gold", myHero.gold),
        ("Ability_points", myHero.ability_points),
        ("Attribute_points", myHero.attribute_points),
        ("Proficiency_Points", myHero.proficiency_points),
        ("Agility", myHero.primary_attributes["Agility"]),
        ("Fortitude", myHero.primary_attributes["Fortitude"])]

    return render_template('admin.html', page_title=page_title, myHero=myHero, admin=admin)  # return a string

@app.route('/display_users')	
def display_user_page():
	users = database.session.query(User).order_by(User.id).all()
	return render_template('users.html', myHero=myHero, users=users)

### PROFILE PAGES (Basically the home page of the game with your character display and stats)
    
@app.route('/home')
@login_required
def home():
    global myHero
    myHero = database.fetch_hero(session['hero_id'])
    database.update_time(myHero) #Or is this supposed to update the time of all hero objects?
    #This should be uneccessary -> but isn't?
    myHero.update_secondary_attributes()
    
    # pdb.set_trace()
    #Consider moving this to the login function? Or instantiate during "create_account?"
    # initialize current_world
    if myHero.current_world == None:
        myHero.current_world = database.get_default_world()
        myHero.current_location = database.get_default_location()
        database.update()
    
    #Not implemented. Control user moves on map.
    #Sets up initial valid moves on the map.
    # Should be a list of urls ...
    # session['valid_moves'] = myHero.current_world.show_directions(myHero.current_location)
    # session['valid_moves'].append(myHero.current_location.id)
        
    # If it's a new character, send them to cerate_character url
    if myHero.character_name == None:
        return redirect(url_for('create_character'))
    return render_template('profile_home.html', page_title="Profile", myHero=myHero, profile=True)  # return a string'

# This gets called anytime you have secondary attribute points to spend
# Currently I send "attributes=True" so that the html knows to highlight the bar and show that you are on this page
@app.route('/attributes', methods=['GET', 'POST'])
@login_required
def attributes():
    #Obviously this is a shitty way to do this, but I'm not sure where else to store this
    #information for now. Probably as part of the hero class so it's easily sent to each html file.
    #Or some global table that we send to each html file with the hero.
    
    #Possibly update the PrimaryAttribute table and add in a "description"?
    #Would require some restructuring.
    attribute_information = [("Agility", "A measure of how agile a character is. Dexterity controls attack and movement speed and accuracy, as well as evading an opponent's attack ."),
                             ("Charisma", "A measure of a character's social skills, and sometimes their physical appearance."),
                             ("Divinity", "A measure of a character's common sense and/or spirituality."),
                             ("Fortitude", "A measure of how resilient a character is."),
                             ("Fortuity", "A measure of a character's luck. "),
                             ("Perception", "A measure of a character's openness to their surroundings."),
                             ("Reflexes", "A measure of how agile a character is. "),
                             ("Resilience", "A measure of how resilient a character is. "),
                             ("Strength", "A measure of how physically strong a character is. "),
                             ("Survivalism", "A measure of a character's openness to their surroundings. "),
                             ("Vitality", "A measure of how sturdy a character is."),
                             ("Wisdom", "A measure of a character's problem-solving ability.")]
    
    #Fix single quotes in string bug when converting from JS to HTML
    #Python to Jinja to HTML to JS needs separate fix.
    for index, data in enumerate(attribute_information):
        attribute, description = data
        attribute_information[index] = attribute, description.replace("'", "\\'")

    if request.method == 'POST':
        points_spent = 0
        for element in request.form:
            form_value = int(request.form[element])
            attribute = element[0:-5].title() #Convert name e.g. agilityInput becomes Agility.
            points_spent += form_value - myHero.primary_attributes[attribute]
            myHero.primary_attributes[attribute] = form_value
        
        myHero.attribute_points -= points_spent

        myHero.update_secondary_attributes()
        myHero.refresh_character()
        myHero.proficiency_test.update_testing(myHero) # TEMP. Testing. Will be a new function that updates all proficiencies soon
        database.update()
        return render_template('profile_attributes.html', page_title="Attributes", myHero=myHero, attribute_information=attribute_information)
    return render_template('profile_attributes.html', page_title="Attributes", myHero=myHero, attribute_information=attribute_information)

# This gets called anytime you have secondary attribute points to spend
# Currently I send "proficiencies=True" so that the html knows to highlight the bar and show that you are on this page
@app.route('/proficiencies', methods=['GET', 'POST'])
@login_required
def proficiencies():
    if request.method == 'POST':
        if (myHero.proficiency_test.level + convert_input(request.form["testplz"])) <= myHero.proficiency_test.max_level:
            myHero.proficiency_test.level += convert_input(request.form["testplz"])
            myHero.proficiency_points -= convert_input(request.form["testplz"])
            myHero.proficiency_test.update_testing(myHero)
            myHero.refresh_character()
            database.update()
            return render_template('profile_proficiencies.html', page_title="Proficiencies", myHero=myHero, proficiencies=True)
    return render_template('profile_proficiencies.html', page_title="Proficiencies", myHero=myHero, proficiencies=True)

@app.route('/ability_tree/<spec>')
@login_required
def ability_tree(spec):
    page_title = "Abilities"
    
    unknown_abilities = []
    learnable_abilities = []
    mastered_abilities = []
    
    # Create a list of learned abilities that match current spec.  
    for ability in myHero.abilities: 
        if ability.ability_type == spec:
            # Add abilities to learnable_abilities (known, but non-mastered)
            # or mastered abilities
            if ability.level < ability.max_level: 
                learnable_abilities.append(ability)
            else:
                mastered_abilities.append(ability)
                
    if myHero.ability_points > 0:
        for ability in database.get_all_abilities():
            # Create a list of unlearned abilities
            # for the current page you are on (basic, archetype, specialization, religion)
            if ability not in myHero.abilities and ability.type == spec: 
                if spec == "Archetype": # If you are on the archetype page, we further narrow it down to your archetype and "all"
                    if ability.archetype == myHero.archetype or ability.archetype == "All":
                        unknown_abilities.append(ability)
                elif spec == "Class": # If you are on the specialization page, we further narrow it down to your specialization and "all"
                    if ability.specialization == myHero.specialization or ability.specialization=="All":
                        unknown_abilities.append(ability)
                elif spec == "Religious": # If you are on the religion page, we further narrow it down to your religion and "all"
                    if ability.religion == myHero.religion or ability.religion == "All":
                        unknown_abilities.append(ability)
                else:
                    unknown_abilities.append(ability)            
        return render_template('profile_ability.html', myHero=myHero, ability_tree=spec, unknown_abilities=unknown_abilities,
                               learnable_abilities=learnable_abilities, mastered_abilities=mastered_abilities, page_title=page_title)
        
    return render_template('profile_ability.html', myHero=myHero, ability_tree=spec, unknown_abilities=unknown_abilities,
                           learnable_abilities=learnable_abilities, mastered_abilities=mastered_abilities, page_title=page_title)

@app.route('/inventory_page')
@login_required
def inventory_page():
    page_title = "Inventory"
    # for item in myHero.inventory:
        # if item.wearable:
            # item.check_if_improvement()
    return render_template('inventory.html', myHero=myHero, page_title=page_title)  # return a string

@app.route('/quest_log')
@login_required
def quest_log():
    myHero.page_refresh_character()
    page_title = "Quest Log"
    return render_template('journal.html', myHero=myHero, quest_log=True, page_title=page_title)  # return a string

@app.route('/bestiary/<current_monster_id>')
@login_required
def bestiary(current_monster_id):
    if current_monster_id == "default":
        current_monster = None
    else:
        for monster in bestiary_data:
            if monster.monster_id == current_monster_id:
                current_monster = monster
                break
    page_title = "Bestiary"
    return render_template('journal.html', myHero=myHero, bestiary=True, page_title=page_title, bestiary_data=bestiary_data, current_monster=current_monster)  # return a string

@app.route('/people_log/<current_npc>')
@login_required
def people_log(current_npc):
    if current_npc == "default":
        current_npc = None
    else:
        for npc in npc_data:
            if npc.npc_id == current_npc:
                current_npc = npc
                break
    page_title = "People"
    return render_template('journal.html', myHero=myHero, people_log=True, page_title=page_title, npc_data=npc_data, current_npc=current_npc)  # return a string

@app.route('/map_log')
@login_required
def map_log():
    page_title = "Map"
    return render_template('journal.html', myHero=myHero, map_log=True, page_title=page_title)  # return a string

@app.route('/achievement_log')
@login_required
def achievement_log():
    page_title = "Achievements"
    return render_template('journal.html', myHero=myHero, achievement_log=True, completed_achievements=myHero.completed_achievements, page_title=page_title)  # return a string

@app.route('/under_construction')
@login_required
def under_construction():
    page_title = "Under Construction"
    return render_template('layout.html', page_title=page_title)  # return a string

### END OF PROFILE/DISPLAY FUNCTIONS



### TOWN FUNCTIONS

@app.route('/Town/<town_name>')
@login_required
#Not implemented. Control user moves on map.
# @prevent_url_typing
def town(town_name):
    #Marked for refractor as ineficient if easy to understand.
    #These should just be part of the basic world_map function as they don't actually
    #add anything yet.
    for location in myHero.current_world.all_map_locations:
        if location.name == town_name:
            myHero.current_location = location
            break

    page_title = myHero.current_city.display.page_title
    places_of_interest = myHero.current_city.display.places_of_interest
    database.update()
    return render_template('town.html', myHero=myHero, page_title=page_title, places_of_interest=places_of_interest )  # return a string

@app.route('/Cave/<cave_name>') # Test function while experimenting with locations
@login_required
#Not implemented. Control user moves on map.
# @prevent_url_typing
def cave(cave_name):
    #Marked for refractor as ineficient if easy to understand.
    #Maybe a search function?
    #myHero.current_city = myHero.current_world.get_city(cave_name)?
    for location in myHero.current_world.all_map_locations:
        if location.name == cave_name:
            myHero.current_location = location
            break
    page_title = myHero.current_city.display.page_title
    page_heading = myHero.current_city.display.page_heading
    page_image = myHero.current_city.display.page_image
    paragraph = myHero.current_city.display.paragraph
    places_of_interest = myHero.current_city.display.places_of_interest
    database.update()
    return render_template('cave.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, places_of_interest=places_of_interest)  # return a string

@app.route('/WorldMap/<current_world>/<int:location_id>') # Test function while experimenting with locations
@login_required
#Not implemented. Control user moves on map.
# @prevent_url_typing
def world_map(current_world, location_id):
    """Set up World Map web page. Return html string/web page.
    
    I don't know where the arguments come from? Or why they are passed.
    I will try and figure it out.
    """
    # pdb.set_trace()
    
    #Very important as current_world is a string variable and should be the object itself.
    current_world = myHero.current_world
    
    #Updates current id. May be redundant. Or it may allow page to be dynamic.
    #May have originally compensated for the lack of a database.
    current_location = current_world.find_location(location_id)
    
    #Needs to be reimplemented/or removed
    # myHero.known_locations.append(current_world)
    # myHero.current_city = None #?
    
    move_on_the_map = current_world.show_directions(current_location)
    myHero.current_location = current_location
    database.update()
    
    
    #Debug Me! Use current_world.display?
    # Check render of places_of_interest
    page_title = current_world.display.page_title
    page_heading = current_world.display.page_heading
    page_image = current_world.display.page_image
    paragraph = current_world.display.paragraph
    places_of_interest = current_world.display.places_of_interest
    
    #Not implemented. Control user moves on map.
    #Should be a list of urls ...
    # session['valid_moves'] = move_on_the_map
    
    return render_template('world_map.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, places_of_interest=places_of_interest, move_on_the_map=move_on_the_map)  

@app.route('/barracks')
@login_required
def barracks():
    if myHero.current_health <= 0:
        page_heading = "Your hero is currently dead."
        page_image = "dead"
        page_links = ["","","",""]
    else:
        page_heading = "Welcome to the arena " + myHero.name+"!"
        page_image = "arena"
        page_links = [("Compete in the ", "/arena","arena", ".(temporary)"), ("Pay to ", "/spar", "spar", " against the trainer."), ("Battle another ", "/under_construction", "player",".")]
    return render_template('building_default.html', page_title="Barracks", page_heading=page_heading, page_image=page_image, myHero=myHero, game=game, page_links=page_links)  # return a string

#From /barracks
@app.route('/spar')
@login_required
def spar():
    spar_cost = 50
    spar_benefit = 5
    if myHero.gold < spar_cost:
        page_heading = "You do not have enough gold to spar."
    else:
        myHero.gold -= spar_cost
        myHero.current_exp += spar_benefit * myHero.experience_gain_modifier
        page_heading = str("You spend some time sparring with the trainer at the barracks. You spend " + str(spar_cost) + " gold and gain " + str(spar_benefit) + " experience.")
    return render_template('building_default.html', page_title="Sparring Room", page_heading=page_heading, myHero=myHero, game=game)  # return a string

#From /barracks
@app.route('/arena')
@login_required
def arena():
    if not game.has_enemy or game.enemy.current_health <= 0:
        enemy = monster_generator(myHero.age)
        if enemy.name == "Wolf":
            enemy.items_rewarded.append((Quest_Item("Wolf Pelt", myHero, 50)))
        if enemy.name == "Scout":
            enemy.items_rewarded.append((Quest_Item("Copper Coin", myHero, 50)))
        if enemy.name == "Spider":
            enemy.items_rewarded.append((Quest_Item("Spider Leg", myHero, 50)))
        game.set_enemy(enemy)
    page_heading = "Welcome to the arena " + myHero.name +"!"
    page_image = str(game.enemy.name)
    conversation = [("Name: ", str(game.enemy.name), "Enemy Details"),
                    ("Level: ", str(game.enemy.level), "Combat Details"),
                    ("Damage: ", str(game.enemy.minimum_damage) + " - " + str(game.enemy.maximum_damage)),
                    ("Attack Speed: ", str(game.enemy.attack_speed)),
                    ("Accuracy: ", str(game.enemy.attack_accuracy) + "%"),
                    ("First Strike: ", str(game.enemy.first_strike) + "%"),
                    ("Critical Hit Chance: ", str(game.enemy.critical_hit_chance) + "%"),
                    ("Critical Hit Modifier: ", str(game.enemy.critical_hit_modifier)),
                    ("Defence: ", str(game.enemy.defence_modifier) + "%"),
                    ("Evade: ", str(game.enemy.evade_chance) + "%"),
                    ("Parry: ", str(game.enemy.parry_chance) + "%"),
                    ("Riposte: ", str(game.enemy.riposte_chance) + "%"),
                    ("Block Chance: ", str(game.enemy.block_chance) + "%"),
                    ("Block Reduction: ", str(game.enemy.block_reduction) + "%"),
                    ("Stealth: ", str(game.enemy.stealth_skill) + "%"),
                    ("Faith: ", str(game.enemy.faith)),
                    ("Sanctity: ", str(game.enemy.current_sanctity) + "/" + str(game.enemy.max_sanctity)),
                    ("Luck: ", str(game.enemy.luck)),
                    ("Health: ", str(game.enemy.current_health) + " / " + str(game.enemy.max_health))]
    page_links = [("Challenge the enemy to a ","/battle","fight","."), ("Go back to the ","/barracks","barracks",".")]
    return render_template('building_default.html', page_title="War Room", page_heading=page_heading, page_image=page_image, myHero=myHero, game=game, page_links=page_links, enemy_info=conversation)  # return a string

# this gets called if you fight in the arena
@app.route('/battle')
@login_required
def battle():
    required_endurance = 1 # T

    page_title = "Battle"
    page_heading = "Fighting"
    print("running function: battle2")

    page_links = [("Return to your ","home","profile"," page.")]
    if myHero.current_endurance < required_endurance:
        page_title = "Battle"
        page_heading = "Not enough endurance, wait a bit!"
        return render_template('layout.html', page_title=page_title, myHero=myHero, page_heading=page_heading, page_links=page_links)

    myHero.current_health,game.enemy.current_health,battle_log,battle_results = battle_logic(myHero,game.enemy)
    if myHero.current_health == 0:
        myHero.current_endurance -= required_endurance
        page_title = "Defeat!"
        page_heading = "You have died."
    else:
        myHero.current_endurance -= required_endurance
        for item in myHero.equipped_items:
            item.durability -= 1
            if item.durability <= 0:
                item.broken = True
        newMonster = True
        """
        for key, value in myHero.kill_quests.items():
            if key == game.enemy.species:
                myHero.kill_quests[key] += 1
                if myHero.kill_quests[key] == 2:
                    for achievement in myHero.completed_achievements:
                        if achievement[0] == "Kill a " + game.enemy.species:
                            myHero.completed_achievements.remove(achievement)
                            break
                    myHero.completed_achievements.append(("Kill two " + game.enemy.species_plural, "10"))
                    myHero.current_exp += 10
                newMonster = False
                break
        """
        if newMonster:
            #myHero.kill_quests[game.enemy.species] = 1
            myHero.completed_achievements.append(("Kill a " + game.enemy.species, "5"))
            for monster in bestiary_data:
                if monster.name == game.enemy.name:
                    myHero.bestiary.append(monster)
            myHero.current_exp += 5
        game.has_enemy = False
        myHero.current_exp += game.enemy.experience_rewarded * myHero.experience_gain_modifier
        if len(game.enemy.items_rewarded) > 0:
            for item in game.enemy.items_rewarded:
                if not any(items.name == item.name for items in myHero.inventory):
                    myHero.inventory.append(item)
                else:
                    for items in myHero.inventory:
                        if items.name == item.name:
                            items.amount_owned += 1
        level_up = myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        page_title = "Victory!"
        page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience!"
        page_links = [("Compete in the ","/arena","arena","."), ("Go back to the ","/barracks","barracks","."), ("Return to your ","/home","profile"," page.")]
        if level_up:
            page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience. You have leveled up! You should return to your profile page to advance in skill."
            page_links = [("Return to your ","/home","profile"," page and distribute your new attribute points.")]

    database.update()
    return render_template('battle.html', page_title=page_title, page_heading=page_heading, battle_log=battle_log, battle_results=battle_results, myHero=myHero, enemy=game.enemy, page_links=page_links)  # return a string

#A.k.a "Blacksmith"
@app.route('/store/<inventory>')
@login_required
def store(inventory):
    page_title = "Store"
    
    # path = database.get_path_if_exists_and_active(quest_name, myHero)
    # if path in myHero.quest_paths:
        # path.advance()
    for path in myHero.quest_paths:
        if path.active and path.quest.name == "Get Acquainted with the Blacksmith" and path.stage == 1:
            path.advance()
    items_for_sale = []
    if inventory == "greeting":
        page_links = [("Take a look at the ", "/store/armoury", "armour", "."), ("Let's see what ", "/store/weaponry", "weapons", " are for sale.")]
        return render_template('store.html', myHero=myHero, page_title=page_title, page_links=page_links)  # return a string
    elif inventory == "armoury":
        page_links = [("Let me see the ", "/store/weaponry", "weapons", " instead.")]
        for item in database.get_all_store_items():
            if item.garment or item.jewelry:
                items_for_sale.append(item)
    elif inventory == "weaponry":
        page_links = [("I think I'd rather look at your ", "/store/armoury", "armour", " selection.")]
        for item in database.get_all_store_items():
            if item.weapon:
                items_for_sale.append(item)
    return render_template('store.html', myHero=myHero, items_for_sale=items_for_sale, page_title=page_title, page_links=page_links)  # return a string

@app.route('/tavern', methods=['GET', 'POST'])
@login_required
def tavern():
    tavern=True
    page_title = "Tavern"
    page_heading = "You enter the Red Dragon Inn."
    page_image = "bartender"
    if "Become an apprentice at the tavern." in myHero.completed_quests:
        paragraph = "Welcome, my apprentice!"
    else:
        paragraph = "Greetings traveler! What can I get for you today?"
    page_links = [("Return to ", "/tavern", "tavern", ".")] # I wish it looked like this
    dialogue_options = {"Drink": "Buy a drink for 25 gold. (This fully heals you)"}
    if "Collect 2 Wolf Pelts for the Bartender" not in myHero.errands and "Collect 2 Wolf Pelts for the Bartender" not in myHero.completed_quests:
        dialogue_options["Jobs"] = "Ask if there are any jobs you can do."
    if "Collect 2 Wolf Pelts for the Bartender" in myHero.errands:
        if any(item.name == "Wolf Pelt" and item.amount_owned >= 2 for item in myHero.inventory):
            dialogue_options["HandInQuest"] = "Give the bartender 2 wolf pelts."
        else:
            dialogue_options["QuestNotFinished"] = "I'm still looking for the 2 wolf pelts."
    if "Collect 2 Wolf Pelts for the Bartender" in myHero.completed_quests:
        if any(quest[0] == "Become an apprentice at the tavern." and quest[2] == 1 for quest in myHero.current_quests):
            if any(item.name == "Copper Coin" and item.amount_owned >= 2 for item in myHero.inventory):
                dialogue_options["HandInQuest2"] = "Give the bartender 2 copper coins."
            else:
                dialogue_options["QuestNotFinished"] = "I'm still looking for the two copper coins."
        elif any(quest[0] == "Become an apprentice at the tavern." and quest[2] == 2 for quest in myHero.current_quests):
            if any(item.name == "Spider Leg" and item.amount_owned >= 1 for item in myHero.inventory):
                dialogue_options["HandInQuest3"] = "Give the bartender a spider leg."
            else:
                dialogue_options["QuestNotFinished"] = "I'm still looking for the spider leg."
        elif "Become an apprentice at the tavern." not in myHero.completed_quests:
            dialogue_options["Jobs2"] = "Do you have any other jobs you need help with?"
    if request.method == 'POST':
        tavern=False
        paragraph = ""
        dialogue_options = {}
        tavern_choice = request.form["tavern_choice"]
        if tavern_choice == "Drink":
            if myHero.gold >= 25:
                myHero.current_health = myHero.max_health
                myHero.gold -= 25
                page_heading = "You give the bartender 25 gold and he pours you a drink. You feel very refreshed!"
            else:
                page_heading = "Pay me 25 gold first if you want to see your drink."
        elif tavern_choice == "Jobs":
            myHero.errands.append("Collect 2 Wolf Pelts for the Bartender")
            page_heading = "The bartender has asked you to find 2 wolf pelts!"
            page_image = ""
        elif tavern_choice == "HandInQuest":
            myHero.gold += 5000
            myHero.errands = [(name, stage) for name, stage in myHero.current_quests if name != "Collect 2 Wolf Pelts for the Bartender"]
            myHero.completed_quests.append(("Collect 2 Wolf Pelts for the Bartender"))
            page_heading = "You have given the bartender 2 wolf pelts and completed your quest! He has rewarded you with 5000 gold."
        elif tavern_choice == "QuestNotFinished":
            page_heading = "Don't take too long!"
        elif tavern_choice == "Jobs2":
            page_heading = "Actually, I could use a hand with something if you are interested in becoming my apprentice. First I will need 2 copper coins. Some of the goblins around the city are carrying them."
            myHero.current_quests.append(["Become an apprentice at the tavern.", "You need to find two copper coins and give them to the blacksmith", 1])
        elif tavern_choice == "HandInQuest2":
            myHero.current_quests[0][1] = "Now the bartender wants you to find a spider leg."
            myHero.current_quests[0][2] += 1
            page_heading = "Fantastic! Now I just need a spider leg."
        elif tavern_choice == "HandInQuest3":
            myHero.current_quests = [quest for quest in myHero.current_quests if quest[0] != "Become an apprentice at the tavern."]
            myHero.completed_quests.append("Become an apprentice at the tavern.")
            page_heading = "You are now my apprentice!"
    return render_template('tavern.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, tavern=tavern, dialogue_options=dialogue_options)  # return a string

@app.route('/marketplace/<inventory>')
@login_required
def marketplace(inventory):
    page_title = "Marketplace"
    items_for_sale = []
    if inventory == "greeting":
        page_links = [("Take a look at our ", "/marketplace/general", "selection", "."), ("Return to ", "/Town/" + myHero.current_city.name, "town", ".")]
        return render_template('store.html', myHero=myHero, page_title=page_title, page_links=page_links)  # return a string
    elif inventory == "general":
        page_links = [("Let me go back to the ", "/marketplace/greeting", "marketplace", " instead.")]
        for item in database.get_all_marketplace_items():
            if isinstance(item, Consumable):
                items_for_sale.append(item)
    return render_template('store.html', myHero=myHero, items_for_sale=items_for_sale, page_title=page_title, page_links=page_links)  # return a string

@app.route('/old_mans_hut')
@login_required
def old_mans_hut():
    page_heading = "Old Man's Hut"
    page_image = "hut"
    paragraph = "Nice to see you again kid. What do you need?"
    return render_template('layout.html', myHero=myHero, page_title="Old Man's Hut", page_heading=page_heading, page_image=page_image, paragraph=paragraph)  # return a string

@app.route('/leave_town')
@login_required
def leave_town():
    page_heading = "Village Gate"
    conversation = [("City Guard: ", "You are too young to be out on your own.")]
    page_links = [("Return to the ", "/Town/" + myHero.current_city.name, "city", ".")]
    return render_template('layout.html', myHero=myHero, page_heading=page_heading, conversation=conversation, page_links=page_links)  # return a string

### END OF STARTING TOWN FUNCTIONS

# This gets called anytime a button gets clicked in html using
# <button class="command", value="foo">. "foo" is what gets sent to this
# Python code.
@app.route('/<cmd>') # need to make sure this doesn't conflict with other routes
def command(cmd=None):
    """Accept a string from HTML button code -> send back a response.
    
    The respose must be in the form: "key=value" (at this time.)
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
    if cmd == 'favicon.ico':
        return "success", 200, {'Content-Type': 'text/plain'}
    
    testing = True
    if testing:
        print('request is:', repr(request))
        # print('request data:', repr(request.data))
        # print("request form:", repr(request.form))
        print('request view_args:', repr(request.view_args))
        print('request args:', repr(request.args))
        print('cmd is:', repr(cmd))
        
    # event = dict(request.args)
    # event.add["hero"] = myHero
    # event.add["database"] = database

    try:
        response = Command.cmd_functions[cmd](myHero, database=database, arg_dict=request.args)
        database.update()
        # pdb.set_trace()
        return response
    except KeyError as ex:
        print("Warning: invalid key {}".format(ex))
        print("Valid keys are: {}".format(list(Command.cmd_functions.keys())))
        # Look in the not yet refractored list of if statemens ...
        
    if cmd == "woodsman":
        myHero.archetype = "Woodsman"
        return "success", 200, {'Content-Type': 'text/plain'} #//
    if cmd == "priest":
        myHero.archetype = "Priest"
        return "success", 200, {'Content-Type': 'text/plain'} #//
    if cmd == "hunter":
        myHero.specialization = "Hunter"
        return "success", 200, {'Content-Type': 'text/plain'} #//
    if cmd == "trapper":
        myHero.specialization = "Trapper"
        return "success", 200, {'Content-Type': 'text/plain'} #//
    # END OF TEST CODE
    
    for item in myHero.inventory:
        if cmd == item.name:
            if item.wearable:            # EQUIP ITEMS
                equipped_items_to_remove = []
                for equipped_item in myHero.equipped_items:
                    if type(item) is Weapon:
                        if item.two_handed_weapon and (equipped_item.shield or equipped_item.one_handed_weapon):
                            equipped_items_to_remove.append(equipped_item)
                            myHero.inventory.append(equipped_item)
                        if item.one_handed_weapon and equipped_item.two_handed_weapon:
                            equipped_items_to_remove.append(equipped_item)
                            myHero.inventory.append(equipped_item)
                        if item.shield and equipped_item.two_handed_weapon:
                            equipped_items_to_remove.append(equipped_item)
                            myHero.inventory.append(equipped_item)
                    if type(equipped_item) is type(item):
                        equipped_items_to_remove.append(equipped_item)
                        myHero.inventory.append(equipped_item)
                myHero.equipped_items = [x for x in myHero.equipped_items if x not in equipped_items_to_remove] # deletes the items in equipped_items_to_remove from myHero.equipped_items
                myHero.equipped_items.append(item)
                myHero.inventory.remove(item)
                myHero.update_secondary_attributes()
                for path in myHero.quest_paths:
                    if path.active and path.quest.name == "Equipping/Unequipping" and path.stage == 1:
                        path.quest.advance_quest()
                return "success", 200, {'Content-Type': 'text/plain'} #//
            if item.consumable == True:                # CONSUME ITEMS
                myHero.consume_item(item.name)
                return "success", 200, {'Content-Type': 'text/plain'} #//

    # UNEQUIP ITEMS
    for item in myHero.equipped_items:
        if cmd == item.name:
            myHero.inventory.append(item)
            myHero.equipped_items.remove(item)
            myHero.update_secondary_attributes()
            for path in myHero.quest_paths:
                    if path.active and path.quest.name == "Equipping/Unequipping" and path.stage == 2:
                        path.quest.advance_quest()
            return "success", 200, {'Content-Type': 'text/plain'} #//

    # UPGRADE ABILITIES
    learnable_known_abilities = [ability for ability in myHero.abilities if ability.level < ability.max_level]
    for ability in learnable_known_abilities:
        if cmd == ability.name and  myHero.ability_points > 0:
            for i in range(0,len(myHero.abilities)):
                if myHero.abilities[i].name == ability.name:
                    myHero.abilities[i].level += 1
                    myHero.abilities[i].update_display()
                    myHero.ability_points -= 1
            myHero.update_secondary_attributes()
            database.update()
            return "success", 200, {'Content-Type': 'text/plain'} #//

    # LEARN NEW ABILITIES
    unknown_abilities = []
    for ability in database.get_all_abilities():
        if ability not in myHero.abilities:
            unknown_abilities.append(ability)
    for ability in unknown_abilities:
        if cmd == ability.name and myHero.ability_points > 0:
            myHero.abilities.append(ability)
            myHero.update_secondary_attributes()
            myHero.ability_points -= 1
            database.update()
            return "success", 200, {'Content-Type': 'text/plain'} #//

    #USE ABILITIES (ACTIVATED ONES)
    for ability in myHero.abilities:
        this_command = ability.name + "_use"
        if cmd == this_command:
            ability.cast(myHero)
            database.update()
            return "success", 200, {'Content-Type': 'text/plain'} #//


    # BUY FROM MARKETPLACE
    for item in database.get_all_marketplace_items():
        if cmd == item.buy_name and myHero.gold >= item.buy_price:
            for my_item in myHero.inventory:
                if my_item.name == item.name:
                    my_item.amount_owned += 1
                    break
            else:
                newItem = item
                newItem.update_owner(myHero)
                myHero.inventory.append(newItem)
                newItem.amount_owned = 1
            myHero.gold -= item.buy_price
            return "success", 200, {'Content-Type': 'text/plain'} #//

    return "failure", 200, {'Content-Type': 'text/plain'} #// these returns do nothing really, but you need them

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

    #Set Current Working Directory (CWD) to the home of this file.
    #This should make all other files import relative to this file fixing the Database doesn't exist problem.

    # os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #Marked for rename
    #I need a better name that "database.db"
    database = database.EZDB('sqlite:///static/database.db', debug=False)
    
    #I know there is a better way ... primary_attributes should be defined on initialization.
    #This allows myHero to be global variable in this module/file without magic. I think.
    myHero = Hero(gold=5000, age=7)
    #Because hero is easier for me to type.
    #Note: they are the same object!
    hero = myHero
    
    # initialization
    game = Game(hero)
    game.set_enemy(monster_generator(hero.age))

    #Not implemented ... should be moved to prebuilt_objects.py and implemented in 
    #database.py as get_default_quests()
    #Quest aren't actually implement yet but they will be soon!
    # Super temporary while testing quests
    # myHero.inventory.append(Quest_Item("Wolf Pelt", myHero, 50))
    # myHero.inventory.append(Quest_Item("Spider Leg", myHero, 50))
    # myHero.inventory.append(Quest_Item("Copper Coin", myHero, 50))
    # for item in myHero.inventory:
        # item.amount_owned = 5
    
    app.run(debug=True)



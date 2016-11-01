#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from battle import *
from bestiary import *
from database import *
from abilities import *
import sqlite3
import hashlib

# create the application object
app = Flask(__name__)

app.secret_key = 'starcraft'
		
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/<cmd>') # need to make sure this doesn't conflict with other routes
def command(cmd=None):
    # cmd (string type)is an item name, sent from the javascript code in html

    # it is the item that will get equipped/unequiped
    equippable_items = [item for item in myHero.inventory if item.equippable == True]
    for item in equippable_items: 
        if cmd == item.name:
            myHero.equipped_items.append(item)
            myHero.inventory.remove(item)
            return "success", 200, {'Content-Type': 'text/plain'} #//
        
    for item in myHero.equipped_items:
        if cmd == item.name:
            myHero.inventory.append(item)
            myHero.equipped_items.remove(item)
            render_template('home.html')
            return "success", 200, {'Content-Type': 'text/plain'} #//

    # ability
    learnable_known_abilities = [ability for ability in myHero.abilities if ability.level < ability.max_level]
    for ability in learnable_known_abilities:
        if cmd == ability.name:
            for i in range(0,len(myHero.abilities)):
                if myHero.abilities[i].name == ability.name:
                    myHero.abilities[i].level += 1
                    myHero.abilities[i].update_display()
            myHero.update_secondary_attributes()
            return "success", 200, {'Content-Type': 'text/plain'} #//
            
    unknown_abilities = []
    for ability in all_abilities:
        if not any(known_ability.name == ability.name for known_ability in myHero.abilities):
            unknown_abilities.append(ability)
    for ability in unknown_abilities:
        if cmd == ability.name:
            myHero.abilities.append(Ability(ability.name, myHero, ability.max_level, ability.description))
            myHero.update_secondary_attributes()
            return "success", 200, {'Content-Type': 'text/plain'} #//

    # store
    for item in all_store_items:
        if cmd == item.name and myHero.gold >= item.buy_price:
            newItem = item
            newItem.update_owner(myHero)
            myHero.inventory.append(newItem)
            myHero.gold -= item.buy_price
            return "success", 200, {'Content-Type': 'text/plain'} #//
        
    return "failure", 200, {'Content-Type': 'text/plain'} #// these returns do nothing really, but you need them
       
@app.route('/level_up', methods=['GET', 'POST'])
@login_required
def level_up():
    if request.method == 'POST':
        strength = convert_input(request.form["Strength"])
        resilience = convert_input(request.form["Resilience"])
        vitality = convert_input(request.form["Vitality"])
        fortitude = convert_input(request.form["Fortitude"])
        reflexes = convert_input(request.form["Reflexes"])
        agility = convert_input(request.form["Agility"])
        perception = convert_input(request.form["Perception"])
        wisdom = convert_input(request.form["Wisdom"])
        divinity = convert_input(request.form["Divinity"])
        charisma = convert_input(request.form["Charisma"])
        survivalism = convert_input(request.form["Survivalism"])
        fortuity = convert_input(request.form["Fortuity"])
        total_points_spent = sum([strength, resilience, vitality, fortitude, reflexes, agility, perception, wisdom, divinity, charisma, survivalism, fortuity])
        if total_points_spent <= myHero.attribute_points:            
            myHero.strength += strength
            myHero.resilience += resilience
            myHero.vitality += vitality
            myHero.fortitude += fortitude
            myHero.reflexes += reflexes
            myHero.agility += agility
            myHero.perception += perception
            myHero.wisdom += wisdom
            myHero.divinity += divinity
            myHero.charisma += charisma
            myHero.survivalism += survivalism
            myHero.fortuity += fortuity
            myHero.attribute_points -= total_points_spent
        else:
            error = "Spend less points."
        if myHero.attribute_points <= 0:
            update_character(session['id'],myHero)
            return redirect(url_for('home'))
    myHero.update_secondary_attributes()
    page_heading = "You have leveled up!"
    paragraph = "Choose how you would like to distribute your attribute points."
    primary_attributes = [("Strength", myHero.strength),
                          ("Resilience", myHero.resilience),
                          ("Vitality", myHero.vitality),
                          ("Fortitude", myHero.fortitude),
                          ("Reflexes", myHero.reflexes),
                          ("Agility", myHero.agility),
                          ("Perception", myHero.perception),
                          ("Wisdom", myHero.wisdom),
                          ("Divinity", myHero.divinity),
                          ("Charisma", myHero.charisma),
                          ("Survivalism", myHero.survivalism),
                          ("Fortuity", myHero.fortuity)]
    return render_template('home.html', page_title="Profile", page_heading=page_heading, paragraph=paragraph, myHero=myHero, primary_attributes=primary_attributes)

# use decorators to link the function to a url
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("LOG IN SUCCESSFUL")
            session['id'] = get_user_id(username)
            fetch_character_data()
            return redirect(url_for('home'))
    return render_template('login.html', error=error, login=True)

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
    return render_template('login.html', error=error, password_recovery=True)

# route for handling the account creation page logic
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = None    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        temp_id = get_user_id(username)
        if temp_id == -1:
            add_new_user(username, password)
            add_new_character("Unknown","None")
            user_id = get_user_id(username)
            update_character(user_id,myHero) # slightly redundant, fix laterrr
            return redirect(url_for('login'))
        else:
            error = "Usename already exists!"  
    return render_template('login.html', error=error, create_account=True)
	
@app.route('/logout')
@login_required
def logout():
    update_character(session['id'],myHero) ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    session.pop('logged_in', None)
    flash("Thank you for playing! Your have successfully logged out.")
    return redirect(url_for('login'))

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
    if request.method == 'POST' and myHero.character_name == "Unknown":
        myHero.character_name = request.form["character_name"]
        page_image = "old_man"
        paragraph = None
        conversation = [("Stranger: ", "Where do you come from, child?")]
        display = False
    elif request.method == 'POST' and fathers_job == None:
        fathers_job = request.form["character_class"]
        if fathers_job == "Brute":
            myHero.inventory.append(starting_items[0])
            myHero.inventory.append(starting_items[4])
            myHero.strength += 3
            myHero.resilience += 1
            myHero.vitality += 1
            myHero.fortitude += 1
        elif fathers_job == "Scholar":
            myHero.inventory.append(starting_items[3])
            myHero.wisdom += 6
            myHero.perception += 1
        elif fathers_job == "Hunter":
            myHero.inventory.append(starting_items[1])
            myHero.inventory.append(starting_items[4])
            myHero.agility += 3
            myHero.reflexes += 1
            myHero.survivalism += 2
        elif fathers_job == "Merchant":
            myHero.inventory.append(starting_items[3])
            myHero.gold += 75
            myHero.charisma += 5
            myHero.fortuity += 1
        elif fathers_job == "Priest":
            myHero.inventory.append(starting_items[3])
            myHero.inventory.append(starting_items[2])
            myHero.divinity += 5
            myHero.wisdom += 1
    if myHero.character_name != "Unknown" and fathers_job != None:
        myHero.character_class = fathers_job
        update_character(session['id'],myHero)
        return redirect(url_for('home'))
    else:
        return render_template('create_character.html', page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, conversation=conversation, display=display)  # render a template  

@app.route('/battle')
@login_required
def battle():
    required_endurance = 5 # Todo: 5 is just a dummy number for testing
    
    page_title = "Battle"
    page_heading = "Fighting"
    print("running function: battle2")
    
    page_links = [("Return to your ","home","profile"," page.")]
    if myHero.current_endurance < required_endurance:
        page_title = "Battle"
        page_heading = "Not enough endurance, wait a bit!"
        return render_template('home.html', page_title=page_title, myHero=myHero, page_heading=page_heading, page_links=page_links)
    
    myHero.current_health,game.enemy.current_health,conversation = battle_logic(myHero,game.enemy)    
    if myHero.current_health == 0:
        myHero.current_endurance -= required_endurance
        page_title = "Defeat!"
        page_heading = "You have died."
    else:
        myHero.current_endurance -= required_endurance
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
        myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        page_title = "Victory!"
        page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience!"
        page_links = [("Compete in the ","/arena","arena","."), ("Go back to the ","/barracks","barracks","."), ("Return to your ","/home","profile"," page.")]
        if myHero.current_exp == 0:
            page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience. You have leveled up! You should return to your profile page to advance in skill."
            page_links = [("Return to your ","/home","profile"," page and distribute your new attribute points.")]
     
    update_character(session['id'],myHero)
    return render_template('home.html', page_title=page_title, page_heading=page_heading, myHero=myHero, enemy=enemy, status_display=conversation, page_links=page_links)  # return a string

@app.route('/reset_character')
@login_required
def reset_character():
    myHero.character_name = "Unknown"
    myHero.character_class = "None" 
    myHero.age = 1
    myHero.attribute_points = 0
    myHero.current_xp = 0
    myHero.max_xp = 0
    myHero.attribute_points = 0
    myHero.strength = 1
    myHero.resilience = 1
    myHero.vitality = 1
    myHero.fortitude = 1
    myHero.reflexes = 1
    myHero.agility = 1
    myHero.perception = 1
    myHero.wisdom = 1
    myHero.divinity = 1
    myHero.charisma = 1
    myHero.survivalism = 1
    myHero.fortuity = 1
    myHero.abilities = []
    myHero.gold = 500
    myHero.update_secondary_attributes()
    return redirect(url_for('home'))  # return a string

@app.route('/admin',methods=['GET', 'POST'])
@login_required
def admin():
    page_title = "Admin"
    page_heading = "Use this page to set values"
    page_image = "town"
    if request.method == 'POST':
        myHero.strength = convert_input(request.form["Strength"])
        myHero.resilience = convert_input(request.form["Resilience"])
        myHero.vitality = convert_input(request.form["Vitality"])
        myHero.fortitude = convert_input(request.form["Fortitude"])
        myHero.reflexes = convert_input(request.form["Reflexes"])
        myHero.agility = convert_input(request.form["Agility"])
        myHero.perception = convert_input(request.form["Perception"])
        myHero.wisdom = convert_input(request.form["Wisdom"])
        myHero.divinity = convert_input(request.form["Divinity"])
        myHero.charisma = convert_input(request.form["Charisma"])
        myHero.survivalism = convert_input(request.form["Survivalism"])
        myHero.fortuity = convert_input(request.form["Fortuity"])
        myHero.age = convert_input(request.form["Age"])
        myHero.current_exp = convert_input(request.form["Current_exp"])
        myHero.max_exp = convert_input(request.form["Max_exp"])
        myHero.renown = convert_input(request.form["Renown"])
        myHero.virtue = convert_input(request.form["Virtue"])
        myHero.charisma = convert_input(request.form["Charisma"])
        myHero.devotion = convert_input(request.form["Devotion"])
        myHero.gold = convert_input(request.form["Gold"])
        myHero.basic_ability_points = convert_input(request.form["Basic_ability_points"])
        myHero.class_ability_points = convert_input(request.form["Class_ability_points"])
        myHero.specialization_ability_points = convert_input(request.form["Specialization_ability_points"])
        myHero.pantheonic_ability_points = convert_input(request.form["Pantheonic_ability_points"])
        myHero.attribute_points = convert_input(request.form["Attribute_points"])
        myHero.current_endurance = convert_input(request.form["Endurance"])
        myHero.update_secondary_attributes()
        update_character(session['id'],myHero)
        return redirect(url_for('home'))

    admin = [("Strength", myHero.strength),
                          ("Resilience", myHero.resilience),
                          ("Vitality", myHero.vitality),
                          ("Fortitude", myHero.fortitude),
                          ("Reflexes", myHero.reflexes),
                          ("Agility", myHero.agility),
                          ("Perception", myHero.perception),
                          ("Wisdom", myHero.wisdom),
                          ("Divinity", myHero.divinity),
                          ("Charisma", myHero.charisma),
                          ("Survivalism", myHero.survivalism),
                          ("Fortuity", myHero.fortuity),
                          ("Age", myHero.age),  
                          ("Current_exp", myHero.current_exp),
                          ("Max_exp", myHero.max_exp),
                          ("Renown", myHero.renown),
                          ("Virtue", myHero.virtue),
                          ("Charisma", myHero.charisma),
                          ("Devotion", myHero.devotion),
                          ("Gold", myHero.gold),
                          ("Basic_ability_points", myHero.basic_ability_points),
                          ("Class_ability_points", myHero.class_ability_points),
                          ("Specialization_ability_points", myHero.specialization_ability_points),
                          ("Pantheonic_ability_points", myHero.pantheonic_ability_points),
                          ("Attribute_points", myHero.attribute_points),
                          ("Endurance",myHero.current_endurance)]
    
    return render_template('home.html', page_title=page_title, page_heading=page_heading, page_image=page_image, myHero=myHero, admin=admin)  # return a string


### PROFILE/DISPLAY FUNCTIONS

@app.route('/home')
@login_required
def home():
    #fetch_character_data()
    myHero.update_secondary_attributes()
    update_time(myHero)
    # If it's a new character, send them to cerate_character url
    if myHero.character_name == "Unknown":
        return redirect(url_for('create_character'))
    # If they have leveled up, send them to level_up url
    elif myHero.attribute_points > 0:
        return redirect(url_for('level_up'))
    return render_template('home.html', page_title="Profile", myHero=myHero, home=True)  # return a string'

@app.route('/ability_tree')
@login_required
def ability_tree():
    paragraph = ""
    page_title = "Abilities"
    unknown_abilities = []
    learnable_abilities = []
    mastered_abilities = []
    for ability in all_abilities:
        if not any(known_ability.name == ability.name for known_ability in myHero.abilities):
            unknown_abilities.append(ability)
    for ability in myHero.abilities:
        if ability.level < ability.max_level:
            learnable_abilities.append(ability)
        else:
            mastered_abilities.append(ability)
    return render_template('home.html', myHero=myHero, ability_tree=True, unknown_abilities=unknown_abilities, learnable_abilities=learnable_abilities, mastered_abilities=mastered_abilities, page_title=page_title)  # return a string

@app.route('/quest_log')
@login_required
def quest_log():
    paragraph = ""
    page_title = "Quest Log"
    current_quests = myHero.current_quests
    completed_quests = myHero.completed_quests
    errands = myHero.errands
    if current_quests == []:
        current_quests = False
    if errands == []:
        errands = False
    if completed_quests == []:
        completed_quests = False
    return render_template('home.html', myHero=myHero, journal=True, quest_log=True, page_title=page_title, current_quests=current_quests, errands=errands, completed_quests=completed_quests)  # return a string

@app.route('/bestiary/<current_beast>')
@login_required
def bestiary(current_beast):
    if current_beast == "default":
        current_beast = None
    else:
        for monster in bestiary_data:
            if monster[0] == current_beast:
                current_beast = monster
                break
    paragraph = ""
    page_title = "Bestiary"
    return render_template('home.html', myHero=myHero, journal=True, bestiary=True, page_title=page_title, bestiary_data=bestiary_data, current_beast=current_beast)  # return a string

@app.route('/people_log')
@login_required
def people_log():
    paragraph = ""
    page_title = "People"
    page_heading = "People"
    return render_template('home.html', myHero=myHero, journal=True, page_title=page_title, page_heading=page_heading)  # return a string

@app.route('/map_log')
@login_required
def map_log():
    paragraph = ""
    page_title = "Map"
    page_heading = "Map"
    return render_template('home.html', myHero=myHero, journal=True, page_title=page_title, page_heading=page_heading)  # return a string

@app.route('/achievement_log')
@login_required
def achievement_log():
    paragraph = ""
    page_title = "Achievements"
    page_heading = "Achievements"
    return render_template('home.html', myHero=myHero, journal=True, page_title=page_title, page_heading=page_heading)  # return a string

@app.route('/under_construction')
@login_required
def under_construction():
    page_title = "Under Construction"
    page_heading = "This page is not complete yet."
    page_image = "under_construction"
    return render_template('home.html', page_title=page_title, page_heading=page_heading, page_image=page_image, myHero=myHero)  # return a string

### END OF PROFILE/DISPLAY FUNCTIONS



### STARTING TOWN FUNCTIONS

@app.route('/town')
@login_required
def town(page_title = "Town"):
    page_heading = "You are in the Starting Town."
    page_image = "town"
    paragraph = "The starting town. There are many places to visit within the town. Have a look!"
    town_links = [("/store/greeting", "Blacksmith", "Shops"),
                  ("/barracks", "Barracks"),
                  ("/under_construction", "Marketplace"),
                  ("/tavern", "Tavern", "Other"),
                  ("/old_mans_hut", "Old Man's Hut"),
                  ("/leave_town", "Village Gate", "Outskirts")]
    return render_template('home.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, town_links=town_links)  # return a string

@app.route('/barracks')
@login_required
def barracks():
    if myHero.current_health <= 0:
        page_heading = "Your hero is currently dead."
        page_image = "dead"
        page_links = ["","","",""]
    else:
        page_heading = "Welcome to the arena " + myHero.character_name +"!"
        page_image = "arena"
        page_links = [("Compete in the ", "/arena","arena", ".(temporary)"), ("Pay to ", "/spar", "spar", " against the trainer."), ("Battle another ", "/under_construction", "player",".")]
    return render_template('home.html', page_title="Barracks", page_heading=page_heading, page_image=page_image, myHero=myHero, game=game, page_links=page_links)  # return a string

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
    return render_template('home.html', page_title="Sparring Room", page_heading=page_heading, myHero=myHero, game=game)  # return a string

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
    page_heading = "Welcome to the arena " + myHero.character_name +"!"
    page_image = str(game.enemy.name)
    conversation = [("Name: ", str(game.enemy.name), "Enemy Details"),
                    ("Level: ", str(game.enemy.level), "Combat Details"),
                    ("Damage: ", str(str(game.enemy.min_damage) + " - " + str(game.enemy.max_damage))),
                    ("Attack Speed: ", str(game.enemy.attack_speed)),
                    ("Health: ", str(str(game.enemy.current_health) + " / " + str(game.enemy.max_health))),
                    ("Accuracy: ", str(str(game.enemy.accuracy) + "%"))]
    page_links = [("Challenge the enemy to a ","/battle","fight","."), ("Go back to the ","/barracks","barracks",".")]
    return render_template('home.html', page_title="War Room", page_heading=page_heading, page_image=page_image, myHero=myHero, game=game, page_links=page_links, status_display=conversation)  # return a string

@app.route('/store/<inventory>')
@login_required
def store(inventory):
    page_title = "Store"
    if inventory == "greeting":
        page_links = [("Take a look at the ", "/store/armoury", "armour", "."), ("Let's see what ", "/store/weaponry", "weapons", " are for sale.")]
        page_heading = "Good day sir! What can I get for you?"
        page_image = "store"
        return render_template('home.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links)  # return a string
    elif inventory == "armoury":
        page_heading = "Check out our new armour!"
        page_links = [("Let me see the ", "/store/weaponry", "weapons", " instead.")]
        items_for_sale = [("Medium Tunic", "5"), ("Strong Tunic", "10")]
    elif inventory == "weaponry":
        page_heading = "Careful! Our weapons are sharp."
        page_links = [("I think I'd rather look at your ", "/store/armoury", "armour", " selection.")]
        items_for_sale = [("Medium Axe", "5"), ("Strong Axe", "10")]
    page_image = "store"
    return render_template('home.html', myHero=myHero, items_for_sale=items_for_sale, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links)  # return a string

@app.route('/tavern', methods=['GET', 'POST'])
@login_required
def tavern():
    tavern=True
    page_title = "Tavern"
    page_heading = "You enter the Red Dragon Inn."
    page_image = "bartender"
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
    return render_template('home.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, tavern=tavern, bottom_page_links=page_links, dialogue_options=dialogue_options)  # return a string

@app.route('/old_mans_hut')
@login_required
def old_mans_hut():
    page_heading = "Old Man's Hut"
    page_image = "hut"
    paragraph = "Nice to see you again kid. What do you need?"
    return render_template('home.html', myHero=myHero, page_title="Old Man's Hut", page_heading=page_heading, page_image=page_image, paragraph=paragraph)  # return a string

@app.route('/leave_town')
@login_required
def leave_town():
    page_heading = "Village Gate"
    conversation = [("City Guard: ", "You are too young to be out on your own.")]
    page_links = [("Return to the ", "/town", "city", ".")]
    return render_template('home.html', myHero=myHero, page_heading=page_heading, conversation=conversation, page_links=page_links)  # return a string

### END OF STARTING TOWN FUNCTIONS





# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)



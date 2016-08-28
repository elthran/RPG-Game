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
import sqlite3
import hashlib



# create the application object
app = Flask(__name__)

app.secret_key = 'starcraft'
		
# login required decorator
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
    for item in myHero.inventory:
        if cmd == item.name:
            myHero.equipped_items.append(item)
            myHero.inventory.remove(item)
            render_template('home.html', page_title="Profile", myHero=myHero, home=True)
            return "success", 200, {'Content-Type': 'text/plain'} #//
        
    for item in myHero.equipped_items:
        if cmd == item.name:
            myHero.inventory.append(item)
            myHero.equipped_items.remove(item)
            render_template('home.html', page_title="Profile", myHero=myHero, home=True)
            return "success", 200, {'Content-Type': 'text/plain'} #//
        
    return "failure", 200, {'Content-Type': 'text/plain'} #// these returns do nothing really, but you need them

       
# use decorators to link the function to a url	
@app.route('/home')
@login_required
def home():
    myHero.update_secondary_attributes()
    # If it's a new character, send them to cerate_character url
    if myHero.character_name == "Unknown":
        return redirect(url_for('create_character'))
    # If they have leveled up, send them to level_up url
    elif myHero.attribute_points > 0:
        return redirect(url_for('level_up'))
    return render_template('home.html', page_title="Profile", myHero=myHero, home=True)  # return a string'

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
            yHero.inventory.append(starting_items[3])
            myHero.gold += 75
            myHero.charisma += 5
            myHero.fortuity += 1
        elif fathers_job == "Priest":
            myHero.inventory.append(starting_items[3])
            myHero.inventory.append(starting_items[2])
            myHero.divinity += 5
            myHero.wisdom += 1
    if myHero.character_name != "Unknown" and fathers_job != None:
        print(myHero.character_name + " " + fathers_job)
        update_character(session['id'],myHero)
        return redirect(url_for('home'))
    else:
        return render_template('create_character.html', page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, conversation=conversation, display=display)  # render a template  

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
        add_new_user(username, password)
        add_new_character("Unknown","None")
        user_id = get_user_id(username)
        update_character(user_id,myHero) # slightly redundant, fix laterrr
        return redirect(url_for('login'))
    return render_template('login.html', error=error, create_account=True)
	
	
@app.route('/logout')
@login_required
def logout():
    update_character(session['id'],myHero) ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    session.pop('logged_in', None)
    flash("Thank you for playing! Your have successfully logged out.")
    return redirect(url_for('login'))

@app.route('/war_room')
@login_required
def war_room():
    if myHero.current_health <= 0:
        page_heading = "Your hero is currently dead."
        page_image = "dead"
        page_links = ["","","",""]
    else:
        page_heading = "Welcome to the arena " + myHero.character_name +"!"
        page_image = "arena"
        page_links = [("Compete in the ","/arena","arena","."), ("Battle another ","/under_construction","player",".")]
    return render_template('home.html', page_title="War Room", page_heading=page_heading, page_image=page_image, myHero=myHero, game=game, page_links=page_links)  # return a string

@app.route('/arena')
@login_required
def arena():
    if not game.has_enemy or game.enemy.current_health <= 0:
        enemy = monster_generator(myHero.age)
        game.set_enemy(enemy)
    page_heading = "Welcome to the arena " + myHero.character_name +"!"
    page_image = str(game.enemy.name)
    conversation = [("Name: ", str(game.enemy.name), "Enemy Details"),
                    ("Level: ", str(game.enemy.level), "Combat Details"),
                    ("Damage: ", str(str(game.enemy.min_damage) + " - " + str(game.enemy.max_damage))),
                    ("Attack Speed: ", str(game.enemy.attack_speed)),
                    ("Health: ", str(str(game.enemy.current_health) + " / " + str(game.enemy.max_health))),
                    ("Accuracy: ", str(str(game.enemy.accuracy) + "%"))]
    page_links = [("Challenge the enemy to a ","/battle","fight","."), ("Go back to the ","/war_room","War Room",".")]
    return render_template('home.html', page_title="War Room", page_heading=page_heading, page_image=page_image, myHero=myHero, game=game, page_links=page_links, status_display=conversation)  # return a string

@app.route('/battle')
@login_required
def battle():
    page_title = "Battle"
    page_heading = "Fighting"
    print("running function: battle2")
    myHero.current_health,game.enemy.current_health,conversation = battle_logic(myHero,game.enemy)
    page_links = [("Return to your ","home","profile"," page.")]
    if myHero.current_health == 0:
        page_title = "Defeat!"
        page_heading = "You have died."
        page_links = [("Return to your ","home","profile"," page.")]
    else:
        game.has_enemy = False
        myHero.current_exp += game.enemy.experience_rewarded
        myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        page_title = "Victory!"
        page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience!"
        page_links = [("Compete in the ","/arena","arena","."), ("Go back to the ","/war_room","War Room","."), ("Return to your ","/home","profile"," page.")]
        if myHero.current_exp == 0:
            page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience. You have leveled up! You should return to your profile page to advance in skill."
            page_links = [("Return to your ","/home","profile"," page and distribute your new attribute points.")]
    return render_template('home.html', page_title=page_title, page_heading=page_heading, myHero=myHero, enemy=enemy, status_display=conversation, page_links=page_links)  # return a string

@app.route('/store_greeting')
@login_required
def store_greeting(page_title = "Store"):
    page_heading = "Good day sir! What can I get for you?"
    page_image = "store"
    page_links = [("Enter the ", "/store_armoury", "armoury", "."), ("Enter the ", "/store_weaponry", "weapons", ".")]
    return render_template('home.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links)  # return a string

@app.route('/store_armoury', methods=['GET', 'POST'])
@login_required
def store_armoury():
    page_title = "Store"
    page_heading = "Check out our new armour!"
    page_image = "store"
    page_links = [("Enter the ", "/store_weaponry", "weapons", ".")]
    items_for_sale = [("Medium Tunic", "25"), ("Strong Tunic", "35")]
    paragraph = ""
    items_being_bought = []
    items_bought = []
    cost = 0
    if request.method == 'POST':
        for item in range (0, int(request.form[items_for_sale[0][0]])):
            items_being_bought.append(items_for_sale[0][0])
            cost += int(items_for_sale[0][1])
        for item in range (0, int(request.form[items_for_sale[1][0]])):
            items_being_bought.append(items_for_sale[1][0])
            cost += int(items_for_sale[1][1])
        if cost <= myHero.gold and len(items_being_bought) > 0:
            paragraph += "You have bought "
            myHero.gold -= cost
            for item in items_being_bought:
                paragraph += item
                dummy_item = Weapon(item, myHero, 5, 5)
                items_bought.append(dummy_item)
            for item in items_bought:
                myHero.inventory.append(item)
            paragraph += " for " + str(cost) + " gold."
        elif len(items_being_bought) == 0:
            paragraph = ""
        else:
            items_being_bought = []
            cost = 0
            paragraph = "You can't afford it."
    return render_template('home.html', myHero=myHero, items_for_sale=items_for_sale, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links, paragraph=paragraph)  # return a string

@app.route('/store_weaponry', methods=['GET', 'POST'])
@login_required
def store_weaponry():
    page_title = "Store"
    page_heading = "Careful! Our weapons are sharp."
    page_image = "store"
    page_links = [("Enter the ", "/store_armoury", "armoury", ".")]
    items_for_sale = [("Medium Axe", "35"), ("Strong Axe", "55"), ("OK Axe", "50")]
    paragraph = ""
    items_being_bought = []
    items_bought = []
    cost = 0
    if request.method == 'POST':
        for item in range (0, int(request.form[items_for_sale[0][0]])):
            items_being_bought.append(items_for_sale[0][0])
            cost += int(items_for_sale[0][1])
        for item in range (0, int(request.form[items_for_sale[1][0]])):
            items_being_bought.append(items_for_sale[1][0])
            cost += int(items_for_sale[1][1])
        if cost <= myHero.gold and len(items_being_bought) > 0:
            paragraph += "You have bought "
            myHero.gold -= cost
            for item in items_being_bought:
                paragraph += item
                dummy_item = Weapon(item, myHero, 5, 5)
                items_bought.append(dummy_item)
            for item in items_bought:
                myHero.inventory.append(item)
            paragraph += " for " + str(cost) + " gold."
        elif len(items_being_bought) == 0:
            paragraph = ""
        else:
            items_being_bought = []
            cost = 0
            paragraph = "You can't afford it."
    return render_template('home.html', myHero=myHero, items_for_sale=items_for_sale, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links, paragraph=paragraph)  # return a string

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

@app.route('/under_construction')
@login_required
def under_construction():
    page_title = "Under Construction"
    page_heading = "This page is not complete yet."
    page_image = "under_construction"
    return render_template('home.html', page_title=page_title, page_heading=page_heading, page_image=page_image, myHero=myHero)  # return a string


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




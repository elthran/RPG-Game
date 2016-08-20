# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from battle import *
from bestiary import *
import sqlite3
import hashlib

# create the application object
app = Flask(__name__)

app.secret_key = 'starcraft'

#///////////////////////////////////////
#
#  TEMPORARY DATABASE FUNCTIONS
#
#///////////////////////////////////////

# Two functions used in login()
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

def validate(username, password):
    con = sqlite3.connect('static/user.db')
    completion = False

    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
    return completion	

def add_new_user(username, password):
    con = sqlite3.connect('static/user.db')

    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                new_user_id = len(rows)+1
                cur.execute('INSERT INTO USERS VALUES ("' + username + '","' + str(hashlib.md5(password.encode()).hexdigest()) + '",' +str(new_user_id) + ');' ) # needs to be changed 
                con.commit()
    con.close()

# username must exist
def get_user_id(username):
    con = sqlite3.connect('static/user.db')
    row = []
    with con:
                cur = con.cursor()
                cur.execute('SELECT USER_ID FROM USERS WHERE USERNAME = ' + '"' + username +'";' ) # needs to be changed 
                row = cur.fetchall()
    con.close()
    return row[0][0]
    

def add_new_character(charname, classname): ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    con = sqlite3.connect('static/user.db')

    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                new_user_id = len(rows)
                cur.execute('INSERT INTO CHARACTERS VALUES (' + str(new_user_id) + ',"' + charname + '","' + classname + '",5' + ');'); 
                con.commit()
    con.close()    

def update_character(user_id,charname , classname, strength): ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    con = sqlite3.connect('static/user.db')

    with con:
                cur = con.cursor()
                cur.execute('UPDATE CHARACTERS SET NAME="' + charname + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET CLASS="' + classname + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET STRENGTH=" + str(strength) + " WHERE USER_ID=" + str(user_id) + ';')
                con.commit()
    con.close()

def fetch_character_data():
    con = sqlite3.connect('static/user.db')
    with con:
                cur = con.cursor()
                cur.execute('SELECT * FROM characters WHERE user_id = ' + str(session['id']) + ';')
                rows = cur.fetchall()
                for row in rows:
                    id = row[0] 
                    if id==session['id']:
                        myHero.name = row[1]
                        myHero.starting_class = row[2]
                        myHero.strength = row[3] ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
                        break
    con.close() 
		
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
       
# use decorators to link the function to a url	
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    myHero.update_secondary_attributes()
    if request.method == 'POST':
        strength = convert_input(request.form["strength_upgrade"])
        endurance = convert_input(request.form["endurance_upgrade"])
        vitality = convert_input(request.form["vitality_upgrade"])
        agility = convert_input(request.form["agility_upgrade"])
        dexterity = convert_input(request.form["dexterity_upgrade"])
        devotion = convert_input(request.form["devotion_upgrade"])
        resistance = convert_input(request.form["resistance_upgrade"])
        wisdom = convert_input(request.form["wisdom_upgrade"])
        charm = convert_input(request.form["charm_upgrade"])
        instinct = convert_input(request.form["instinct_upgrade"])
        total_points_spent = sum([strength, endurance, vitality, agility, dexterity, devotion, resistance, wisdom, charm, instinct])
        if total_points_spent <= myHero.attribute_points:
            myHero.strength += strength
            myHero.endurance += endurance
            myHero.vitality += vitality
            myHero.agility += agility
            myHero.dexterity += dexterity
            myHero.devotion += devotion
            myHero.resistance += resistance
            myHero.wisdom += wisdom
            myHero.charm += charm
            myHero.instinct += instinct
            myHero.attribute_points -= total_points_spent
            myHero.update_secondary_attributes()
        else:
            error = "Spend less points."
    if myHero.name == "Unknown" or myHero.starting_class == "None":
        return redirect(url_for('create_character'))
    elif myHero.attribute_points > 0:
        return render_template('home.html', page_title="Profile", myHero=myHero, leveling_up=True)
    else:
        return render_template('home.html', page_title="Profile", myHero=myHero, home=True)  # return a string'

# use decorators to link the function to a url
@app.route('/create_character', methods=['GET', 'POST'])
@login_required
def create_character():
    display = True
    page_title = "Create Character"
    page_heading = "A New Beginning"
    page_image = "beached"
    paragraph = "You awake to great pain and confusion as you hear footsteps approaching in the sand. Unsure of where you are, you quickly look around for something to defend yourself. A firm and inquisitive voice pierces the air."
    conversation = [("Stranger: ", "Who are you and what are you doing here?")]
    if request.method == 'POST' and myHero.name == "Unknown":
        myHero.name = request.form["character_name"]
        page_image = "old_man"
        paragraph = None
        conversation = [("Stranger: ", "Where do you come from, child?")]
        display = False
    elif request.method == 'POST' and myHero.starting_class == "None":
        myHero.starting_class = request.form["starting_class"]
        
    if myHero.name != "Unknown" and myHero.starting_class != "None":
        print(myHero.name + " " + myHero.starting_class)
        add_new_character(myHero.name,myHero.starting_class) 
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
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_new_user(username, password)
        return redirect(url_for('login'))
    return render_template('login.html', error=error, create_account=True)
	
	
@app.route('/logout')
@login_required
def logout():
    user_id = session['id']
    update_character(user_id,myHero.name, myHero.starting_class,myHero.strength) ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    session.pop('logged_in', None)
    flash("Thank you for playing! Your have successfully logged out.")
    return redirect(url_for('login'))

@app.route('/arena')
@login_required
def arena():
    print("running function: arena")
    if not game.has_enemy or game.enemy.current_hp <= 0:
        enemy = monster_generator(myHero.level)
        game.set_enemy(enemy)
    page_heading = "Welcome to the arena " + myHero.name +"!"
    page_image = "arena"
    return render_template('home.html', page_title="Arena Results", page_heading=page_heading, page_image=page_image, myHero=myHero, arena=arena, game=game)  # return a string

@app.route('/battle')
@login_required
def battle():
    print("running function: battle")
    page_title = "Battle"
    page_heading = "Fighting"
    myHero.current_hp,game.enemy.current_hp,conversation = battle_logic(myHero,game.enemy)
    if myHero.current_hp == 0:
        page_title = "Defeat!"
        page_heading = "You have died."
    elif game.enemy.current_hp <= 0:
        game.has_enemy = False
        myHero.current_exp += game.enemy.experience_rewarded
        myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        page_title = "Victory!"
        page_heading = "You have defeated the " + str(game.enemy.name) + " and gained " + str(game.enemy.experience_rewarded) + " experience!"
    return render_template('home.html', page_title=page_title, page_heading=page_heading, myHero=myHero, enemy=enemy, conversation=conversation)  # return a string

@app.route('/store_greeting')
@login_required
def store_greeting():
    page_title = "Store"
    page_heading = "Good day sir! What can I get for you?"
    page_image = "store"
    page_links = [("store_armoury", "Armour"), ("store_weaponry", "Weapons")]
    return render_template('home.html', myHero=myHero, inside_store=True, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links)  # return a string

@app.route('/store_armoury')
@login_required
def store_armoury():
    page_title = "Store"
    page_heading = "We have the finest armoury in town! Take a look."
    page_image = "store"
    page_links = [("store_weaponry", "Weapons")]
    items_for_sale = ["ripped tunic", "torn tunic"]
    return render_template('home.html', myHero=myHero, inside_store=True, items_for_sale=items_for_sale, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links)  # return a string

@app.route('/store_weaponry')
@login_required
def store_weaponry():
    page_title = "Store"
    page_heading = "Careful! Our weapons are sharp."
    page_image = "store"
    page_links = [("store_armoury", "Armour")]
    items_for_sale = ["sword", "axe"]
    return render_template('home.html', myHero=myHero, inside_store=True, items_for_sale=items_for_sale, page_title=page_title, page_heading=page_heading, page_image=page_image, page_links=page_links)  # return a string

@app.route('/reset_character')
@login_required
def reset_character():
    myHero.name = "Unknown"
    myHero.level = 1
    myHero.update_secondary_attributes()
    return redirect(url_for('home'))  # return a string


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




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
                cur.execute('INSERT INTO CHARACTERS VALUES (' + str(new_user_id) + ',"' + charname + '","' + classname + '",1' + ');'); 
                con.commit()
    con.close()    

def update_character(user_id,strength): ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    con = sqlite3.connect('static/user.db')

    with con:
                cur = con.cursor()
                cur.execute("UPDATE CHARACTERS SET STRENGTH=" + str(strength) + " WHERE USER_ID=" + str(user_id) + ';')
                con.commit()
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

    if request.method == 'POST':
        strength = convert_input(request.form["strength_upgrade"])
        endurance = convert_input(request.form["endurance_upgrade"])
        vitality = convert_input(request.form["vitality_upgrade"])
        total_points_spent = sum([strength, endurance, vitality])
        if total_points_spent <= myHero.attribute_points:
            myHero.strength += strength
            myHero.endurance += endurance
            myHero.vitality += vitality
            myHero.attribute_points -= total_points_spent
            myHero.update_health()
            myHero.update_combat_stats()
        else:
            error = "Spend less points."
    if myHero.name == "Unknown" or myHero.starting_class == "None":
        return redirect(url_for('create_character'))
    elif myHero.attribute_points > 0:
        return render_template('home.html', page_title="Profile", myHero=myHero, leveling_up=leveling_up)
    else:
        return render_template('home.html', page_title="Profile", myHero=myHero, home=home)  # return a string'

# use decorators to link the function to a url
@app.route('/create_character', methods=['GET', 'POST'])
@login_required
def create_character():
    display = True
    page_title = "A New Beginning"
    choose_image = "beached"
    paragraph = "You awake to great pain and confusion as you hear footsteps approaching in the sand. Unsure of where you are, you quickly look around for something to defend yourself. A firm and inquisitive voice pierces the air."
    conversation = ["Stranger: Who are you and what are you doing here?"]
    if request.method == 'POST' and myHero.name == "Unknown":
        myHero.name = request.form["character_name"]
        page_title = None
        choose_image = "old_man"
        paragraph = None
        conversation = ["Stranger: Where do you come from, child?"]
        display = False
    elif request.method == 'POST' and myHero.starting_class == "None":
        myHero.starting_class = request.form["starting_class"]
        
    if myHero.name != "Unknown" and myHero.starting_class != "None":
        add_new_character(myHero.name,myHero.starting_class) 
        return redirect(url_for('home'))
    else:
        return render_template('create_character.html', paragraph=paragraph, conversation=conversation, page_title=page_title, choose_image=choose_image, display=display)  # render a template  

# use decorators to link the function to a url
@app.route('/level_up')
@login_required
def level_up():
    return render_template('level_up.html')  # render a template

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
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# route for handling the account creation page logic
@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_new_user(username, password)
        return redirect(url_for('login'))
    return render_template('createaccount.html', error=error)
	
	
@app.route('/logout')
@login_required
def logout():
    user_id = session['id']
    update_character(user_id,myHero.strength) ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    session.pop('logged_in', None)
    flash("LOG OUT SUCCESSFUL")
    return redirect(url_for('logout'))

@app.route('/arena')
@login_required
def arena():
    if not game.has_enemy:
        enemy = monster_generator(myHero.level)
        game.set_enemy(enemy)
    page_greeting= "Welcome to the arena " + myHero.name +"!"
    return render_template('home.html', page_title="Arena Results", page_greeting=page_greeting, myHero=myHero, arena=arena, game=game)  # return a string

@app.route('/level_up')
@login_required
def leveling_up():
    page_greeting = "You have leveled up! How would you like to spend your attribute points?"
    return render_template('home.html', page_title="Level Up", page_greeting=page_greeting, myHero=myHero, leveling_up=leveling_up)  # return a string


@app.route('/battle')
@login_required
def battle():
    myHero.hp,game.enemy.hp = battle_logic(myHero,game.enemy)
    if myHero.hp == 0:
        page_title = "Defeat!"
        page_greeting = "You have died."
    elif game.enemy.hp == 0:
        game.has_enemy = False
        myHero.current_exp += game.enemy.experience
        myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        page_title = "Victory!"
        page_greeting = "You have won the battle and gained " + str(game.enemy.experience) + " experience!"
    return render_template('home.html', page_title=page_title, page_greeting=page_greeting, myHero=myHero, enemy=enemy)  # return a string


@app.route('/defeat')
@login_required
def defeat():
    return render_template('home.html', page_title="Death", myHero=myHero)  # return a string

@app.route('/victory')
@login_required
def victory():
    return render_template('home.html', page_title="Victory!", myHero=myHero)  # return a string

@app.route('/store_greeting')
@login_required
def store_greeting():
    return render_template('store.html', myHero=myHero, is_store_greeting=True)  # return a string

@app.route('/store_armoury')
@login_required
def store_armoury():
    items_for_sale = ["ripped tunic", "torn tunic"]
    return render_template('store.html', myHero=myHero, is_store_armoury=True, items_for_sale=items_for_sale)  # return a string

@app.route('/store_weaponry')
@login_required
def store_weaponry():
    items_for_sale = ["sword", "axe"]
    return render_template('store.html', myHero=myHero, is_store_weaponry=True, items_for_sale=items_for_sale)  # return a string

@app.route('/createcharacter', methods=['GET', 'POST'])
@login_required
def createcharacter():
    if request.method == 'POST':
        myHero.choose_class()
        return redirect(url_for('home'))
    return render_template('create_character.html', myHero=myHero)  # return a string

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




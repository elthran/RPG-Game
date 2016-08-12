# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *
from battle import *
from bestiary import *

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

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    if myHero.name != "Unknown":
        created = "OK"
    else:
        created = None
    return render_template('home.html', created=created, myHero=myHero)  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/level_up')
def level_up():
    return render_template('level_up.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username_password = {'admin':'admin','jacob':'silly'}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in username_password:
            error = 'You have typed in your username incorrectly.'
        elif password != username_password[username]:
            error = 'You have typed in your password incorrectly.' 
        else:
            session['logged_in'] = True
            flash("LOG IN SUCCESSFUL")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("LOG OUT SUCCESSFUL")
    return redirect(url_for('logout'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        myHero.strength += int(request.form['strength_upgrade'])
        myHero.attribute_points -= int(request.form['strength_upgrade'])
        myHero.endurance += int(request.form['endurance_upgrade'])
        myHero.attribute_points -= int(request.form['endurance_upgrade'])
        myHero.vitality += int(request.form['vitality_upgrade'])
        myHero.attribute_points -= int(request.form['vitality_upgrade'])
        myHero.set_health(myHero.endurance, myHero.vitality, myHero.max_hp)
        myHero.set_damage(myHero.strength)
    return render_template('profile.html', page_title="Profile", myHero=myHero, profile=profile, sidebar=sidebar)  # return a string'

@app.route('/arena')
@login_required
def arena():
    page_greeting= "Welcome to the arena " + myHero.name +"!"
    return render_template('profile.html', page_title="Arena Results", page_greeting=page_greeting, myHero=myHero, arena=arena, sidebar=sidebar)  # return a string

@app.route('/level_up')
@login_required
def leveling_up():
    page_greeting = "You have leveled up! How would you like to spend your attribute points?"
    return render_template('profile.html', page_title="Level Up", page_greeting=page_greeting, myHero=myHero, leveling_up=leveling_up, sidebar=sidebar)  # return a string


@app.route('/battle')
@login_required
def battle():
    enemy = monster_generator(myHero.level)
    game.set_enemy(enemy)
    myHero.hp,game.enemy.hp = battle_logic(myHero,game.enemy)
    if myHero.hp == 0:
        return redirect(url_for('defeat', myHero=myHero))
    elif game.enemy.hp == 0:
        myHero.current_exp += game.enemy.level * 5
        myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        return redirect(url_for('victory', myHero=myHero))
    return render_template('battle.html', page_title="Battle", myHero=myHero, game=game, sidebar=sidebar)  # return a string

@app.route('/defeat')
@login_required
def defeat():
    return render_template('profile.html', page_title="Death", myHero=myHero, sidebar=sidebar)  # return a string

@app.route('/victory')
@login_required
def victory():
    return render_template('profile.html', page_title="Victory!", myHero=myHero, sidebar=sidebar)  # return a string

@app.route('/store_greeting')
@login_required
def store_greeting():
    return render_template('store.html', myHero=myHero, is_store_greeting=True, sidebar=sidebar)  # return a string

@app.route('/store_armoury')
@login_required
def store_armoury():
    items_for_sale = ["ripped tunic", "torn tunic"]
    return render_template('store.html', myHero=myHero, is_store_armoury=True, items_for_sale=items_for_sale, sidebar=sidebar)  # return a string

@app.route('/store_weaponry')
@login_required
def store_weaponry():
    items_for_sale = ["sword", "axe"]
    return render_template('store.html', myHero=myHero, is_store_weaponry=True, items_for_sale=items_for_sale, sidebar=sidebar)  # return a string

@app.route('/createcharacter', methods=['GET', 'POST'])
@login_required
def createcharacter():
    if request.method == 'POST':
        myHero.choose_class()
        return redirect(url_for('profile'))
    return render_template('createcharacter.html', myHero=myHero, sidebar=sidebar)  # return a string

sidebar = {"Arena": "/arena",
         "Profile": "/profile",
         "Store": "/store_greeting",
         "Logout": "/logout",
         "Battle": "/arena"}
sidebar = OrderedDict(sidebar)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




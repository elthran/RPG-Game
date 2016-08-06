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
    return render_template('home.html', created=created)  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

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

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', myHero=myHero)  # return a string'

@app.route('/arena')
@login_required
def arena():
    enemy = monster_generator(myHero.level)
    game.set_enemy(enemy)
    return render_template('arena.html', myHero=myHero, game=game)  # return a string

@app.route('/battle')
@login_required
def battle():
    myHero.hp,game.enemy.hp = battle_logic()
    if myHero.hp == 0:
        return redirect(url_for('defeat', myHero=myHero))
    elif game.enemy.hp == 0:
        myHero.wins += 1
        myHero.current_exp += game.enemy.level * 5
        myHero.level_up(myHero.attribute_points, myHero.current_exp, myHero.max_exp)
        return redirect(url_for('victory', myHero=myHero))
    return render_template('battle.html', myHero=myHero, game=game)  # return a string

@app.route('/defeat')
@login_required
def defeat():
    return render_template('defeat.html', myHero=myHero)  # return a string

@app.route('/victory')
@login_required
def victory():
    return render_template('victory.html', myHero=myHero)  # return a string

@app.route('/store_greeting')
@login_required
def store_greeting():
    return render_template('store.html', myHero=myHero, is_store_greeting=True)  # return a string

@app.route('/store_armoury')
@login_required
def store_armoury():
    items_for_sale = ["tunic", "hat"]
    return render_template('store.html', myHero=myHero, is_store_armoury=True, items_for_sale=items_for_sale)  # return a string

@app.route('/store_weaponry')
@login_required
def store_weaponry():
    items_for_sale = ["sword", "axe"]
    return render_template('store.html', myHero=myHero, is_store_weaponry=True, items_for_sale=items_for_sale)  # return a string


@app.route('/createcharacter', methods=['GET', 'POST'])
@login_required
def createcharacter():
    myHero.wins = 0
    myHero.set_health(myHero.max_hp)
    if request.method == 'POST':
        myHero.name = request.form['char_name']
        myHero.starting_class = request.form['spec']
        return redirect(url_for('profile'))
    return render_template('createcharacter.html', myHero=myHero)  # return a string

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




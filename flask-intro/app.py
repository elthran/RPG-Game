# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from game import *

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
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'You have typed in your username or password incorrctly.'
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
    return render_template('arena.html', myHero=myHero, enemy=enemy)  # return a string

@app.route('/battle')
@login_required
def battle():
    myHero.hp = 50
    enemy.hp = 7 + myHero.wins
    while myHero.hp > 0 and enemy.hp > 0:
        myHero.hp -= 1
        enemy.hp -= 5
        if myHero.hp < 0:
            myHero.hp = 0
        if enemy.hp < 0:
            enemy.hp = 0
    if myHero.hp == 0:
        return redirect(url_for('defeat', myHero=myHero))
    elif enemy.hp == 0:
        myHero.wins += 1
        return redirect(url_for('victory', myHero=myHero))
    return render_template('battle.html', myHero=myHero, enemy=enemy)  # return a string

@app.route('/defeat')
@login_required
def defeat():
    return render_template('defeat.html', myHero=myHero)  # return a string

@app.route('/victory')
@login_required
def victory():
    return render_template('victory.html', myHero=myHero)  # return a string


@app.route('/createcharacter', methods=['GET', 'POST'])
@login_required
def createcharacter():
    if request.method == 'POST':
        myHero.name = request.form['char_name']
        myHero.spec = request.form['spec']
        return redirect(url_for('profile'))
    return render_template('createcharacter.html')  # return a string

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




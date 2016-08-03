# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

class Hero(object):
    def __init__(self, name, level, strength, agility, wisdom, vitality, hp, maxhp, wins, spec):
        self.name = name
        self.level = level
        self.strength = strength
        self.agility = agility
        self.wisdom = wisdom
        self.vitality = vitality
        self.hp = hp
        self.maxhp = maxhp
        self.wins = wins
        self.spec = spec

    def __repr__(self):
        return "Name: %s \n Class: Brute \n Level: %s \n Strength: %s \n Agility: %s \n Wisdom: %s \n Vitality: %s \n HP: %s/%s \n" % (self.name, self.level, self.strength, self.agility, self.wisdom, self.vitality, self.hp, self.maxhp) 
myHero = Hero("Unknown", 1, 3, 4, 2, 3, 50, 50, 1, "")
enemy = Hero("Goblin", 1, 2, 2, 2, 2, 7, 7, 0, "")

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
    myHero.hp -= 20
    if myHero.hp <= 0:
        dead = " "
    else:
        dead = None
        myHero.wins += 1
    return render_template('battle.html', myHero=myHero, enemy=enemy, dead=dead)  # return a string

@app.route('/battle_results')
@login_required
def battle_results():
    return render_template('battle_results.html', myHero=myHero, enemy=enemy, dead=dead)  # return a string

@app.route('/createcharacter', methods=['GET', 'POST'])
@login_required
def createcharacter():
    if request.method == 'POST':
        myHero.name = request.form['char_name']
        myHero.spec = request.form['spec']
        return redirect(url_for('profile'))
    return render_template('createcharacter.html', myHero=myHero)  # return a string

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)




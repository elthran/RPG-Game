#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from app import *
import sqlite3
import hashlib


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
                cur.execute('INSERT INTO CHARACTERS (USER_ID,NAME,CLASS) VALUES  (' + str(new_user_id) + ',"' + charname + '","' + classname + '"' + ');'); 
                con.commit()
    con.close()    


def update_character(user_id, hero): ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    con = sqlite3.connect('static/user.db')

    with con:
                cur = con.cursor()
                cur.execute('UPDATE CHARACTERS SET NAME="' + hero.name + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET CLASS="' + hero.starting_class + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET STRENGTH=" + str(hero.strength) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET CURRENT_EXP=" + str(hero.current_exp) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET MAX_EXP=" + str(hero.max_exp) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET LEVEL=" + str(hero.level) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET ATTRIBUTE_POINTS=" + str(hero.attribute_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET ENDURANCE=" + str(hero.endurance) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET VITALITY=" + str(hero.vitality) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET AGILITY=" + str(hero.agility) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET DEXTERITY=" + str(hero.dexterity) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET DEVOTION=" + str(hero.devotion) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET RESISTANCE=" + str(hero.resistance) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET WISDOM=" + str(hero.wisdom) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET CHARM=" + str(hero.charm) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET INSTINCT=" + str(hero.instinct) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET GOLD=" + str(hero.gold) + " WHERE USER_ID=" + str(user_id) + ';')
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
                        myHero.strength = row[3]
                        myHero.current_exp = row[4]
                        myHero.max_exp = row[5]
                        myHero.level = row[6]
                        myHero.attribute_points = row[7]
                        myHero.endurance = row[8]
                        myHero.vitality = row[9]
                        myHero.agility = row[10]
                        myHero.dexterity = row[11]
                        myHero.resistance = row[12]
                        myHero.wisdom = row[13]
                        myHero.charm = row[14]
                        myHero.instinct = row[15]
                        #myHero.gold = row[16]
                        ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
                        break
    con.close() 

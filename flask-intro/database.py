#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from app import *
import sqlite3
import hashlib
import datetime   

# Every second_per_endurance seconds, endurance will recover by 1
second_per_endurance = 10

# Two functions used in login()
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

def update_time(hero):
    con = sqlite3.connect('static/user.db')
    now = datetime.datetime.now()
    with con:
                cur = con.cursor()
                cur.execute('SELECT ENDURANCE FROM characters WHERE user_id = ' + str(session['id']) + ';')
                rows1 = cur.fetchall()
                hero.endurance = rows1[0][0]
                cur.execute('SELECT PREVIOUS_TIME FROM characters WHERE user_id = ' + str(session['id']) + ';')
                rows2 = cur.fetchall()
                s = str(rows2[0][0].split('.')[0])
                time_dif = now - datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
                print("difference in previously recorded time and the current time in seconds: " + str(time_dif.total_seconds()))
                endurance_increment = int(time_dif.total_seconds()/second_per_endurance)
                print("endurance should increase by this amount:" + str(endurance_increment))
                if endurance_increment >= 1 and hero.endurance < hero.max_endurance:
                    cur.execute('UPDATE CHARACTERS SET PREVIOUS_TIME="' + str(now) + '" WHERE USER_ID=' + str(session['id']) + ';')
                    if hero.endurance + endurance_increment < hero.max_endurance:
                        hero.endurance += endurance_increment
                        cur.execute('UPDATE CHARACTERS SET ENDURANCE=' + str(hero.endurance) + ' WHERE USER_ID = ' + str(session['id']) + ';')     
                    else:
                        hero.endurance = hero.max_endurance
                        cur.execute('UPDATE CHARACTERS SET ENDURANCE=' + str(hero.max_endurance) + ' WHERE USER_ID = ' + str(session['id']) + ';')
                con.commit()
    con.close()

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
    now = datetime.datetime.now()
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                new_user_id = len(rows)
                cur.execute('INSERT INTO CHARACTERS (USER_ID,CHARACTER_NAME,CHARACTER_CLASS) VALUES  (' + str(new_user_id) + ',"' + charname + '","' + classname + '"' + ');');
                cur.execute('UPDATE CHARACTERS SET PREVIOUS_TIME="' + str(now) + '" WHERE USER_ID=' + str(new_user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET ENDURANCE=" + str(myHero.endurance) + " WHERE USER_ID=" + str(new_user_id) + ';')
                con.commit()
    con.close()    


def update_character(user_id, hero): ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
    con = sqlite3.connect('static/user.db')

    with con:
                cur = con.cursor()
                cur.execute('UPDATE CHARACTERS SET CHARACTER_NAME="' + hero.character_name + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET AGE=" + str(hero.age) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET CHARACTER_CLASS="' + hero.character_class + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET SPECIALIZATION="' + str(hero.specialization) + '" WHERE USER_ID='+ str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET HOUSE="' + str(hero.house) + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET CURRENT_EXP=" + str(hero.current_exp) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET MAX_EXP=" + str(hero.max_exp) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET RENOWN=" + str(hero.renown) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET VIRTUE=" + str(hero.virtue) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET DEVOTION=" + str(hero.devotion) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET GOLD=" + str(hero.gold) + " WHERE USER_ID=" + str(user_id) + ';')

                cur.execute("UPDATE CHARACTERS SET BASIC_ABILITY_POINTS=" + str(hero.basic_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET CLASS_ABILITY_POINTS=" + str(hero.class_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET SPECIALIZATION_ABILITY_POINTS=" + str(hero.specialization_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET PANTHEONIC_ABILITY_POINTS=" + str(hero.pantheonic_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')
                
                cur.execute("UPDATE CHARACTERS SET ATTRIBUTE_POINTS=" + str(hero.attribute_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET STRENGTH=" + str(hero.strength) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET RESILIENCE=" + str(hero.resilience) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET VITALITY=" + str(hero.vitality) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET FORTITUDE=" + str(hero.fortitude) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET REFLEXES=" + str(hero.reflexes) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET AGILITY=" + str(hero.agility) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET PERCEPTION=" + str(hero.perception) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET WISDOM=" + str(hero.wisdom) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET DIVINITY=" + str(hero.divinity) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET CHARISMA=" + str(hero.charisma) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET SURVIVALISM=" + str(hero.survivalism) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET FORTUITY=" + str(hero.fortuity) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET ENDURANCE=" + str(hero.endurance) + " WHERE USER_ID=" + str(user_id) + ';')

                #cur.execute("UPDATE CHARACTERS SET EQUIPPED_ITEMS=" + str(hero.equipped_items) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET INVENTORY=" + str(hero.inventory) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET ABILITIES=" + str(hero.abilities) + " WHERE USER_ID=" + str(user_id) + ';')
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
                        myHero.character_name = row[1]
                        myHero.age = row[2]
                        myHero.character_class = row[3]
                        myHero.specialization = row[4]
                        myHero.house = row[5]
                        myHero.current_exp = row[6]
                        myHero.max_exp = row[7]
                        myHero.renown = row[8]
                        myHero.virtue = row[9]
                        myHero.devotion = row[10]
                        myHero.gold = row[11]

                        myHero.basic_ability_points = row[12]
                        myHero.class_ability_points = row[13]
                        myHero.specialization_ability_points = row[14]
                        myHero.pantheonic_ability_points = row[15]
                        
                        myHero.attribute_points = row[16]
                        myHero.strength = row[17]
                        myHero.resilience = row[18]
                        myHero.vitality = row[19]
                        myHero.fortitude = row[20]
                        myHero.reflexes = row[21]
                        myHero.agility = row[22]
                        myHero.perception = row[23]
                        myHero.wisdom = row[24]
                        myHero.divinity = row[25]
                        myHero.charisma = row[26]
                        myHero.survivalism = row[27]
                        myHero.fortuity = row[28]
                        
                        #myHero.equipped_items = row[29]
                        #myHero.inventory = row[30]
                        #myHero.abilities = row[31]
                        ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
                        break
    con.close() 

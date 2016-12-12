#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

from app import * #Commenting this out will probably break everything ...
import sqlite3
import hashlib
import datetime
import os

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
                hero.current_endurance = rows1[0][0]
                cur.execute('SELECT PREVIOUS_TIME FROM characters WHERE user_id = ' + str(session['id']) + ';')
                rows2 = cur.fetchall()
                s = str(rows2[0][0].split('.')[0])
                time_dif = now - datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
                print("difference in previously recorded time and the current time in seconds: " + str(time_dif.total_seconds()))
                endurance_increment = int(time_dif.total_seconds()/second_per_endurance)
                print("endurance should increase by this amount:" + str(endurance_increment))
                if endurance_increment >= 1 and hero.current_endurance < hero.max_endurance:
                    cur.execute('UPDATE CHARACTERS SET PREVIOUS_TIME="' + str(now) + '" WHERE USER_ID=' + str(session['id']) + ';')
                    if hero.current_endurance + endurance_increment < hero.max_endurance:
                        hero.current_endurance += endurance_increment
                        cur.execute('UPDATE CHARACTERS SET ENDURANCE=' + str(hero.current_endurance) + ' WHERE USER_ID = ' + str(session['id']) + ';')     
                    else:
                        hero.current_endurance = hero.max_endurance
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
    if (len(row) == 0):
        return -1
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
                #cur.execute("UPDATE CHARACTERS SET ENDURANCE=" + str(myHero.current_endurance) + " WHERE USER_ID=" + str(new_user_id) + ';')
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
                
                cur.execute("UPDATE CHARACTERS SET ENDURANCE=" + str(hero.current_endurance) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET HEALTH=" + str(hero.current_health) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET SANCTITY=" + str(hero.current_sanctity) + " WHERE USER_ID=" + str(user_id) + ';')

                #cur.execute("UPDATE CHARACTERS SET EQUIPPED_ITEMS=" + str(hero.equipped_items) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET INVENTORY=" + str(hero.inventory) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET ABILITIES=" + str(hero.abilities) + " WHERE USER_ID=" + str(user_id) + ';')

                #3 types of QUESTS
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

                        #myHero.current_endurance = 
                        #myHero.current_health =
                        #myHero.current_sanctity =
                        
                        #myHero.equipped_items = row[29]
                        #myHero.inventory = row[30]
                        #myHero.abilities = row[31]

                        #3 types of quests
                        ######### MODIFY HERE TO ADD MORE THINGS TO STORE INTO DATABASE #########
                        break
    con.close() 

### Marlen --- testing ###
"""I am going to try and make an easy version of the current database. There will be all of the old code
but to add stuff will be simpler (I hope). I am just going to flesh out the concept. It won't work for a while.
"""
 

class EasyDatabase():
    """A more human usuable database.
    
    Implement by:
    game_database = EasyDatabase('static/user2.db') #The databases name.
    
    It might be a good idea to have separate user, location and item databases .... just in case one breaks?
    
    How to use:
        In the various places that originally used from database import *, now use from database import EasyDatabase as EzDB or something.
    Then create a database in the main app. When the user provides input call the relavent method on the games database object.
    
    """
    def __init__(self, name):
        """Set up a basic database for the game.
        
        This should include creating all of the basic tables and (possibly) populating this database with any data the game needs
        to run.
        """
        self.name = name
        self.build_basic_tables()
    
    def build_basic_tables(self):
        """Build the tables needed by the game.
        
        This should be upgraded to make it more human readable and editable .... maybe an external xml/spreadsheet/excel file?
        
        NOTE: User_ID field removed and replaced 'username' as a primary key ... I think it is a good idea?
        """
        basic_tables = (
            """CREATE TABLE USERS(
            USERNAME TEXT PRIMARY KEY NOT NULL,
            PASSWORD TEXT NOT NULL)""",
            
            """CREATE TABLE characters(
            User_ID integer primary key,
            character_name text,
            character_class number,
            age number,
            specialization text,
            house text,
            current_exp number,
            max_exp number,
            renown number,
            virtue number,
            devotion number,
            gold number,
            basic_ability_points number,
            class_ability_points number,
            specialization_ability_points number,
            pantheonic_ability_points number,
            attribute_points number,
            strength number,
            resilience number,
            vitality number,
            fortitude number,
            reflexes number,
            agility number,
            perception number,
            wisdom number,
            divinity number,
            charisma number,
            survivalism number,
            fortuity number,
            equipped_items number[],
            inventory number[],
            abilities number[],
            previous_login_time datetime current_timestamp,
            current_time datetime current_timestamp,
            previous_time datetime current_timestamp,
            endurance number)""",) #Dam ugly .. I think it might look nice in a spreadsheet file ... :)
            
        #Deal with use case where table already exists ... not very exacting (by which I mean it may fail randomly) ...
        #This failure has been explicitly silenced ...
        for table in basic_tables:
            try:
                self._write(table, build_tables=True)
            except sqlite3.OperationalError as e:
                print(e.args)
        
        
    def _write(self, *args, **kwargs):
        """Open connection and excute SQL statement then commit and close.
        
        This defaults to excecuting if only an argument is passed ... it is very insecure.
        NOTE: *args should be a list of tuples ... or maybe it already is? I shall test.
        
        This function when properly implemented should really be one of the few places actual SQL gets used ...
        All the INSERTS and SHIT should be in here. 
        """
        
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        
        def insert_user():
            print(len(args))
            c.execute("INSERT INTO USERS VALUES (?,?)", args)
            
        def build_tables():
            c.execute(args[0])
            
        def insert_character():
            c.execute("INSERT INTO CHARACTERS(user_id, character_name, character_class, current_time) VALUES (?,?,?,?)", args)
        
        def update_character():
            """This sql statement should be built using string formating but should still be secure using ?? for data values ..?
            
            UPDATE table_name
            SET column1 = value1, column2 = value2...., columnN = valueN
            WHERE [condition];
            """
            c.execute("""Update CHARACTERS set 
            {}=? WHERE ROWID=?
            """.format('username'), ('Marlen', 1))
            
        
        options = {'insert_user': insert_user,
            'build_tables': build_tables,
            'insert_character': insert_character,
            'update_character': update_character,
        }
        
        for key in kwargs:
            if kwargs[key]:
                options[key]()
        
        conn.commit()
        conn.close()
        
    def _read(self, *args, **kwargs):
        """Execute a prebaked SQL statement that returns pythonic data types.
        
        This is an internal database function only.  Other modules should call things like 'validate' or 'update_character'
        Those functions should call this.
        
        ##All of the SQL will be inside the read function!! 
        
        Ok so this is my latest idea.
        kwargs should be a dictionary of various types of basic database functions.
        
        Usage:
        db = EasyDatabase('static/Users2.db') #Make a database!
        db.validate(username, password) #Use an external function.
        -->Inside validate:
        password = self._read(username, read_password=True) #Execute SQL 'read a password' statement and return the password.
        
        NOTE: The kwargs variable is a mini language for the game that allows the user to execute specific SQL requests that
        have been preconstructed.
        NOTE2: no database commit happens in this funciton.
        """
        data = {}
        conn = sqlite3.connect(self.name)
        
        #I think this will come in realy hand at some point but I don't know how to use it yet.
        # conn.row_factory = sqlite3.Row #Some kind of fancy use of sqlite3 class variables that makes fetchall return a dictionary.
        # data = c.fetchall() #This combined with the row_factory is a dictionary object apparently .. which will come in handy someday.
        
        c = conn.cursor()
              
        def read_password():
            c.execute("SELECT password FROM USERS WHERE username=?", args)
            try:
                return c.fetchone()[0]
            except TypeError:
                return "no_match_found"
        
        def read_rowid():
            c.execute("SELECT ROWID FROM USERS WHERE username=?", args)
            return c.fetchone()[0]
            
        def some_other_usefull_function():
            #Do another SQL statement! and return the result in python please!
            pass
        
        #Yes this is kind of slow but the whole exec/compile is a whole nother problem.
        options = {'read_password' : read_password,
                'read_rowid' : read_rowid,
                'some_other_usefull_function': some_other_usefull_function
                }
        
        #Executes functions listed above (and arbitrary SQL so get rid of that yes?)
        #And like really really don't use exec or compile or any of those ok?.
        for key in kwargs:
            if kwargs[key]:
                data = options[key]()
        conn.close()
        return data
        
            
    def update_character(self, user_id, hero):
        """Save all of the new data a character has generated.
        
        This should check for changes and only save new data (if that is quicker).
        Basically the update_character function with less duplications.
        
        Ok ....
        atributes is an ordered list
        hero should have a ordered list of attributes
        rowid should extracted from character table using username?
        Basically update all colums in a give row ...
        """
        attributes = 'username','Me', 1
        
        self._write(attributes, update_character=True)
        pass
        
    def create_user(self, username, password):
        """Add a new user to the database.
        
        This should auto-validate as username is the primary key. 
        I can't decide if this should return False on failure or raise an error .. I went with raise error.
        I will build a custom exception at some point too ...
        """
        hashed_password = str(hashlib.md5(password.encode()).hexdigest())
        try:
            self._write(username, password, insert_user=True)
        except sqlite3.IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: USERS.USERNAME':
                raise Exception("Username '{}' already exists.".format(username)) #raise error if already in use.
    
    def create_character(self, user_id, character, classname):
        """Add a new character to a users account.
        
        ??Only one character at a time? or multiple characters?
        I will build for one only ...
        
        NOTE: Updates current_time
        """
        try:
            now = EasyDatabase.now()
            self._write(user_id, character, classname, now, insert_character=True)
        except sqlite3.IntegrityError as e:
            raise Exception("User '{}' already has a character.".format(username))
    
    def now():
        return str(datetime.datetime.now())
    
    def _wipe_database(self):
        os.remove(self.name)
        
    def validate(self, username, password):
        """Check if username and password match return True if they do.
        
        Passwords are stored in hashed form so ...
        hash the test password and compare with the retrieved one.
        """
        
        return  self._read(username, read_password=True) == hashlib.md5(password.encode()).hexdigest()
    
    def get_user_id(self, username):
        """Return the ID of a given user.
        
        This corresponds to the ROWID from SQL.
        The user must exist ... but since this should only be called after the user has logged in it should be redundant?
        """
        return self._read(username, read_rowid=True)
        
        

### testing
if __name__ == "__main__":
    db = EasyDatabase('static/Users2.db')
    # try:
        # db.create_user('Marlen', 'Brunner') #I should be able to add a bunch of users from a text file.
        # user_id = db.get_user_id("Marlen")
        # db.create_character(user_id, "Haldon", "Wizard")
    # except Exception as e:
        # print(e.args[0])
    
    # username = 'Marlen'
    # password = "Brunner"
    # db._read(username, read_password=True)
    # print("password valid?", db.validate(username, password))
    
    # print(db.get_user_id(username))
    # db.create_user(username, password)
    
    # db.update_character(1, "Haldon")
    
    ##Wipe the database.
    # db._wipe_database()
   
    db.name = 'static/User.db'
    username = 'marlen'
    password = "brunner"
    print(db._read(username, read_password=True))
    print("password valid?", db.validate(username, password))
    
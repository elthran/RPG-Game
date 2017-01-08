#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

# from app import * #Commenting this out will probably break everything ...
import sqlite3
import hashlib
import datetime
import os
from game import Hero
import ast

# Every second_per_endurance seconds, endurance will recover by 1
second_per_endurance = 10

# Two functions used in login()
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

def update_time(hero, session):
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
                cur.execute('UPDATE CHARACTERS SET CHARACTER_NAME="' + hero.name + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET AGE=" + str(hero.age) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET CHARACTER_CLASS="' + hero.archetype + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET SPECIALIZATION="' + str(hero.specialization) + '" WHERE USER_ID='+ str(user_id) + ';')
                cur.execute('UPDATE CHARACTERS SET HOUSE="' + str(hero.house) + '" WHERE USER_ID=' + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET CURRENT_EXP=" + str(hero.current_exp) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET MAX_EXP=" + str(hero.max_exp) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET RENOWN=" + str(hero.renown) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET VIRTUE=" + str(hero.virtue) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET DEVOTION=" + str(hero.devotion) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET GOLD=" + str(hero.gold) + " WHERE USER_ID=" + str(user_id) + ';')

                cur.execute("UPDATE CHARACTERS SET BASIC_ABILITY_POINTS=" + str(hero.basic_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET SPECIALIZATION_ABILITY_POINTS=" + str(hero.specialization_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')
                cur.execute("UPDATE CHARACTERS SET PANTHEONIC_ABILITY_POINTS=" + str(hero.pantheonic_ability_points) + " WHERE USER_ID=" + str(user_id) + ';')

                cur.execute("UPDATE CHARACTERS SET ATTRIBUTE_POINTS=" + str(hero.attribute_points) + " WHERE USER_ID=" + str(user_id) + ';')

                cur.execute("UPDATE CHARACTERS SET ENDURANCE=" + str(hero.current_endurance) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET HEALTH=" + str(hero.current_health) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET SANCTITY=" + str(hero.current_sanctity) + " WHERE USER_ID=" + str(user_id) + ';')

                #cur.execute("UPDATE CHARACTERS SET EQUIPPED_ITEMS=" + str(hero.equipped_items) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET INVENTORY=" + str(hero.inventory) + " WHERE USER_ID=" + str(user_id) + ';')
                #cur.execute("UPDATE CHARACTERS SET ABILITIES=" + str(hero.abilities) + " WHERE USER_ID=" + str(user_id) + ';')

                #3 types of QUESTS
                con.commit()
    con.close()

def fetch_character_data(hero, session):
    con = sqlite3.connect('static/user.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM characters WHERE user_id = ' + str(session['id']) + ';')
        rows = cur.fetchall()
        for row in rows:
            id = row[0]
            if id==session['id']:
                hero.character_name = row[1]
                hero.age = row[2]
                hero.character_class = row[3]
                hero.specialization = row[4]
                hero.house = row[5]
                hero.current_exp = row[6]
                hero.max_exp = row[7]
                hero.renown = row[8]
                hero.virtue = row[9]
                hero.devotion = row[10]
                hero.gold = row[11]

                hero.basic_ability_points = row[12]
                hero.class_ability_points = row[13]
                hero.specialization_ability_points = row[14]
                hero.pantheonic_ability_points = row[15]

                hero.attribute_points = row[16]

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
    return hero

### Marlen --- testing ###
"""I am going to try and make an easy version of the current database. There will be all of the old code
but to add stuff will be simpler (I hope). I am just going to flesh out the concept. It won't work for a while.

??Use "reflection" to port old database to new one. It's really cool I promise :).
"""


class EasyDatabase():
    """A more human usuable database.

    Basic principles:
        Hide SQL calls inside internal methods such a _write and _read.
        External methods should take simple input such as username and password.
        All connections to database should occur inside _read and _write.    
    
    Implement by:
    game_database = EasyDatabase('static/user2.db') #The databases name.

    It might be a good idea to have separate user, location and item databases .... just in case one breaks?

    How to use:
        Before: from database import *
        Now: from database import EasyDatabase
    
    eg.
    UserDatabase = EasyDatabase('static/User.db')
    In game usage:
        UserDatabase.validate(username, password)
        
    Note: EasyDatabase cannot store objects if an attribute is string "None". Boolean None is just fine :).
    Please use something like "Unknown" instead
    eg.
    
    class Hero():
        def __init__(self, money):
            specialization = "None" #Will NOT work
            specialization = None #Will work
            specialization = "Uknown" #Will work
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
        See https://www.draw.io/#LJacob%27s%20game for the table concepts (well it isn't quite using this yet but it will be).

        NOTE: I am using the ROWID as the primary key for both tables. It is invisible.
        """
        basic_tables = [
            """CREATE TABLE users(
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            email TEXT)"""]

        #Dam ugly .. I think it might look nice in a spreadsheet file ... :)

        char_table = self._build_char_table(Hero())
        basic_tables.append(char_table)

        #Deal with use case where table already exists ... not very exacting (by which I mean it may fail randomly) ...
        #This failure has been explicitly silenced ...
        for table in basic_tables:
            try:
                self._write(table, build_tables=True)
            except sqlite3.OperationalError as e:
                if 'already exists' in e.args[0]:
                    pass #Do nothing if the table exists.
                else:
                    raise(e) #Some other error that you need to deal with :)


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
            if len(args) == 2: #No email provide ...
                c.execute("INSERT INTO USERS VALUES (?,?, null)", args)
            else:
                c.execute("INSERT INTO USERS VALUES (?,?,?)", args)

        def build_tables():
            c.execute(args[0])

        def insert_character():
            c.execute("INSERT INTO CHARACTERS(user_id, character_name, archetype, timestamp) VALUES (?,?,?,?)", args)

        def update_char_table():
            """This sql statement should be built using string formating but should still be secure using ?? for data values ..?

            UPDATE table_name
            SET col1 = ?, col2 = ?, ...., colN = ?
            WHERE [condition];

            executemany("UPDATE characters
            SET col1=?, col2=?
            WHERE ROWID=?
            argument format should be [[val1,id], [val2,id], [val3,id], ...] while the columns must be built
            using string formating. These names need to be checked for validity.

            I wanted to have the column as a variable. You can't see: https://stackoverflow.com/questions/29335050/sqlite3-updating-row-defined-by-a-variable

            """

            columns = args[0]
            vars_and_id = args[1]

            # check if columns are in table ... if not then raise error do to possible injection attack.
            # requite manual overide.
            # self.check_for_injection(columns)
            sql_statement = EasyDatabase._build_update_table(columns)
            c.execute(sql_statement, vars_and_id)
       
        def update_endurance():
            c.execute('UPDATE CHARACTERS SET current_endurance=? WHERE ROWID=?', args)

        def update_timestamp():
            c.execute('UPDATE CHARACTERS SET timestamp=? WHERE ROWID=?', args)

        options = {'insert_user': insert_user,
            'build_tables': build_tables,
            'insert_character': insert_character,
            'update_char_table': update_char_table,
            'update_endurance': update_endurance,
            'update_timestamp': update_timestamp,
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

        def read_users_rowid():
            c.execute("SELECT ROWID FROM USERS WHERE username=?", args)
            return c.fetchone()[0]

        def read_characters_rowid():
            c.execute("SELECT ROWID FROM CHARACTERS WHERE user_id=? AND character_name=?", args)
            return c.fetchone()[0]
            
        def read_character_data():
            """Rebuild Hero object from database and return it.
            
            NOTE: redefines cursor!
            "SELECT * FROM CHARACTERS WHERE ROWID=?"
            """
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM CHARACTERS WHERE ROWID=?", args)
            return c.fetchone()
            
        def read_character_timestamp():
            c.execute("SELECT timestamp FROM CHARACTERS WHERE ROWID=?", args)
            return c.fetchone()[0]

        #Yes this is kind of slow but the whole exec/compile is a whole nother problem.
        options = {'read_password' : read_password,
                'read_users_rowid' : read_users_rowid,
                'read_characters_rowid': read_characters_rowid,
                'read_character_data': read_character_data,
                'read_character_timestamp': read_character_timestamp,
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
        attributes is an ordered list
        hero is a Hero Class object ... should have a ordered list of attributes
        rowid should extracted from character table using username?
        Basically update all colums in a give row ...

        Arguments format should be columns , [val1, val2, val3, ... valN, id]

        NOTE: data must be 'cleaned'! until I switch over to using SQLAlchemy. https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite
        """

        char_id = self._read(user_id, hero.character_name, read_characters_rowid=True)
        cols = list(vars(hero).keys())
        params = []
        for var in vars(hero).values():
            params.append(EasyDatabase._clean(var))
        params.append(char_id)

        self._write(cols, params, update_char_table=True)

    def _clean(obj):
        """Returns an sqlite3.InterfaceError supported type for all python objects.

        Currently int and str are left alone and everything else is converted to a string.
        I should use SQLAlchemy ...
        Lol. I totally attemted to recreate a basic ORM from scratch.
        """
        if type(obj) is type(int()):
            return obj
        elif type(obj) is type(str()):
            return obj
        else:
            #This should/will end up using recursion any time a python object is hit that is not
            #one of the base objects listed above.
            return str(obj)

    def add_new_user(self, username, password):
        """Add a new user to the database.

        This should auto-validate as username is the primary key.

        NOTE: rowid is now used as user_id

        I can't decide if this should return False on failure or raise an error .. I went with raise error.
        I will build a custom exception at some point too ...
        """
        hashed_password = str(hashlib.md5(password.encode()).hexdigest())
        try:
            self._write(username, hashed_password, insert_user=True)
        except sqlite3.IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: USERS.USERNAME':
                raise Exception("Username '{}' already exists.".format(username)) #raise error if already in use.

    def add_new_character(self, user_id, character, classname):
        """Add a new character to a users account.

        ??Only one character at a time? or multiple characters?
        I will build for one only ...

        NOTE: Updates timestamp
        """
        try:
            now = EasyDatabase.now()
            self._write(user_id, character, classname, now, insert_character=True)
        except sqlite3.IntegrityError as e:
            raise Exception("User '{}' already has a character.".format(username))

    def now():
        """Return current UTC time as datatime object in string form.
        
        NOTE: I am using UTC as we are working in different time zones and I think it might screw up otherwise.
        """
        return datetime.datetime.utcnow()

    def _delete_database(self):
        """Deletes current database file.
        
        Use with caution, mainly for testing.
        """
        os.remove(self.name)

    def validate(self, username, password):
        """Check if username and password match return True if they do.

        Passwords are stored in hashed form so ...
        hash the test password and compare with the retrieved one.
        """
        return  self._read(username, read_password=True) == str(hashlib.md5(password.encode()).hexdigest())

    def get_user_id(self, username):
        """Return the ID of a given user.

        This corresponds to the ROWID from SQL.
        The user must exist ... but since this should only be called after the user has logged in it should be redundant?
        """
        return self._read(username, read_users_rowid=True)

    def _build_char_table(self, hero):
        """Generate a database table based on attributes of the Hero Class.

        This should allow me to avoid updating the database every time anyone changes what a
        Hero looks like.

        NOTE: the time attributes have been added in separately.
        """
        basic_columns = ',\n'.join(column for column in EasyDatabase.generate_column_headings(hero))
        special_columns = 'timestamp UTC DATETIME CURRENT_TIMESTAMP'
        return """CREATE TABLE characters(\n{},\n{})""".format(basic_columns, special_columns)


    def _build_update_table(cols):
        """Return SQL statement for updating the character table based on a list of columns.

        Looks like: UPDATE characters SET {col1} = ?, {col2} = ?, {col3} = ?, ... WHERE ROWID=?
        WORRY: cols should be safe as it is a list pulled from the hero class?
        """
        return """UPDATE characters SET {} WHERE ROWID=?""".format(', '.join(col + '=?' for col in cols))

    def generate_column_headings(obj):
        """Build a table's column headings from a python objects variables.

        Currently only supports data types TEXT and INTEGER and and pythonic type() (whatever that is).

        User_ID is a special case of "INTEGER KEY NOT NULL"

        NOTE: vars(obj) is a dictionary of variable/value pairs for a given object.
        """
        sql_data_type = ''
        for key in sorted(vars(obj).keys()):
            data_type = type(vars(obj)[key])
            if data_type == type(str()):
                sql_data_type = "TEXT"
            elif data_type == type(int()):
                sql_data_type = "INTEGER"
            else:
                sql_data_type = "python_object_as_string"
            if key is 'user_id':
                yield "{} {}".format(key, "INTEGER KEY NOT NULL")
            else:
                yield '{} {}'.format(key, sql_data_type)
                
    def fetch_character_data(self, user_id, character_name):
        """Pull hero object from database and return it based on user_id and character_name.
        
        Could user user_name and character name instead ...
        
        NOTE: makes use of ast.literal_eval which is supposedly safe unlike eval ...?
        NOTE2: currently may mess up time objects?
        NOTE3: Testing has revealed that some keys are in the Character table but not in the
            Hero class ... this should be fixed, see TESTING ONLY!!
        """
        char_id = self._read(user_id, character_name, read_characters_rowid=True)
        
        r = self._read(char_id, read_character_data=True)
        hero = Hero()
        
        #DateTime objects are currently ingnored ...
        for key in r.keys():
            if key in vars(hero).keys():
                try:
                    vars(hero)[key] = ast.literal_eval(r[key])
                except:
                    vars(hero)[key] = r[key]
            else:
                # TESTING ONLY!!
                #some kind of value added to character table that is not in hero class but should be.
                #print("ERROR: '{}' in Character table but not an attribute of the Hero class".format(key))
                pass
                            
        return hero
        
    def _get_character_rowid(self, name, user_id):
        """Return ROWID of character from database based on characters name and user_id.
        
        NOTE: the character name should be the name of the characters hero object.
        eg. hero.character_name
        
        Suggestion: change character_name to just 'name'?
        """
        return self._read(user_id, name, read_characters_rowid=True)
        
    
    def _get_charaters_current_timestamp(self, rowid):
        """Return the character's last updated timestamp return as datatime.
        
        This is used to calculate the change in character endurance.
        """
        timestamp = self._read(rowid, read_character_timestamp=True)
        return datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f')
        
    def _update_endurance(self, value, rowid):
        """Update a characters endurance base on rowid.
        """
        self._write(value, rowid, update_endurance=True)

    def _update_timestamp(self, rowid):
        """Updates characters timestamp to now based on rowid.
        
        """
        self._write(EasyDatabase.now(), rowid, update_timestamp=True)
        
    def update_time(self, hero, user_id):
        """Update the hero game time clock and endurance values.
        
        This increases the hero's endurance by the difference between past timestamp and current time.
        NOTE: Updates current timestamp in charater table but only if endurance changes.
        Which may not be a good idea but ...
        
        NOTE: Must update both hero.current_endurance and current_endurance in Character table
        or update hero then run update_character. I did the first one.
        """
        
        char_id = self._get_character_rowid(hero.character_name, user_id)
        
        #Possible confusion ... hero.current_endurance being updated in old code but
        #is already current?
        
        timestamp = self._get_charaters_current_timestamp(char_id)
        time_diff = (EasyDatabase.now() - timestamp).total_seconds()
        endurance_increment = int(time_diff / second_per_endurance)
        new_endurance = hero.current_endurance + endurance_increment
        
        if hero.current_endurance != hero.max_endurance and endurance_increment:
            if new_endurance < hero.max_endurance:
                hero.current_endurance = new_endurance
            else:
                hero.current_endurance = hero.max_endurance
            self._update_endurance(hero.current_endurance, char_id)
            self._update_timestamp(char_id)
            
        

### Possible import data from spreadsheet
"""
Use https://github.com/pyexcel/pyexcel-ods3

Style would be read file from ....
sheet name = table name
row 1 is list of table colums
rows 2+ .... would be data rows
??? Or something?
"""


### testing
if __name__ == "__main__":
    """
    Currently working on ... replacing all database.py function with class methods in EasyDatabase.

    TODO
    --replicate update_time
    """

    import tests.database_tests



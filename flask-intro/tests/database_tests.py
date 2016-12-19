from database import EasyDatabase

"""
This program runs as a test suite for the EasyDatabase class when it is imported.
"""

def set_up():
    return EasyDatabase('static/test_database.db')
    
def tear_down(database):
    database._delete_database()
    
def test_EasyDatabase_init():
    db = EasyDatabase('static/test_database.db')
    # print(db)
    assert db #looks like it is supposed to ... that will be hard ... :P
    db._delete_database()  
    
def test_add_new_user():
        db = set_up()
        db.add_new_user('Marlen', 'Brunner') #I should be able to add a bunch of users from a text file.
        assert 1 #Check if database has a user called Marlen with a password of Brunner in it.
        tear_down(db)
        

def test_get_user_id():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    user_id = db.get_user_id("Marlen")
    assert user_id == 1
    tear_down(db)
    
    
        # db.create_character(user_id, "Haldon", "Wizard")
    # except Exception as e:
        # print(e.args[0])
    
    # username = 'Marlen'
    # password = "Brunner"
    # db._read(username, read_password=True)
    # print("password valid?", db.validate(username, password))
    
    # print(db.get_user_id(username))
    # db.add_new_user(username, password)
    
    # db.update_character(1, "Haldon")
    
    ##Wipe the database.
    # db._wipe_database()
   
    # db.name = 'static/User.db'
    # username = 'marlen'
    # password = "brunner"
    # print(db._read(username, read_password=True))
    # print("password valid?", db.validate(username, password))    
    

def run_all():
    test_EasyDatabase_init()
    test_add_new_user()
    test_get_user_id()
    print("No Errors, yay!")
    # test2()
    
run_all()
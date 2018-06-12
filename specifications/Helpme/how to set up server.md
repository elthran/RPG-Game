Setup a Flask app on pythonanywhere.com with MySQL support.

## On local computer
### Setup app.py (or ethranonline/\_\_init\_\_.py) file
```python
import private_config

# Configurations
app.config.from_object('private_config')

# Check location of code whether server or local
if 'liveweb' in socket.gethostname():  # Running on server (pythonanywhere)
    app.config['SQLALCHEMY_DATABASE_URI'] = private_config.SERVER_DATABASE_URI
```
SQLALCHEMY_DATABASE_URI is to accommodate Flask-SQLAlchemy ...
otherwise you would replace whatever your normal DATABASE_URI was.


### Setup private_config.py
```python
SERVER_DATABASE_URI = 'mysql+mysqldb://[user_name]:[password]@[user_name].mysql.pythonanywhere-services.com/[user_name]$[database_name]'
```


### Setup local distribution branch
1. In your project make a new branch called distribution
2. $ `git checkout -b distribution` (from whichever branch is your most current one)
3. $ `git push --set-upstream origin distribution`
4. $ `git push`

## On PythonAnywhere
### Go to Consoles page
1. Open a bash console
2. $ `git checkout https://github.com/elthran/RPG-Game.git rpg_game`
3. $ `cd rpg_game`
4. $ `git checkout distribution`
5. $ `git fetch && git pull`
6. $ `export FLASK_APP=elthranonline` (whatever your app name is, I'm not sure if this is neccessary or not ...)
7. $ `pip install --user .` (install your flask application)
8. $ `pip install --user [any missing dependencies]` (If you built your 'setup.py' file correctly you won't need this step :P)


### Go to Files page
1. Open your new rpg_game folder.
2. Upload your 'private_config.py' file (Upload a file button).


### Create a database.
1. Go to Databases tab and create a database. Note that the generated name will be:
'[user_name]$[name_you_picked]' Make sure [name_you_picked] matches the SERVER_DATABASE_URI [database_name]
2. Set a password for the database. (MySQL password section) make it match the SERVER_DATABASE_URI [password]


### Setup Web section.
#### (Code section)
1. Pick a source code directory (e.g. /home/elthran/rpg_game)
2. Pick a working directory (e.g. /home/elthran/rpg_game)
3. Pick a WSGI config file (e.g.  /var/www/elthran_pythonanywhere_com_wsgi.py)
4. Pick a Python version (e.g. 3.5)

#### (Static files section)
1. Pick a static files directory (e.g. /home/elthran/rpg_game/static)

#### (Edit the WSGI file)
Make your WSGI file look like this:
```python
import sys

# add your project directory to the sys.path
project_home = u'/home/elthran/rpg_game/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from elthranonline import app as application
```

#### Reload app.
1. Click reload app button near the top.
2. Test your app by going to 'http://[user_name].pythonanywhere.com/'

#### Debug app.
1. Open a new bash console
2. $ `tail /var/log/[user_name].pythonanywhere.com.[access].log`
   1. OR `tail /var/log/[user_name].pythonanywhere.com.[error].log`
   2. OR `tail /var/log/[user_name].pythonanywhere.com.[server].log`

`tail -n 100` looks at last 100 lines. `tail -f` does live monitoring of the file.

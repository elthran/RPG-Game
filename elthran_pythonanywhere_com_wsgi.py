## NOTE: this goes in the /var/www/elthran_pythonanywhere_com_wsgi.py location on PythonAnywhere for it to do any good.
## I'm just backing it up here .. just in case :)
# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = u'/home/elthran/rpg_game/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import os
# from dotenv import load_dotenv
# load_dotenv(os.path.join(project_home, '.env'))

# import flask app but need to call it "application" for WSGI to work
from app import app as application

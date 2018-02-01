import os
# os.system("del static\database.db")
os.system("cls")
# Custom drop/rebuild database table here.
# See alembic!
print("Take a look at Alembic (and 'clean_start.py' code) if you get database errors!")
try:
    os.system("app.py")
except KeyboardInterrupt:
    pass  # Only raise error from the actual program

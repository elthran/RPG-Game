import os
# os.system("del static\database.db")
# Custom drop/rebuild database table here.
# See alembic!
print("Take a look at Alembic if you get database errors!")
os.system("cls")
try:
    os.system("app.py")
except KeyboardInterrupt:
    pass  # Only raise error from the actual program

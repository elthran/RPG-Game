import os
# os.system("del static\database.db")
os.system("cls")
try:
    os.system("app.py")
except KeyboardInterrupt:
    pass  # Only raise error from the actual program

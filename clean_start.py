import os
import argparse
import platform

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-v", "--verbose",
    #                     help="Cleanly start 'app.py' .. possibly rebuild the database.",
    #                     action='store_true')
    parser.add_argument("-f", help="Delete the database.", action='store_true')
    args = parser.parse_args()
    # print(args)

    # Mult-system clear screen.
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear && printf '\033[3J'")

    print("Take a look at Alembic (and 'clean_start.py' code) if you get database errors!")
    if args.f:
        os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
        print("Database deleted!")

    try:
        os.system("python3 app.py")
    except KeyboardInterrupt:
        pass  # Only raise error from the actual program


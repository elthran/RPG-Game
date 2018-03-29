import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-v", "--verbose",
    #                     help="Cleanly start 'app.py' .. possibly rebuild the database.",
    #                     action='store_true')
    parser.add_argument("-f", help="Delete the database.", action='store_true')
    parser.add_argument("-m", help="Make blank database for migrations.", action='store_true')
    args = parser.parse_args()
    # print(args)

    os.system("cls")
    print("Take a look at Alembic (and 'clean_start.py' code) if you get database errors!")
    if args.f:
        os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
        print("Database deleted!")
    elif args.m:
        os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
        os.system("python3 -c 'import database;database.EZDB(\"mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database\", debug=False, testing=True);print(\"Blank database initialized!\")'")
        exit(0)

    try:
        os.system("app.py")
    except KeyboardInterrupt:
        pass  # Only raise error from the actual program


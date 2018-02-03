import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-v", "--verbose",
    #                     help="Cleanly start 'app.py' .. possibly rebuild the database.",
    #                     action='store_true')
    parser.add_argument("-f", help="Delete the database.", action='store_true')
    args = parser.parse_args()
    # print(args)

    os.system("cls")
    print("Take a look at Alembic (and 'clean_start.py' code) if you get database errors!")
    if args.f:
        print("Database delete and rebuilt!")
        os.system("mysql -u root -p7ArQMuTUSoxXqEfzYfUR rpg_database < rebuild_database.sql")

    try:
        os.system("app.py")
    except KeyboardInterrupt:
        pass  # Only raise error from the actual program


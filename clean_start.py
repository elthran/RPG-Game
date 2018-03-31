import os
import argparse
import platform

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("-v", "--verbose",
    #                     help="Cleanly start 'app.py' .. possibly rebuild the database.",
    #                     action='store_true')
    parser.add_argument("-f", help="Delete the database.", action='store_true')
    parser.add_argument("-t", help="Run code profiling on app.py.",
                        action='store_true')
    parser.add_argument(
        "-p",
        nargs='*',
        help="""Print code statistics created by using -t option. Accepts a list of arguments for pstats 'sort_stats(*args)'""",
        default=False
    )
    parser.add_argument("-c", help="Compile all the game code. "
                                   "Max level optimization!",
                        action='store_true')
    parser.add_argument("-g", help="Print a nice graph of the code profile.",
                        action='store_true')
    parser.add_argument("-m", help="Make blank database for migrations.", action='store_true')
    args = parser.parse_args()

    if args.p == []:
        args.p = ['cumtime']
    # print(args)
    # exit()
    # Mult-system clear screen.
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear && printf '\033[3J'")

    print("Take a look at Alembic (and 'clean_start.py' code) if you get database errors!")
    if args.f:
        os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS rpg_database;"')
        print("Database deleted!")
    elif args.t:
        os.system("python3 -m cProfile -o code_profile.pstats app.py")
    elif args.c:
        os.system("python -OO -m compileall -f ./")
    elif args.p:
        import pstats
        p = pstats.Stats('code_profile.pstats')
        p.strip_dirs().sort_stats(*args.p).print_stats(.05)
    elif args.g:
        os.system("gprof2dot -f pstats code_profile.pstats | "
                  "dot -Tpng -o code_profile.png")
    elif args.m:
        os.system('mysql -u elthran -p7ArQMuTUSoxXqEfzYfUR -e "DROP DATABASE IF EXISTS old_rpg_database;"')
        os.system("python3 -c 'import database;database.EZDB(\"mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/old_rpg_database\", debug=False, testing=True);print(\"Blank database \'old_rpg_database\' with current schema initialized!\")'")
        exit(0)

    if not any([args.c, args.p, args.t, args.g, args.m]):
        try:
            os.system("python3 app.py")
        except KeyboardInterrupt:
            pass  # Only raise error from the actual program

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
        # const=["cumtime"],
        default=False
    )
    parser.add_argument("-c", help="Compile all the game code!",
                        action='store_true')
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
        os.system("python3 -m cProfile -o restats app.py")
    elif args.c:
        os.system("python -m compileall ./")
    elif args.p:
        import pstats
        p = pstats.Stats('restats')
        p.strip_dirs().sort_stats(*args.p).print_stats(.05)

    if not args.c and not args.p and not args.t:
        try:
            os.system("python3 app.py")
        except KeyboardInterrupt:
            pass  # Only raise error from the actual program


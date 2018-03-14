"""
This test suite should be run each time I make changes to the main game code before I push the changes.
This should ensure that my changes didn't break anything.

This modules is run using:
$ python3 test_all.py
or for post mortem debugging
$ python3 -m pdb test_all.py

It then imports all of the unit tests for each module in the game.
These test suites should run on import.
Using: https://docs.pytest.org/en/latest/getting-started.html

Useful options:
PS> clear;pytest -x -vv -l -s
$ cls && pytest -x -vv -l -s

s - no output capture (shows print statement output)
x - exit after first failed test
v - verbose
vv - show full length output
l - show local vars during traceback (when a test fails)
"""

import os
import platform

if __name__ == "__main__":
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear && printf '\033[3J'")
    os.system("pytest -x -vv -l -s")

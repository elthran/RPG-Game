import os

if __name__ == "__main__":
    os.system("python3 -m pytest -vv {}".format(__file__))
    exit()  # prevents code from trying to run file afterwards.

import configparser
import pdb

import pytest

from database import EZDB

config = configparser.ConfigParser()
config.read('rpg_game_tests/test.ini')
url = config['DEFAULT']['url']


class GenericTestCase:
    url = url

    @classmethod
    def setup_class(cls):
        """Setup any state specific to the execution of the given class (which

        usually contains tests).
        """
        # print("Setup class")
        return EZDB(url, debug=False, testing=True)

    @classmethod
    def teardown_class(cls, delete=True):
        # print("Teardown class")
        db = EZDB(url, debug=False, testing=True)
        if delete:
            db._delete_database()
        return db

    def setup(self):
        # print("Setup")
        self.db = EZDB(url, debug=False, testing=True)

    def teardown(self, delete=False):
        # print("Teardown")
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()

    def rebuild_instance(self):
        """Tidy up and rebuild database instance.

        ... otherwise you may not be retrieving the actual data
        from the database only from memory.
        """

        # print("Rebuild instance")
        self.db.update()
        self.teardown(delete=False)
        self.setup()


def db_execute_script(path, ezdb):
    """Execute the sql script file located at path.

    Error handling is poor ...

    ezdb can be any database like thing that has an attached
    'engine'.

    NOTE: this can't handle comments and can only handle functions
    that are one line long.

    I want to improve this so that I can execute multi-line input.
    """

    with open(path, 'r') as file:
        wait = False
        ignore = False
        long_line = ''
        for line in file:
            if line != os.linesep and not any([line.startswith('--'), line.startswith("/*")]):
                ezdb.engine.execute(line)


class Mock:
    def __init__(self, location, value):
        attrs = location.split('.')
        if len(attrs) > 1:
            setattr(self, attrs[0], Mock('.'.join(attrs[1:]), value))
        setattr(self, location, value)

    @classmethod
    def blank(cls):
        temp = cls.__init__
        cls.__init__ = lambda self: None
        mock = cls()
        cls.__init__ = temp
        return mock


class TestMock:
    def test_init(self):
        mock_hero = Mock('current_location.id', 5)

        assert mock_hero.current_location.id == 5

    def test_blank(self):
        mock_hero = Mock.blank()
        assert type(mock_hero) == Mock

        # Make sure init isn't messed up by blank.
        mock_hero = Mock('current_location.id', 5)
        assert mock_hero.current_location.id == 5

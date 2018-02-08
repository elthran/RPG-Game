import configparser
from database import EZDB

config = configparser.ConfigParser()
config.read('tests/test.ini')
url = config['DEFAULT']['url']


class GenericTestClass:
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

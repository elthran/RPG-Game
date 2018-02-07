import pytest
import pdb
from pprint import pprint

from database import EZDB
# from hero import Hero
# from inventory import Inventory
from items import Item, OneHandedWeapon


"""
NOTE:
Run order looks like:

setup_class
setup
method_1
teardown
setup
method_2
teardown
teardown_class

And it seems to create a new instance of the class for each method.
e.g.
if method_1 defines self.name = "marlen"

and method_2 calss self.name ... it won't work.

You need to define class level variables to pass data.
TestItem.name = "marlen" should be available everywhere.

    Though I recommend defining them in the 'setup_class' method first
so that they are easier to keep track of.


Some useful decorators (@ things :P).
@pytest.mark.incremental - if test 1 fails don't try test 2 and so on.
@pytest.mark.skip("Some message ...") - skips with message.

Other at https://docs.pytest.org/en/latest/builtin.html

Get all built in decorators with:
    pytest --markers
    
Add new markers in the 'conftest.py'. I don't really understand the syntax yet.
"""

import configparser
config = configparser.ConfigParser()
config.read('tests/test.ini')
url = config['DEFAULT']['url']


@pytest.mark.incremental
class TestItem:
    @classmethod
    def setup_class(cls):
        """Setup any state specific to the execution of the given class (which

        usually contains tests).
        """
        # print("Setup class")
        EZDB(url, debug=False, testing=True)
        cls.template_id = 0
        cls.item_id = 0

    @classmethod
    def teardown_class(cls, delete=True):
        # print("Teardown class")
        if delete:
            db = EZDB(url, debug=False, testing=True)
            db._delete_database()

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

    def test_init(self):
        """Check if object is created, storeable and retrievable.
        """
        template = OneHandedWeapon(
            "Small Dagger", buy_price=5, damage_minimum=30, damage_maximum=60,
            speed_speed=1)
        self.db.session.add(template)
        self.db.session.commit()
        TestItem.template_id = template.id
        str_template = template.pretty

        self.rebuild_instance()
        template2 = self.db.session.query(Item).get(TestItem.template_id)
        assert str_template == template2.pretty

    # @pytest.mark.skip("Not built.")
    def test_build_from_template(self):
        template = self.db.session.query(Item).get(TestItem.template_id)
        item = template.build_new_from_template()
        self.db.session.add(item)
        self.db.session.commit()
        TestItem.item_id = item.id
        str_item = item.pretty
        
        self.rebuild_instance()
        item2 = self.db.session.query(Item).get(TestItem.item_id)
        assert str_item == item2.pretty

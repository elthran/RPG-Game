import pytest
import pdb
from pprint import pprint

from database import EZDB
# from hero import Hero
# from inventory import Inventory
from . import GenericTestCase

from items import Item, OneHandedWeapon, Ring


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


@pytest.mark.incremental
class TestItem(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        # Might be better for testing? To allow post mortem analysis.
        db.engine.execute("DROP TABLE `proficiency`;")
        db.engine.execute("DROP TABLE `item`;")
        db = super().setup_class()

        template = OneHandedWeapon(
            "Big Dagger", buy_price=10,
            proficiency_data=[('Damage', {'base': 300}),
                              ('Combat', {'base': 600}),
                              ('Speed', {'base': 2})],
            template=True)
        db.session.add(template)
        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)
        # db.engine.execute("DROP TABLE `item`;")

    def setup(self):
        super().setup()
        self.template = self.db.session.query(
            Item).filter_by(name="Big Dagger", template=True).first()

    def test_init(self):
        """Check if object is created, storeable and retrievable.
        """
        template = self.template
        str_template = template.pretty

        self.rebuild_instance()
        template2 = self.template
        assert str_template == template2.pretty

    def test_build_from_template(self):
        template = self.template
        item = template.build_new_from_template()
        self.db.session.add(item)
        self.db.session.commit()
        str_item = item.pretty
        item_id = item.id
        
        self.rebuild_instance()
        item2 = self.db.session.query(Item).get(item_id)
        assert str_item == item2.pretty

    def test_create_item(self):
        template = self.template
        item = self.db.create_item(template.id)
        self.db.session.add(item)
        self.db.session.commit()
        item_id = item.id
        str_item = item.pretty

        self.rebuild_instance()
        item2 = self.db.session.query(Item).get(item_id)
        assert str_item == item2.pretty

    def test_ring(self):
        template = Ring("Silver Ring", 8, template=True)
        self.db.session.add(template)
        self.db.session.commit()

        template_id = template.id
        item = self.db.create_item(template.id)
        self.db.session.commit()
        str_item = item.pretty
        self.rebuild_instance()

        item2 = self.db.session.query(
            Item).filter_by(name="Silver Ring", template=False).first()
        assert str_item == item2.pretty
        assert template_id != item2.id

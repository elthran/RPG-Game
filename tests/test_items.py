import pytest
import pdb

from database import EZDB
# from hero import Hero
# from inventory import Inventory
from items import Item, OneHandedWeapon


class TestItem:
    def setup(self):
        self.template = OneHandedWeapon(
            "Small Dagger", buy_price=5, min_damage=30,
            max_damage=60, attack_speed=1)
        self.item = Item(self.template)
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        self.db.session.add(self.template)
        self.db.session.add(self.item)
        self.db.session.commit()
    
    def teardown(self, delete=False):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()
            
    def rebuild_instance(self):
        """Tidy up and rebuild database instance.

        ... otherwise you may not be retrieving the actual data
        from the database only from memory.
        """

        self.db.session.commit()
        self.teardown(delete=False)
        self.setup()

    def test_init(self):
        """Check if object is created, storeable and retrievable.
        """
        str_item = str(self.item)

        self.rebuild_instance()
        item2 = self.db.session.query(
            Item).filter_by(name='Small Dagger').first()
        self.assertEqual(str_item, str(item2))

    @pytest.mark.skip("Not built.")
    def test_load_template(self):
        # str_item = str(item)
        
        # self.rebuild_instance()
        # item2 = self.db.session.query(Item).filter_by(name='S').first()
        self.assertEqual("", "not built")
        

if __name__ == '__main__':
    pass

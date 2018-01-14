import pytest
import pdb

from database import EZDB
# from hero import Hero
# from inventory import Inventory
from items import Item, OneHandedWeapon


class TestItem:
    @classmethod
    def setup_class(cls):
        """Setup any state specific to the execution of the given class (which

        usually contains tests).
        """
        cls.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        cls.template = OneHandedWeapon(
            "Small Dagger", buy_price=5, damage_minimum=30, damage_maximum=60,
            speed_speed=1)
        cls.db.session.add(cls.template)
        cls.db.update()

        cls.item = cls.db.create_item(1)
        cls.db.session.add(cls.item)
        cls.db.session.commit()

    @classmethod
    def teardown_class(cls, delete=False):
        cls.db.session.close()
        cls.db.engine.dispose()
        if delete:
            cls.db._delete_database()
            
    def rebuild_instance(self):
        """Tidy up and rebuild database instance.

        ... otherwise you may not be retrieving the actual data
        from the database only from memory.
        """

        self.db.update()
        self.teardown_class(delete=False)

    def test_init(self):
        """Check if object is created, storeable and retrievable.
        """
        str_item = self.item.pretty

        self.rebuild_instance()
        item2 = self.db.session.query(
            Item).filter_by(name='Small Dagger', template=False).first()
        assert str_item == item2.pretty

    @pytest.mark.skip("Not built.")
    def test_load_template(self):
        # str_item = str(item)
        
        # self.rebuild_instance()
        # item2 = self.db.session.query(Item).filter_by(name='S').first()
        assert "" == "not built"
        

if __name__ == '__main__':
    pass

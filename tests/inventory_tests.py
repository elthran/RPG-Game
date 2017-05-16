from database import EZDB
from game import Hero, Inventory
from items import Item, ItemTemplate
import complex_relationships

import unittest
import pdb           


##########
#Inventory: work in progress
##########

class InventoryTestCase(unittest.TestCase):
    def setUp(self):
        #Testing=False loads prebuilt_objects.
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=False)
        self.db.session.commit()
        self.hero = self.db.session.query(Hero).filter_by(id=1).first()
        self.inv = self.hero.inventory
        print("setUp")
    
    def tearDown(self, delete=True):
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
        self.tearDown(delete=False)
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=True)
        self.hero = self.db.session.query(Hero).filter_by(id=1).first()
        self.inv = self.hero.inventory

    def test_inventory_init(self):
        """Check if object is created, storeable and retrievable.
        """
        str_inventory = str(self.inv)

        self.rebuild_instance()
        self.assertEqual(str_inventory, str(self.inv))
        
    def test_add_item(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        str_inventory = str(self.inv)

        self.rebuild_instance()
        self.assertEqual(str_inventory, str(self.inv))
        
    def test_equip_item(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        ids_to_unequip = self.inv.equip(item)
        self.inv.pprint()
        item.pprint()
        
        self.assertEqual("", "not built")
    
        
if __name__ == '__main__':
    unittest.main()

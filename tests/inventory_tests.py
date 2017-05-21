from database import EZDB
from game import Hero, Inventory
from items import Item, ItemTemplate
import complex_relationships

import unittest
import pdb           
import re

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
            print("tearDown")
            
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
    
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_inventory_init(self):
        """Check if object is created, storeable and retrievable.
        """
        str_inventory = str(self.inv)

        self.rebuild_instance()
        self.assertEqual(str_inventory, str(self.inv))
    
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")    
    def test_add_item(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        str_inventory = str(self.inv)

        self.rebuild_instance()
        self.assertEqual(str_inventory, str(self.inv))
    
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")    
    def test_equip_helmet(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        inv_str = str(self.inv)
        item_str = str(item)

        ids_to_unequip = self.inv.equip(item)
        self.rebuild_instance()
        
        inv_str2 = str(self.inv)
        item_str2 = str(self.inv.helmet)

        self.assertEqual(
            inv_str,
            inv_str2.replace("helmet='<Item(id=1)>'", "helmet=None"
            ).replace("helmet_id=1", "helmet_id=None"
            ).replace("unequipped=[]", "unequipped='[Item.id=1]'"))
        self.assertEqual(item_str, 
            item_str2.replace("inventory_helmet='<Inventory(id=2)>'", "inventory_helmet=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("unequipped_id=None", "unequipped_id=2"))
           
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_equip_both_hands(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Polearm").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        inv_str = str(self.inv)
        item_str = str(item)

        ids_to_unequip = self.inv.equip(item)
        self.rebuild_instance()
        
        inv_str2 = str(self.inv)
        item_str2 = str(self.inv.both_hands)

        self.assertEqual(
            inv_str,
            inv_str2.replace("both_hands='<Item(id=1)>'", "both_hands=None"
            ).replace("both_hands_id=1", "both_hands_id=None"
            ).replace("unequipped=[]", "unequipped='[Item.id=1]'"))
        self.assertEqual(item_str, 
            item_str2.replace("inventory_both_hands='<Inventory(id=2)>'", "inventory_both_hands=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("unequipped_id=None", "unequipped_id=2"))
            
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")        
    def test_equip_ring(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Silver Ring").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        inv_str = str(self.inv)
        item_str = str(item)
        
        ids_to_unequip = self.inv.equip(item, 7)
        
        self.rebuild_instance()
        
        inv_str2 = str(self.inv)
        item_str2 = str(self.inv.rings[0])

        self.assertEqual(
            inv_str,
            inv_str2.replace("rings='[Item.id=1]'", "rings=[]"
            ).replace("unequipped=[]", "unequipped='[Item.id=1]'"))
        self.assertEqual(item_str, 
            item_str2.replace("inventory_rings='<Inventory(id=2)>'", "inventory_rings=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("rings_id=2", "rings_id=None"
            ).replace("unequipped_id=None", "unequipped_id=2"))
    
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")        
    def test_replace_helmet(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        item2 = self.db.create_item(template.id)
        self.inv.add_item(item)
        self.inv.add_item(item2)
        
        inv_str = str(self.inv)
        item2_str = str(item2)
        
        self.inv.equip(item)
        ids_to_unequip = self.inv.equip(item2)
        self.rebuild_instance()
        
        item2_str2 = str(self.inv.helmet)
        self.assertEqual(
            inv_str,
            str(self.inv).replace("helmet='<Item(id=2)>'", "helmet=None"
            ).replace("helmet_id=2", "helmet_id=None"
            ).replace("unequipped='[Item.id=1]'", "unequipped='[Item.id=1, Item.id=2]'"))
        self.assertEqual(item2_str, 
            item2_str2.replace("inventory_helmet='<Inventory(id=2)>'", "inventory_helmet=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("unequipped_id=None", "unequipped_id=2"))
        self.assertEqual(ids_to_unequip, [1])
        
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_replace_both_hands(self):
        polearm_template = self.db.session.query(ItemTemplate).filter_by(name="Medium Polearm").first()
        shield_template = self.db.session.query(ItemTemplate).filter_by(name="Small Shield").first()
        sword_template = self.db.session.query(ItemTemplate).filter_by(name="Big Dagger").first()
        
        shield = self.db.create_item(shield_template.id)
        sword = self.db.create_item(sword_template.id)
        polearm = self.db.create_item(polearm_template.id)
        self.inv.add_item(shield)
        self.inv.add_item(sword)
        self.inv.add_item(polearm)
        
        self.inv.equip(sword)
        self.inv.equip(shield)
        
        inv_str = str(self.inv)
        polearm_str = str(polearm)        
        
        ids_to_unequip = self.inv.equip(polearm)
        self.rebuild_instance()
        
        polearm2_str = str(self.inv.both_hands)
        self.assertEqual(inv_str,
            str(self.inv).replace("both_hands='<Item(id=3)>'", "both_hands=None"
            ).replace("both_hands_id=3", "both_hands_id=None"
            ).replace("left_hand=None", "left_hand='<Item(id=1)>'"
            ).replace("left_hand_id=None", "left_hand_id=1"
            ).replace("right_hand=None", "right_hand='<Item(id=2)>'"
            ).replace("right_hand_id=None", "right_hand_id=2"
            ).replace("unequipped='[Item.id=1, Item.id=2]'", "unequipped='[Item.id=3]'"))
        self.assertEqual(ids_to_unequip, [1, 2])
        
    def test_equip_lots_of_rings(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Silver Ring").first()
        
        ids_to_unequip = []
        for i in range(12):
            item = self.db.create_item(template.id)
            self.inv.add_item(item)
            try:
                self.inv.equip(item, i)
            except IndexError as ex:
                self.assertTrue(i >= 10)
                self.assertEqual(str(ex), "'Ring' index out of range. Index must be from 0 to 9.")
        
        self.inv.pprint()
        inv_str = str(self.inv)
        
        pdb.set_trace()
        ids_to_unequip = self.inv.equip(self.inv.unequipped[1], 4)
        
        self.rebuild_instance()
        
        self.inv.pprint()
        print("ids:", ids_to_unequip)
        # inv_str2 = str(self.inv)
        # item_str2 = str(self.inv.rings[0])

        # self.assertEqual(
            # inv_str,
            # inv_str2.replace("rings='[Item.id=1]'", "rings=[]"
            # ).replace("unequipped=[]", "unequipped='[Item.id=1]'"))
        # self.assertEqual(item_str, 
            # item_str2.replace("inventory_rings='<Inventory(id=2)>'", "inventory_rings=None"
            # ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            # ).replace("rings_id=2", "rings_id=None"
            # ).replace("unequipped_id=None", "unequipped_id=2"))
        
        
if __name__ == '__main__':
    unittest.main()

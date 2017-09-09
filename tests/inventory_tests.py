import unittest
import pdb
import re

from database import EZDB
from game import Hero, Inventory
from items import Item, ItemTemplate
import complex_relationships

##########
# Inventory: work in progress
##########


class InventoryTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        # Testing=False loads prebuilt_objects.
        self.db = EZDB('sqlite:///tests/test.db', debug=False, testing=False)
        self.db.session.commit()
        self.hero = self.db.session.query(Hero).filter_by(id=1).first()
        self.inv = self.hero.inventory
        # print("setUp")
    
    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()
            # print("tearDown")
            
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
        str_inventory = self.inv.pretty

        self.rebuild_instance()
        self.assertEqual(str_inventory, self.inv.pretty)
    
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_add_item(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        str_inventory = str(self.inv)

        self.rebuild_instance()
        self.assertEqual(str_inventory, str(self.inv))
    
    # @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")    
    def test_equip_helmet(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        self.inv.items.append(item)
        
        inv_str = self.inv.pretty
        item_str = item.pretty

        ids_to_unequip = self.inv.equip2(item)
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        item_str2 = self.inv.helmet.pretty

        self.assertEqual(
            inv_str,
            inv_str2.replace("helmet='<Item(id=1)>'", "helmet=None"
            ).replace("helmet_item_id=1", "helmet_item_id=None"
            ))
        self.assertEqual(item_str, 
            item_str2.replace("inventory_helmet='<Inventory(id=2)>'", "inventory_helmet=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("unequipped_inventory_id=None", "unequipped_inventory_id=2"))
           
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_equip_both_hands(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Polearm").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        inv_str = self.inv.pretty
        item_str = item.pretty

        ids_to_unequip = self.inv.equip(item)
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        item_str2 = self.inv.both_hands.pretty

        self.assertEqual(
            inv_str,
            inv_str2.replace("both_hands='<Item(id=1)>'", "both_hands=None"
            ).replace("both_hands_item_id=1", "both_hands_item_id=None"
            ).replace("unequipped=[]", "unequipped='[Item.id=1]'"))
        self.assertEqual(item_str, 
            item_str2.replace("inventory_both_hands='<Inventory(id=2)>'", "inventory_both_hands=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("unequipped_inventory_id=None", "unequipped_inventory_id=2"))
            
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_equip_ring(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Silver Ring").first()
        item = self.db.create_item(template.id)
        self.inv.add_item(item)
        
        inv_str = self.inv.pretty
        item_str = item.pretty
        
        ids_to_unequip = self.inv.equip(item, 7)
        
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        item_str2 = self.inv.rings[0].pretty
        
        self.assertEqual(
            inv_str,
            inv_str2.replace("rings='[Item.id=1]'", "rings=[]"
            ).replace("unequipped=[]", "unequipped='[Item.id=1]'"))
        self.assertEqual(item_str, 
            item_str2.replace("inventory_rings='<Inventory(id=2)>'", "inventory_rings=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("rings_inventory_id=2", "rings_inventory_id=None"
            ).replace("unequipped_inventory_id=None", "unequipped_inventory_id=2"
            ).replace("rings_position=0", "rings_position=None"))
    
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_replace_helmet(self):
        template = self.db.session.query(ItemTemplate).filter_by(name="Medium Helmet").first()
        item = self.db.create_item(template.id)
        item2 = self.db.create_item(template.id)
        self.inv.add_item(item)
        self.inv.add_item(item2)
        
        inv_str = self.inv.pretty
        item2_str = item2.pretty
        
        self.inv.equip(item)
        ids_to_unequip = self.inv.equip(item2)
        self.rebuild_instance()
        
        item2_str2 = self.inv.helmet.pretty
        inv_str2 = self.inv.pretty
        self.assertEqual(inv_str,
            inv_str2.replace("helmet='<Item(id=2)>'", "helmet=None"
            ).replace("helmet_item_id=2", "helmet_item_id=None"
            ).replace("unequipped='[Item.id=1]'", "unequipped='[Item.id=1, Item.id=2]'"))
        self.assertEqual(item2_str, 
            item2_str2.replace("inventory_helmet='<Inventory(id=2)>'", "inventory_helmet=None"
            ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            ).replace("unequipped_inventory_id=None", "unequipped_inventory_id=2"
            ).replace("unequipped_position=0", "unequipped_position=1"))
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
        
        inv_str = self.inv.pretty
        polearm_str = polearm.pretty       
        
        ids_to_unequip = self.inv.equip(polearm)
        self.rebuild_instance()
        
        polearm2_str = self.inv.both_hands.pretty
        inv_str2 = self.inv.pretty
        self.assertEqual(inv_str,
            inv_str2.replace("both_hands='<Item(id=3)>'", "both_hands=None"
            ).replace("both_hands_item_id=3", "both_hands_item_id=None"
            ).replace("left_hand=None", "left_hand='<Item(id=1)>'"
            ).replace("left_hand_item_id=None", "left_hand_item_id=1"
            ).replace("right_hand=None", "right_hand='<Item(id=2)>'"
            ).replace("right_hand_item_id=None", "right_hand_item_id=2"
            ).replace("unequipped='[Item.id=1, Item.id=2]'", "unequipped='[Item.id=3]'"))
        self.assertEqual(ids_to_unequip, [1, 2])
        
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
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
        
        inv_str = str(self.inv)
        
        silver_ring12 = self.inv.unequipped[1]
        ids_to_unequip = self.inv.equip(silver_ring12, 4)
        
        self.rebuild_instance()
        
        inv_str2 = str(self.inv)

        self.assertEqual(
            inv_str,
            inv_str2.replace("Item.id=4, Item.id=12, Item.id=6", "Item.id=4, Item.id=5, Item.id=6"
            ).replace("unequipped='[Item.id=11, Item.id=5]'", "unequipped='[Item.id=11, Item.id=12]'"))
        self.assertEqual(ids_to_unequip, [5])
        
    @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_unequip_legs(self):
        pants_template = self.db.session.query(ItemTemplate).filter_by(name="Medium Pants").first()
        
        pants = self.db.create_item(pants_template.id)
        self.inv.add_item(pants)
        
        self.inv.equip(pants)      
        self.rebuild_instance()
        
        inv_str = self.inv.pretty
        pants_str = self.inv.legs.pretty
        
        self.inv.unequip(self.inv.legs)
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        pants_str2 = self.inv.unequipped[0].pretty
        self.assertEqual(inv_str,
            inv_str2.replace("legs=None", "legs='<Item(id=1)>'"
            ).replace("legs_item_id=None", "legs_item_id=1"
            ).replace("unequipped='[Item.id=1]'", "unequipped=[]"))
        self.assertEqual(pants_str,
            pants_str2.replace("inventory_legs=None", "inventory_legs='<Inventory(id=2)>'"
            ).replace("inventory_unequipped='<Inventory(id=2)>'", "inventory_unequipped=None"
            ).replace("unequipped_inventory_id=2", "unequipped_inventory_id=None"))

    @unittest.skip("Temporarily disabled for speed of development ->"
                   " re-enable before you trust :)")
    def test_unequip_ring(self):
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
        
        self.rebuild_instance()
        
        inv_str = self.inv.pretty
        ring_string = self.inv.rings[4].pretty
        
        silver_ring5 = self.inv.rings[4]
        self.inv.unequip(silver_ring5)
        
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        ring_string2 = self.inv.unequipped[2].pretty

        self.assertEqual(inv_str,
            inv_str2.replace("Item.id=4, Item.id=6", "Item.id=4, Item.id=5, Item.id=6"
            ).replace("unequipped='[Item.id=11, Item.id=12, Item.id=5]'", "unequipped='[Item.id=11, Item.id=12]'"))
        self.assertEqual(ring_string,
            ring_string2.replace("inventory_rings=None", "inventory_rings='<Inventory(id=2)>'"
            ).replace("inventory_unequipped='<Inventory(id=2)>'","inventory_unequipped=None"
            ).replace("unequipped_inventory_id=2","unequipped_inventory_id=None"
            ).replace("unequipped_position=2","unequipped_position=0"
            ).replace("rings_inventory_id=None", "rings_inventory_id=2"
            ))
        
if __name__ == '__main__':
    unittest.main()

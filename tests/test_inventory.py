import pytest
from pprint import pprint
import pdb
import re

from database import EZDB
from hero import Hero
from inventory import Inventory
from items import Item, OneHandedWeapon, HeadArmour, TwoHandedWeapon, Ring

from generic_setup import GenericTestClass

"""
Inventory: work in progress
Useful: 

$ pytest -x -vv -l

s - no output capture (shows print statement output)
x - exit after first failed test
v - verbose
vv - show full length output
l - show local vars during traceback (when a test fails)
"""


@pytest.mark.incremental
class TestInventory(GenericTestClass):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        hero = Hero(name="Haldon")
        db.session.add(hero)

        # Add stock item/template combo - helmet/head armour.
        template = HeadArmour("Medium Helmet", 4, armour_value=3)
        db.session.add(template)
        db.session.commit()
        item = template.build_new_from_template()
        db.session.add(item)
        db.session.commit()

        # Add second stock item/template combo - 2 handed weapon.
        template_2handed = TwoHandedWeapon(
            "Medium Polearm", buy_price=5, damage_minimum=30,
            damage_maximum=60, speed_speed=1)
        db.session.commit()
        item_2handed = template_2handed.build_new_from_template()
        db.session.add(item_2handed)
        db.session.commit()

        template_ring = Ring("Silver Ring", 8)
        item_ring = template_ring.build_new_from_template()
        db.session.add(item_ring)

        db.update()

    def setup(self):
        super().setup()
        self.hero = self.db.session.query(Hero).get(1)
        self.inv = self.hero.inventory
        self.item_helmet = self.db.session.query(
            Item).filter_by(name="Medium Helmet").first()
        self.item_polearm = self.db.session.query(
            Item).filter_by(name="Medium Polearm").first()
        self.item_ring = self.db.session.query(Item).filter_by(
            name="Silver Ring").first()

    def test_init(self):
        """Check if object is created, storeable and retrievable.
        """

        str_inventory = self.inv.pretty

        self.rebuild_instance()
        assert str_inventory == self.inv.pretty
    
    def test_add_item(self):
        """Test if item is added successfully to inventory.

        This should add the item to the unequipped slot.
        """
        self.inv.add_item(self.item_helmet)
        str_inventory = self.inv.pretty
        str_item = self.item_helmet.pretty

        self.rebuild_instance()
        str_unequipped = self.inv.unequipped[0].pretty

        assert str_inventory == self.inv.pretty
        assert str_item == str_unequipped
    
    def test_equip_helmet(self):
        """Test if you can equip a helmet.

        And that it goes to the head slot.
        """
        inv_str = self.inv.pretty
        item_str = self.item_helmet.pretty
        ids_to_unequip = self.inv.equip(self.item_helmet)

        self.rebuild_instance()
        inv_str2 = self.inv.pretty
        helmet = self.inv.head.pretty

        assert inv_str.replace(
             "head=None", "head='<HeadArmour(id=1)>'").replace(
            "equipped=[]", "equipped='[HeadArmour.id=1]'").replace(
            "unequipped='[HeadArmour.id=1]'", "unequipped=[]") == inv_str2

        assert item_str.replace(
            "equipped=False", "equipped=True").replace(
            "unequipped_position=0", "unequipped_position=None") == helmet
           
    def test_equip_both_hands(self):
        """Test if when you add a two handed weapon it equips in both hands.

        The equip + replacement test comes later.
        """
        self.inv.add_item(self.item_polearm)
        inv_str = self.inv.pretty
        item_str = self.item_polearm.pretty

        ids_to_unequip = self.inv.equip(self.item_polearm)
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        item_str2 = self.inv.both_hands.pretty

        assert inv_str.replace(
            "both_hands=None", "both_hands='<TwoHandedWeapon(id=3)>'").replace(
            "equipped='[HeadArmour.id=1]'",
            "equipped='[HeadArmour.id=1, TwoHandedWeapon.id=3]'").replace(
            "unequipped='[TwoHandedWeapon.id=3]'", "unequipped=[]") == inv_str2
        assert item_str.replace(
            "equipped=False", "equipped=True").replace(
            "unequipped_position=0", "unequipped_position=None") == item_str2
            
    def test_equip_ring(self):
        """Test if rings can be equipped safely."""

        self.inv.add_item(self.item_ring)
        inv_str = self.inv.pretty
        item_str = self.item_ring.pretty

        ids_to_unequip = self.inv.equip(self.item_ring)
        
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        item_str2 = self.inv.rings[0].pretty
        
        assert inv_str.replace(
            "rings=[]", "rings='[Ring.id=4]'").replace(
            "equipped='[HeadArmour.id=1, TwoHandedWeapon.id=3]'",
            "equipped='[HeadArmour.id=1, TwoHandedWeapon.id=3, Ring.id=4]'"
        ).replace("unequipped='[Ring.id=4]'", "unequipped=[]") == inv_str2

        assert item_str.replace(
            "equipped=False", "equipped=True").replace(
            "unequipped_position=0", "unequipped_position=None").replace(
            "rings_position=None", "rings_position=0") == item_str2
    
    def test_replace_helmet(self):
        """Test if equipping second helmet replaces first."""

        template_helmet = self.db.session.query(
            Item).filter_by(name="Medium Helmet", template=True).first()
        item_helmet2 = template_helmet.build_new_from_template()

        self.inv.add_item(item_helmet2)
        inv_str = self.inv.pretty
        item2_str = item_helmet2.pretty
        
        self.inv.equip(item_helmet2)
        ids_to_unequip = self.inv.equip(item_helmet2)
        self.rebuild_instance()
        
        item2_str2 = self.inv.head.pretty
        inv_str2 = self.inv.pretty
        assert inv_str == inv_str2
            # .replace("helmet='<Item(id=2)>'", "helmet=None"
            # ).replace("helmet_item_id=2", "helmet_item_id=None"
            # ).replace("unequipped='[Item.id=1]'", "unequipped='[Item.id=1, Item.id=2]'")
        assert item2_str == item2_str2
            # .replace("inventory_helmet='<Inventory(id=2)>'", "inventory_helmet=None"
            # ).replace("inventory_unequipped=None", "inventory_unequipped='<Inventory(id=2)>'"
            # ).replace("unequipped_inventory_id=None", "unequipped_inventory_id=2"
            # ).replace("unequipped_position=0", "unequipped_position=1")
        assert ids_to_unequip == [1]
        
    # @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_replace_both_hands(self):
        polearm_template = self.db.session.query(Item).filter_by(name="Medium Polearm").first()
        shield_template = self.db.session.query(Item).filter_by(name="Small Shield").first()
        sword_template = self.db.session.query(Item).filter_by(name="Big Dagger").first()
        
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
        
    # @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_equip_lots_of_rings(self):
        template = self.db.session.query(Item).filter_by(name="Silver Ring").first()
        
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
        
    # @unittest.skip("Temporarily disabled for speed of developemnt -> renable before you trust :)")
    def test_unequip_legs(self):
        pants_template = self.db.session.query(Item).filter_by(name="Medium Pants").first()
        
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

    # @unittest.skip("Temporarily disabled for speed of development -> re-enable before you trust :)")
    def test_unequip_ring(self):
        template = self.db.session.query(Item).filter_by(name="Silver Ring").first()
        
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

import pytest
from pprint import pprint
import pdb
import re

from inventory import Inventory
from items import (Item, OneHandedWeapon, HeadArmour, TwoHandedWeapon, Ring,
                   Shield, LegArmour)

from test_setup import GenericTestCase

"""
Inventory: work in progress
Useful: 

PS> clear;pytest -x -vv -l -s
$ cls && pytest -x -vv -l -s

s - no output capture (shows print statement output)
x - exit after first failed test
v - verbose
vv - show full length output
l - show local vars during traceback (when a test fails)
"""


# @pytest.mark.skip("Some message ...")
@pytest.mark.incremental
class TestInventory(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()

        # Might be better for testing? To allow post mortem analysis.
        # db.engine.execute("SET FOREIGN_KEY_CHECKS = 0;")
        db.engine.execute("DROP TABLE `item`;")
        db.engine.execute("DROP TABLE `inventory`;")
        # db.engine.execute("SET FOREIGN_KEY_CHECKS = 0;")
        db = super().setup_class()

        inv = Inventory()
        db.session.add(inv)
        db.session.commit()

        # Add stock item/template combo - helmet/head armour.
        template = HeadArmour("Medium Helmet", 4, armour_value=3,
                              template=True)
        db.session.add(template)
        db.session.commit()
        item = template.build_new_from_template()
        db.session.add(template.build_new_from_template())
        db.session.commit()

        # Add second stock item/template combo - 2 handed weapon.
        template_2handed = TwoHandedWeapon(
            "Medium Polearm", buy_price=5, damage_minimum=30,
            damage_maximum=60, speed_speed=1, template=True)
        db.session.add(template_2handed)
        db.session.commit()
        item_2handed = template_2handed.build_new_from_template()
        db.session.add(item_2handed)
        db.session.commit()

        template_ring = Ring("Silver Ring", 8, template=True)
        db.session.add(template_ring)
        db.session.commit()
        item_ring = template_ring.build_new_from_template()
        db.session.add(item_ring)
        db.session.commit()

        template_shield = Shield("Small Shield", buy_price=10, template=True)
        db.session.add(template_shield)
        db.session.commit()
        db.session.add(template_shield.build_new_from_template())
        db.session.commit()

        template_sword = OneHandedWeapon(
            "Big Dagger", buy_price=10, damage_minimum=300, damage_maximum=600,
            speed_speed=2, template=True)
        db.session.add(template_sword)
        db.session.commit()
        template_sword.build_new_from_template()

        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)
        # db.engine.execute("DROP TABLE `item`;")

    def setup(self):
        super().setup()
        self.inv = self.db.session.query(Inventory).get(1)
        self.item_helmet = self.db.session.query(
            Item).filter_by(name="Medium Helmet", template=False).first()
        self.item_polearm = self.db.session.query(
            Item).filter_by(name="Medium Polearm", template=False).first()
        self.item_ring = self.db.session.query(
            Item).filter_by(name="Silver Ring", template=False).first()
        self.item_shield = self.db.session.query(
            Item).filter_by(name="Small Shield", template=False).first()
        self.item_sword = self.db.session.query(
            Item).filter_by(name="Big Dagger", template=False).first()

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
             "head=None", "head='<HeadArmour(id=2)>'").replace(
            "equipped=[]", "equipped='[<HeadArmour(id=2)>]'").replace(
            "unequipped='[<HeadArmour(id=2)>]'", "unequipped=[]") == inv_str2

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
            "both_hands=None", "both_hands='<TwoHandedWeapon(id=5)>'").replace(
            "equipped='[<HeadArmour(id=2)>]'",
            "equipped='[<HeadArmour(id=2)>, <TwoHandedWeapon(id=5)>]'").replace(
            "unequipped='[<TwoHandedWeapon(id=5)>]'", "unequipped=[]") == inv_str2
        assert item_str.replace(
            "equipped=False", "equipped=True").replace(
            "unequipped_position=0", "unequipped_position=None") == item_str2
            
    def test_equip_ring(self):
        """Test if rings can be equipped safely."""

        self.inv.add_item(self.item_ring)
        inv_str = self.inv.pretty
        item_str = self.item_ring.pretty

        ids_to_unequip = self.inv.equip(self.item_ring, 7)
        self.rebuild_instance()
        
        inv_str2 = self.inv.pretty
        item_str2 = self.inv.rings[7].pretty
        
        assert inv_str.replace(
            "rings={}", "rings='{7: <Ring(id=7)>}'").replace(
            "equipped='[<HeadArmour(id=2)>, <TwoHandedWeapon(id=5)>]'",
            "equipped='[<HeadArmour(id=2)>, <TwoHandedWeapon(id=5)>, <Ring(id=7)>]'"
        ).replace("unequipped='[<Ring(id=7)>]'", "unequipped=[]") == inv_str2

        assert item_str.replace(
            "equipped=False", "equipped=True").replace(
            "unequipped_position=0", "unequipped_position=None").replace(
            "ring_position=None", "ring_position=7") == item_str2
    
    def test_replace_helmet(self):
        """Test if equipping second helmet replaces first."""

        template_helmet = self.db.session.query(
            Item).filter_by(name="Medium Helmet", template=True).first()
        item_helmet2 = template_helmet.build_new_from_template()

        self.inv.add_item(item_helmet2)
        assert item_helmet2.unequipped_position == 0
        inv_str = self.inv.pretty
        item2_str = item_helmet2.pretty
        
        ids_to_unequip = self.inv.equip(item_helmet2)
        assert item_helmet2.unequipped_position is None
        assert self.inv.unequipped[0].unequipped_position == 0
        self.rebuild_instance()
        
        item2_str2 = self.inv.head.pretty
        inv_str2 = self.inv.pretty
        assert inv_str.replace(
            "equipped='[<HeadArmour(id=2)>, <TwoHandedWeapon(id=5)>, <Ring(id=7)>]'",
            "equipped='[<TwoHandedWeapon(id=5)>, <Ring(id=7)>, <HeadArmour(id=12)>]'"
        ).replace(
            "head='<HeadArmour(id=2)>'", "head='<HeadArmour(id=12)>'"
        ).replace(
            "unequipped='[<HeadArmour(id=12)>]'",
            "unequipped='[<HeadArmour(id=2)>]'") == inv_str2
        assert item2_str.replace(
            "equipped=False", "equipped=True").replace(
            "unequipped_position=0", "unequipped_position=None") == item2_str2

        assert ids_to_unequip == [2]
        
    def test_replace_both_hands(self):
        """See if equip code can handle multiple replacement."""

        shield = self.item_shield
        sword = self.item_sword
        polearm = self.item_polearm
        self.inv.add_item(shield)
        self.inv.add_item(sword)

        self.inv.equip(sword)
        self.inv.equip(shield)
        inv_str = self.inv.pretty
        polearm_str = polearm.pretty       
        
        ids_to_unequip = self.inv.equip(polearm)
        self.rebuild_instance()
        
        polearm2_str = self.inv.both_hands.pretty
        inv_str2 = self.inv.pretty
        assert inv_str.replace(
            "both_hands=None", "both_hands='<TwoHandedWeapon(id=5)>'"
        ).replace(
            "equipped='[<Ring(id=7)>, <Shield(id=9)>, <OneHandedWeapon(id=11)>, "
            "<HeadArmour(id=12)>]'",
            "equipped='[<TwoHandedWeapon(id=5)>, <Ring(id=7)>, "
            "<HeadArmour(id=12)>]'"
        ).replace(
            "left_hand='<Shield(id=9)>'", "left_hand=None"
        ).replace(
            "right_hand='<OneHandedWeapon(id=11)>'", "right_hand=None"
        ).replace(
            "unequipped='[<HeadArmour(id=2)>, <TwoHandedWeapon(id=5)>]'",
            "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, "
            "<OneHandedWeapon(id=11)>]'") == inv_str2
        assert ids_to_unequip == [9, 11]
        
    def test_equip_lots_of_rings(self):
        """Equip lots of rings ... see if that breaks anything :P"""

        # I'm getting some bugs ... maybe a clean slate will help?
        template_ring = self.db.session.query(
            Item).filter_by(name="Silver Ring", template=True).first()

        str_inv = self.inv.pretty
        ids_to_unequip = []
        for i in range(12):
            item = self.db.create_item(template_ring.id)
            try:
                self.inv.equip(item, i)
            except IndexError as ex:
                assert i >= 10
                assert str(ex) == "'Ring' index out of range. Index must be " \
                                  "from 0 to 9."
            if i == 0:
                assert str_inv.replace(
                    "equipped='[<TwoHandedWeapon(id=5)>, <Ring(id=7)>, "
                    "<HeadArmour(id=12)>]'",
                    "equipped='[<TwoHandedWeapon(id=5)>, <Ring(id=7)>, "
                    "<HeadArmour(id=12)>, <Ring(id=13)>]'"
                ).replace(
                    "rings='{7: <Ring(id=7)>}'",
                    "rings='{0: <Ring(id=13)>, 7: <Ring(id=7)>}'"
                ).replace(
                    "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, "
                    "<OneHandedWeapon(id=11)>, <Ring(id=7)>]'",
                    "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, "
                    "<OneHandedWeapon(id=11)>]'") == self.inv.pretty

        str_inv2 = self.inv.pretty
        assert str_inv.replace(
            "equipped='[<TwoHandedWeapon(id=5)>, <Ring(id=7)>, <HeadArmour(id=12)>]'",
            "equipped='[<TwoHandedWeapon(id=5)>, <HeadArmour(id=12)>, <Ring(id=13)>, <Ring(id=14)>, <Ring(id=15)>, <Ring(id=16)>, <Ring(id=17)>, <Ring(id=18)>, <Ring(id=19)>, <Ring(id=20)>, <Ring(id=21)>, <Ring(id=22)>]'"
        ).replace(
            "rings='{7: <Ring(id=7)>}'",
            "rings='{0: <Ring(id=13)>, 1: <Ring(id=14)>, 2: <Ring(id=15)>, 3: <Ring(id=16)>, 4: <Ring(id=17)>, 5: <Ring(id=18)>, 6: <Ring(id=19)>, 7: <Ring(id=20)>, 8: <Ring(id=21)>, 9: <Ring(id=22)>}'"
        ).replace(
            "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, <OneHandedWeapon(id=11)>]'",
            "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, <OneHandedWeapon(id=11)>, <Ring(id=7)>, <Ring(id=23)>, <Ring(id=24)>]'"
        ) == str_inv2

        silver_ring7 = self.inv.unequipped[3]
        assert silver_ring7.type == "Ring"
        assert silver_ring7.id == 7
        assert self.inv.rings[4].id == 17
        ids_to_unequip = self.inv.equip(silver_ring7, 4)
        
        self.rebuild_instance()
        
        str_inv3 = self.inv.pretty
        assert str_inv2.replace(
            "equipped='[<TwoHandedWeapon(id=5)>, <HeadArmour(id=12)>, <Ring(id=13)>, <Ring(id=14)>, <Ring(id=15)>, <Ring(id=16)>, <Ring(id=17)>, <Ring(id=18)>, <Ring(id=19)>, <Ring(id=20)>, <Ring(id=21)>, <Ring(id=22)>]'",
            "equipped='[<TwoHandedWeapon(id=5)>, <Ring(id=7)>, <HeadArmour(id=12)>, <Ring(id=13)>, <Ring(id=14)>, <Ring(id=15)>, <Ring(id=16)>, <Ring(id=18)>, <Ring(id=19)>, <Ring(id=20)>, <Ring(id=21)>, <Ring(id=22)>]'"
        ).replace(
            "rings='{0: <Ring(id=13)>, 1: <Ring(id=14)>, 2: <Ring(id=15)>, 3: <Ring(id=16)>, 4: <Ring(id=17)>, 5: <Ring(id=18)>, 6: <Ring(id=19)>, 7: <Ring(id=20)>, 8: <Ring(id=21)>, 9: <Ring(id=22)>}'",
            "rings='{0: <Ring(id=13)>, 1: <Ring(id=14)>, 2: <Ring(id=15)>, 3: <Ring(id=16)>, 4: <Ring(id=7)>, 5: <Ring(id=18)>, 6: <Ring(id=19)>, 7: <Ring(id=20)>, 8: <Ring(id=21)>, 9: <Ring(id=22)>}'"
        ).replace(
            "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, <OneHandedWeapon(id=11)>, <Ring(id=7)>, <Ring(id=23)>, <Ring(id=24)>]'",
            "unequipped='[<HeadArmour(id=2)>, <Shield(id=9)>, <OneHandedWeapon(id=11)>, <Ring(id=23)>, <Ring(id=24)>, <Ring(id=17)>]'"
        ) == str_inv3
        assert ids_to_unequip == [17]
        
    def test_unequip_legs(self):
        """See if you can unequip some pants!"""
        pants_template = LegArmour("Medium Pants", 7, armour_value=25,
                                   template=True)
        self.db.session.add(pants_template)
        self.db.session.commit()
        pants = self.db.create_item(pants_template.id)
        self.inv._clear_inventory()

        self.inv.add_item(pants)
        
        self.inv.equip(pants)
        self.rebuild_instance()
        
        str_inv = self.inv.pretty
        str_pants = self.inv.leg.pretty
        
        self.inv.unequip(self.inv.leg)
        self.rebuild_instance()
        
        str_inv2 = self.inv.pretty
        str_pants2 = self.inv.unequipped[0].pretty
        assert str_inv.replace(
            "equipped='[<LegArmour(id=26)>]'", "equipped=[]").replace(
            "leg='<LegArmour(id=26)>'", "leg=None").replace(
            "unequipped=[]", "unequipped='[<LegArmour(id=26)>]'") == str_inv2
        assert str_pants.replace(
            "equipped=True", "equipped=False").replace(
            "unequipped_position=None", "unequipped_position=0") == str_pants2

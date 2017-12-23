from locations import Location
from abilities import Ability
from game import User, Hero
from quests import Quest, QuestPath
from items import (
    OneHandedWeapon, Shield, TwoHandedWeapon, LegArmour, ChestArmour,
    HeadArmour, FeetArmour, ArmArmour, HandArmour, Ring, Consumable
)
from events import Trigger, Condition

"""
This module preloads all of its objects directly into the database or does
nothing if the objects already exists in the database.

All access to these objects occurs through the database interface directly.

I am currently in the process of switching to a game editor approach
which loads these object from a .csv file.
"""

# ------------------------------------
#
#  Initializing Game Worlds
#  (To be moved to a common
#   init function later)
#
# ------------------------------------

'''
 +Test Map Visual Representation:
 +
 +0 ---- 1 ---- 2 (Creepy Cave)
 +| \    |
 +|  \   |
 +|   \  |
 +3    \ |
 +|     5 ---- 6 ---- 7
 +|    / \     |
 +4   /   \    |
 +   /     \   |
 +  /       \  |
 + /         \ |
 +8           9
 +
 +
 +Thornwall at location 5
 +Creepy Cave at location 2
 +'''
world = Location(name="Htrae", location_type="map")
world.display.page_heading = "You are wandering in the world"
world.display.paragraph = "Be safe"

node_grid = []
for i in range(0, 12):
    node_grid.append(
        Location(name="Location{}".format(i),
                 location_type='explorable'))
world.children = node_grid

town = node_grid[5]
town.name = "Thornwall"
town.type = 'town'
town.update()

"""
town.display.places_of_interest=[
("/store/greeting", "Blacksmith", "Shops"),
("/barracks", "Barracks"),
("/marketplace/greeting", "Marketplace"),
("/tavern", "Tavern", "Other"),
("/old_mans_hut", "Old Man's Hut"),
("/leave_town", "Village Gate", "Outskirts"),
("/WorldMap/{}/{}".format(town.location_world.name, town.id), "World Map")
]
"""
blacksmith = Location('Blacksmith', 'store')
blacksmith.children.append(Location('armoury', 'store'))
blacksmith.children.append(Location('weaponry', 'store'))
marketplace = Location('Marketplace', 'marketplace')
marketplace.children.append(Location('general', 'marketplace'))
tavern = Location("Red Dragon Inn", 'tavern')

barracks = Location('Barracks', 'barracks')
spar = Location('Spar', 'spar')
spar.display.page_title = "Sparring Room"
barracks.children.append(spar)
barracks.children.append(Location('Arena', 'arena'))

town.children.append(blacksmith)
town.children.append(barracks)
town.children.append(marketplace)
town.children.append(tavern)

old_mans_hut = Location("Old Man's Hut", 'house')
old_mans_hut.display.page_heading = "Old Man's Hut"
old_mans_hut.display.page_image = 'hut.jpeg'
old_mans_hut.display.paragraph = "Nice to see you again kid. What do you need?"
old_mans_hut.update()
town.children.append(old_mans_hut)

gate = Location('Village Gate', 'gate')
town.children.append(gate)

cave = node_grid[2]
cave.name = "Entrance to Creepy cave"
cave.type = 'cave'
cave.display.page_heading = "You are in a cave called {}".format(cave.name)
cave.page_image = "cave_entrance.jpg"
cave.display.paragraph = "There are many scary places to die within the cave. Have a look!"
cave.update()

cave_entrance = Location('Cave Entrance', 'cave_entrance')
cave_entrance.page_image = "cave.jpg"
explore_cave = Location('Explore Cave', 'explore_cave')
explore_cave.display.page_title = "Exploring"
cave_entrance.children.append(explore_cave)

cave.children.append(cave_entrance)


node_grid[0].adjacent = [node_grid[1], node_grid[3], node_grid[5]]
node_grid[1].adjacent = [node_grid[0], node_grid[2], node_grid[5]]
node_grid[2].adjacent = [node_grid[1]]
node_grid[3].adjacent = [node_grid[0], node_grid[4]]
node_grid[4].adjacent = [node_grid[3]]
node_grid[5].adjacent = [node_grid[0], node_grid[1], node_grid[6],
                         node_grid[8], node_grid[9]]
node_grid[6].adjacent = [node_grid[5], node_grid[7], node_grid[9]]
node_grid[7].adjacent = [node_grid[6]]
node_grid[8].adjacent = [node_grid[5]]
node_grid[9].adjacent = [node_grid[5], node_grid[6]]
node_grid[10].adjacent = []

current_location = town
game_worlds = [world]  # Just chop this out and use world instead.

# game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
# game_worlds = [World_Map("Test_World", TEST_WORLD_ID, test_locations)]

# game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]

#########
# Conditions
#########
blacksmith_condition = Condition('current_location', '==', blacksmith)
blacksmith_is_parent_of_current_location_condition \
    = Condition('current_location.parent', '==', blacksmith)



##########
# Triggers
##########
visit_blacksmith_trigger = Trigger(
    'move_event', conditions=[blacksmith_condition],
    extra_info_for_humans='Should activate when '
                          'the hero.current_location.id == the id of the '
                          'blacksmith object.')

buy_item_from_blacksmith_trigger = Trigger(
    'buy_event',
    conditions=[blacksmith_is_parent_of_current_location_condition],
    extra_info_for_humans='Should activate when buy code runs and '
                          'hero.current_location.id == id of the blacksmith.'
)

equip_item_trigger = Trigger(
    'equip_event',
    conditions=[],
    extra_info_for_humans="Should activate when equip_event spawns."
)

unequip_item_trigger = Trigger(
    'unequip_event',
    conditions=[],
    extra_info_for_humans="Should activate when unequip_event spawns."
)


###########
# Quests
##########
blacksmith_quest_stage1 = Quest(
    "Go talk to the blacksmith",
    "Find the blacksmith in Thornwall and enter his shop.",
    trigger=visit_blacksmith_trigger
)

blacksmith_quest_stage2 = Quest(
    "Buy your first item",
    "Buy any item from the blacksmith.",
    reward_experience=4,
    trigger=buy_item_from_blacksmith_trigger
)

inventory_quest_stage1 = Quest(
    "Equip an item",
    "Equip any item in your inventory.",
    trigger=equip_item_trigger
)

inventory_quest_stage2 = Quest(
    "Unequip an item",
    "Unequip any item in your inventory.",
    trigger=unequip_item_trigger
)

# tavern = Quest("Become an apprentice at the tavern", "Ask if there are any jobs you can do.")
# tavern.next_quests.append("Become an apprentice at the tavern", "Collect 2 Wolf Pelts for the Bartender")

# tavern.next_quests.append("Become an apprentice at the tavern", "Find two copper coins and give them to the blacksmith")

# tavern.next_quests.append("Become an apprentice at the tavern", "Give the bartender 2 copper coins.")

all_quests = [blacksmith_quest_stage1, blacksmith_quest_stage2,
              inventory_quest_stage1, inventory_quest_stage2]

meet_the_blacksmith_path = QuestPath(
    "Get Acquainted with the Blacksmith",
    "Find the blacksmith and buy something from him.",
    quests=[blacksmith_quest_stage1, blacksmith_quest_stage2]
)

learn_about_your_inventory_path = QuestPath(
    "Learn how your inventory works",
    "Practice equipping an unequipping.",
    quests=[inventory_quest_stage1, inventory_quest_stage2]
)

default_quest_paths = [
    meet_the_blacksmith_path, learn_about_your_inventory_path
]

##########
# Users (and heroes)
"""
NOTE: password is set as plaintext here. It must (and currently is) hashed in database.py
when prebuilt_objects are preloaded into the database.
"""
##########
admin = User(username="admin", password="admin", is_admin=True)
adminHero = Hero(name="Admin", fathers_job="Priest", current_world=world, current_location=town, gold=5000)
admin.heroes = [adminHero]

marlen = User(username="marlen", password="brunner", is_admin=True)
haldon = Hero(name="Haldon", fathers_job="Priest", current_world=world, current_location=town, gold=5000)
marlen.heroes = [haldon]
users = [marlen, admin]

##########
# Items
##########
all_store_items = [
    LegArmour("Medium Pants", 7, health_maximum=25),
    ChestArmour("Medium Tunic", 2, armour_value=25),
    ChestArmour("Strong Tunic", 5, armour_value=250),
    HeadArmour("Weak Helmet", 2, armour_value=1),
    HeadArmour("Medium Helmet", 4, armour_value=3),
    FeetArmour("Light Boots", 3, armour_value=3),
    ArmArmour("Light Sleeves", 4, armour_value=5),
    HandArmour("Light Gloves", 5, armour_value=7),
    Ring("Silver Ring", 8),
    TwoHandedWeapon("Medium Polearm", buy_price=5, damage_minimum=30,
                    damage_maximum=60, speed_speed=1),
    TwoHandedWeapon("Small Polearm", buy_price=5, damage_minimum=30,
                    damage_maximum=60, speed_speed=1),
    Shield("Small Shield", buy_price=10),
    OneHandedWeapon("Big Dagger", buy_price=10,
                    damage_minimum=300, damage_maximum=600, speed_speed=2),
    OneHandedWeapon("Small Dagger", buy_price=5,
                    damage_minimum=30, damage_maximum=60, speed_speed=1),
    OneHandedWeapon("Poisoned Dagger", buy_price=5,
                    damage_minimum=2, damage_maximum=10, damage_modifier=1,
                    resist_poison_modifier=25),
    Shield("Ice Buckler", buy_price=100, max_durability=3,
           damage_minimum=2, damage_maximum=10, damage_modifier=1,
           block_chance=50, block_modifier=50,
           resist_frost_modifier=30),
    TwoHandedWeapon("Simple Staff", buy_price=100, max_durability=3,
                    damage_minimum=2, damage_maximum=10, damage_modifier=1)
    ]

all_marketplace_items = [
    Consumable("Minor Health Potion", 3, healing_amount=10),
    Consumable("Major Health Potion", 6, healing_amount=50),
    Consumable("Major Faith Potion", 6, sanctity_amount=50),
    Consumable("Major Awesome Max Potion", 6000, sanctity_amount=50)
]

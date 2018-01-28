from locations import Location
from abilities import Ability
from specializations import ArchetypeSpecialization
from game import User
from hero import Hero
from quests import Quest, QuestPath
from items import (
    OneHandedWeapon, Shield, TwoHandedWeapon, LegArmour, ChestArmour,
    HeadArmour, FootArmour, ArmArmour, HandArmour, Ring, Consumable
)
from events import Trigger, Condition
from random import choice # To create pre-built adjectives
from forum import Forum, Thread, Post

# for testing
import pdb

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
 Haunted Forest at 8
 Old Man's Hut at 7
 +'''

adjective_list = ["Dark", "Creepy", "Shadowy", "Haunted", "Sacred"]

starting_world = Location(name="Htrae", location_type="map")
starting_world.display.page_heading = "You are wandering in the world"
starting_world.page_heading = "You are looking at the world map."
starting_world.display.paragraph = "Be safe"
starting_world.display.page_image = "htrae.jpg"

node_grid = []
for i in range(0, 12):
    node_grid.append(
        Location(name="Location{}".format(i),
                 location_type='explorable'))
starting_world.children = node_grid

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

old_mans_hut = node_grid[7]
old_mans_hut.name = "Old Man's Hut"
old_mans_hut.type = 'building'
old_mans_hut.update()
old_mans_hut.display.page_heading = "Old Man's Hut"
old_mans_hut.display.page_image = 'hut.jpg'
old_mans_hut.display.paragraph = "Nice to see you again kid. What do you need?"

gate = Location('Village Gate', 'gate')
town.children.append(gate)

# Child of Dungeon Entrance
explore_dungeon = Location('Explore Dungeon', 'explore_dungeon')
explore_dungeon.display.page_title = "Exploring"

# Child of all "type == dungeon": Cave/Forest/etc.
dungeon_entrance = Location('Dungeon Entrance', 'dungeon_entrance')
dungeon_entrance.display.page_image = "generic_cave_entrance2.jpg"
dungeon_entrance.children.append(explore_dungeon)

cave = node_grid[2]
cave.name = choice(adjective_list) + " Cave"
cave.type = 'dungeon'
cave.update()
cave.display.page_heading = "You are outside {}".format(cave.name)
cave.display.page_image = "generic_cave_entrance.jpg"
cave.display.paragraph = "There are many scary places to die within the cave. Have a look!"
cave.children.append(dungeon_entrance)

forest = node_grid[8]
forest.name = choice(adjective_list) + " Forest"
forest.type = 'dungeon'
forest.update()
forest.display.page_heading = "You are outside {}".format(forest.name)
forest.display.page_image = "generic_forest_entrance.jpg"
forest.display.paragraph = "There are many scary places to die within the forest. Have a look!"
forest.children.append(dungeon_entrance)

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
game_worlds = [starting_world]  # Just chop this out and use world instead.

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
    quests=[inventory_quest_stage1, inventory_quest_stage2],
    is_default=True
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
admin.prestige = 371
adminHero = Hero(name="Admin", fathers_job="Priest", current_world=starting_world, current_location=town, gold=5000)
admin.heroes = [adminHero]

marlen = User(username="marlen", password="brunner", is_admin=True)
marlen.prestige = 309
haldon = Hero(name="Haldon", fathers_job="Priest", current_world=starting_world, current_location=town, gold=5000)
marlen.heroes = [haldon]
users = [marlen, admin]

##########
# Items
##########
all_store_items = [
    LegArmour("Medium Pants", 7, armour_value=25),
    ChestArmour("Medium Tunic", 2, armour_value=25),
    ChestArmour("Strong Tunic", 5, armour_value=250),
    HeadArmour("Weak Helmet", 2, armour_value=1),
    HeadArmour("Medium Helmet", 4, armour_value=3),
    FootArmour("Light Boots", 3, armour_value=3),
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
    Shield("Rare Fire Buckler", buy_price=100, max_durability=3,
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

all_specializations = [
    ArchetypeSpecialization('Brute', 
                            'A character who uses strength and combat to solve problems.  Proficient with many types of weapons.',
        'Brawn of 6, Any Weapon Talent ~ 10'),
    ArchetypeSpecialization('Scoundrel', 
                            'A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.', 
                            'Dagger Talent of 6, Virtue of -100'),
    ArchetypeSpecialization('Ascetic', 
                            'A character who focuses on disciplining mind and body. They use a combination of combat and intellect.', 
                            '10 Errands Complete, Virtue of 100, Willpower of 4'),
    ArchetypeSpecialization('Survivalist', 
                            'A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.', 
                            '5 Locations Discovered, 10 Animals in Bestiary'),
    ArchetypeSpecialization('Philosopher', 
                            'A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.', 
                            'Intellect of 7, Books Read of 10'),
    ArchetypeSpecialization('Opportunist', 
                            'A character who solves problems using speech and dialogue.', 
                            'Charisma of 7, Fame of 200')
]

testing_forum = Forum()

sample_thread = Thread("General Discussion", "Elthran")
testing_forum.create_thread(sample_thread)

first_post = Post("testing post, please ignore")
sample_thread.write_post(first_post)
from locations import Location
import specializations
from game import User
from hero import Hero
from quests import Quest, QuestPath
from items import (
    OneHandedWeapon, Shield, TwoHandedWeapon, LegArmour, ChestArmour,
    HeadArmour, FootArmour, ArmArmour, HandArmour, Ring, Consumable
)
from events import Trigger, Condition
from random import choice # To create pre-built adjectives
from forum import Forum, Board

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

"""
Nodes used:
    5 - Thornwall (town)
    7 - Old Man's Hut (building)
    2 - Cave (dungeon)
    8 - Forest (dungeon)
    4 - Outpost (town)
"""

node_grid = []
for i in range(0, 12):
    node_grid.append(
        Location(name="Location{}".format(i),
                 location_type='explorable'))
starting_world.children = node_grid

town = node_grid[5]
town.name = "Thornwall"
town.type = 'town'
town.terrain = 'city'
town.update()

town2 = node_grid[4]
town2.name = "Outpost"
town2.type = 'town'
town2.terrain = 'city'
town2.update()

"""
town.display.places_of_interest=[
("/town/blacksmith", "Blacksmith", "Shops"),
("/barracks", "Barracks"),
("/marketplace/greeting", "Marketplace"),
("/tavern", "Tavern", "Other"),
("/old_mans_hut", "Old Man's Hut"),
("/leave_town", "Village Gate", "Outskirts"),
("/WorldMap/{}/{}".format(town.location_world.name, town.id), "World Map")
]
"""

# Town's children
blacksmith = Location('Blacksmith', 'store')
marketplace = Location('Marketplace', 'store')
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

# Outpost's children
marketplace2 = Location('Marketplace2', 'store')
town2.children.append(marketplace2)

old_mans_hut = node_grid[7]
old_mans_hut.name = "Old Man's Hut"
old_mans_hut.type = 'building'
old_mans_hut.update()
old_mans_hut.display.page_heading = "Old Man's Hut"
old_mans_hut.display.page_image = 'hut.jpg'
old_mans_hut.display.paragraph = "Nice to see you again kid. What do you need?"

gate = Location('Village Gate', 'gate')
town.children.append(gate)

NUM_OF_DUNGEONS = 2
# Child of Dungeon Entrance
explorable_dungeons = []
for n in range(NUM_OF_DUNGEONS):
    explorable_dungeon = Location('Explore Dungeon{}'.format(n), 'explore_dungeon')
    explorable_dungeon.display.page_title = "Exploring"
    explorable_dungeons.append(explorable_dungeon)


# Child of all "type == dungeon": Cave/Forest/etc.
dungeon_entrances = []
for n in range(NUM_OF_DUNGEONS):
    dungeon_entrance = Location('Dungeon Entrance{}'.format(n), 'dungeon_entrance')
    dungeon_entrance.display.page_heading = "You are in the dungeon and exploring!"
    dungeon_entrance.display.page_image = "generic_cave_entrance2.jpg"
    dungeon_entrance.display.paragraph = "Take a step into the dungeon."
    dungeon_entrance.children.append(explorable_dungeons[n])
    dungeon_entrances.append(dungeon_entrance)

cave = node_grid[2]
cave.name = choice(adjective_list) + " Cave"
cave.type = 'dungeon'
cave.terrain = 'cave'
cave.update()
cave.display.page_heading = "You are outside {}".format(cave.name)
cave.display.page_image = "generic_cave_entrance.jpg"
cave.display.paragraph = "There are many scary places to die within the cave. Have a look!"
cave.children.append(dungeon_entrances[0])

forest = node_grid[8]
forest.name = choice(adjective_list) + " Forest"
forest.type = 'dungeon'
forest.terrain = 'forest'
forest.update()
forest.display.page_heading = "You are outside {}".format(forest.name)
forest.display.page_image = "generic_forest_entrance.jpg"
forest.display.paragraph = "There are many scary places to die within the forest. Have a look!"
forest.children.append(dungeon_entrances[1])

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
    conditions=[blacksmith_condition],
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
admin.signature = "I am admin."
adminHero = Hero(name="Gnahz", fathers_job="Priest", current_world=starting_world, current_location=town, gold=5000)
admin.heroes = [adminHero]

marlen = User(username="marlen", password="brunner", is_admin=True)
marlen.signature = "Insert some joke about Haldon here."
haldon = Hero(name="Haldon", fathers_job="Priest", current_world=starting_world, current_location=town, gold=5000)
marlen.heroes = [haldon]

elthran = User(username="elthran", password="brunner", is_admin=True)
elthranHero = Hero(name="Elthran", fathers_job="Priest", current_world=starting_world, current_location=town, gold=5000)
elthran.heroes = [elthranHero]

users = [elthran, marlen, admin]
for user in users:
    user.prestige = 50

##########
# Items
##########
all_store_items = [
    ChestArmour("Cloth Tunic", buy_price=18, description="A simple cloth tunic.", template=True,
                proficiency_data=[
                    ('Defence', {'base': 5})]),
    TwoHandedWeapon("Gnarled Staff", buy_price=13, description="An old, simple walking stick.", template=True, damage_type='Blunt',
                    proficiency_data=[
                        ('Strength', {'base': 15}),
                        ('Combat', {'modifier': 10})]),
    Shield("Small Shield", buy_price=25, description="A simple wooden shield.", template=True,
           proficiency_data=[
                ('Block', {'base': 25}),
                ('BlockAmount', {'base': 15})]),
    OneHandedWeapon("Rusted Dagger", buy_price=23, description="A rusted dagger in poor condition.", template=True, damage_type='Piercing',
                    proficiency_data=[
                        ('Strength', {'base': 5}),
                        ('Speed', {'base': 0.5})]),
    Ring("Silver Ring", buy_price=35, description="A silver ring with no markings. Nothing seems special about it.", template=True, style="silver",
                    proficiency_data=[
                        ('Luck', {'base': 1})])
    ]

all_marketplace_items = [
    Consumable("Minor Health Potion", 3,
               proficiency_data=[('Health', {'base': 10})], template=True),
    Consumable("Major Health Potion", 6,
               proficiency_data=[('Health', {'base': 50})], template=True),
    Consumable("Major Faith Potion", 6,
               proficiency_data=[('Sanctity', {'base': 50})], template=True),
    Consumable("Major Awesome Max Potion", 6000,
               proficiency_data=[('Sanctity', {'base': 50})],
               template=True)
]

all_specializations = [getattr(specializations, cls_name)(template=True)
                       for cls_name in specializations.ALL_CLASS_NAMES]


basic_forum = Forum("Basic")  # Create the first forum
all_forums = [basic_forum]  # Add it to the list of forums to be generated on game init
basic_forum.create_board(Board("General"))  # Add a board to the forum so it doesn't seem so lonely

game_monsters = [Hero(name="Sewer Rat", species="Rat", level_max=10, forest=False, city=True),
                 Hero(name="Giant Spider", species="Spider", level_max=10, forest=True, city=False),
                 Hero(name="Rabid Dog", species="Dog", level_max=10, forest=False, city=True)]

for i in range(len(game_monsters)):
    game_monsters[i].is_monster = True
    game_monsters[i].monster_id = i+1
    if game_monsters[i].species == "Rat":
        game_monsters[i].species_plural = "Rats"
        game_monsters[i].base_proficiencies.poison_chance.base = 15
        game_monsters[i].base_proficiencies.poison_duration.base = 4
        game_monsters[i].base_proficiencies.poison_amount.base = 2
    if game_monsters[i].species == "Spider":
        game_monsters[i].species_plural = "Spiders"
        game_monsters[i].base_proficiencies.poison_chance.base = 35
        game_monsters[i].base_proficiencies.poison_duration.base = 3
        game_monsters[i].base_proficiencies.poison_amount.base = 1
    if game_monsters[i].species == "Dog":
        game_monsters[i].species_plural = "Dogs"
        game_monsters[i].base_proficiencies.health.current += 5
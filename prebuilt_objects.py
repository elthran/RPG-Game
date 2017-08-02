from locations import Location
from abilities import Ability, Archetype_Ability, Class_Ability, Religious_Ability
from game import User, Hero
from quests import Quest, QuestPath
from items import (
    One_Handed_Weapon, Shield, Two_Handed_Weapon, Leg_Armour, Chest_Armour,
    Head_Armour, Feet_Armour, Arm_Armour, Hand_Armour, Ring, Consumable
)

# MUST be imported last.
import complex_relationships

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
cave.name = "Creepy cave"
cave.type = 'cave'
cave.display.page_heading = "You are in a cave called {}".format(cave.name)
cave.display.paragraph = "There are many scary places to die within the " \
                         "cave. Have a look!"
cave.update()
"""
cave.display.places_of_interest=[
("/WorldMap/{}/{}".format(cave.location_world.name, cave.id), "World Map")])
"""

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

##########
#Abilities
##########
all_abilities = [Ability("Determination", 5, "Increases Endurance by 3 for each level."),
    Ability("Salubrity", 5, "Increases Health by 4 for each level."),
    Ability("Gain Gold to Test", 5, "Gain 3 gold for each level, every time you actvate this ability.",
        castable=True, cost=2),
    Archetype_Ability("Survivalism", 10, "Increases survivalism by 1 for each level.", archetype="Woodsman"),
    Archetype_Ability("Piety", 10, "Increases divinity by 1 for each level.", archetype="Priest"),
    Archetype_Ability("Sagacious", 10, "Increases experience gained by 5% for each level."),
    Class_Ability("Panther Aspect", 10, "Increases evade chance by 1% for each level.",
        specialization="Hunter"),
    Class_Ability("Camouflage", 10, "Increases stealth by 1% for each level.", specialization="Trapper"),
    Class_Ability("Luck", 10, "Increases luck by 2 for each level."),
    Religious_Ability("Iron Bark", 10, "Increases defence by 2% for each level.", religion="Dryarch"),
    Religious_Ability("Wreath of Flames", 10, "Increases fire damage by 3 for each level.",
        religion="Forgoth"),
    Religious_Ability("Blessed", 10, "Increases devotion by 5 for each level.")]

###########
#Quests
##########
blacksmith_quest = Quest("Get Acquainted with the Blacksmith", "Go talk to the blacksmith.")
blacksmith_quest.next_quests.append(Quest("Get Acquainted with the Blacksmith", "Buy your first item.", reward_experience=7))

equipment_quest = Quest("Equipping/Unequipping", "Equip any item.")
equipment_quest.next_quests.append(Quest("Equipping/Unequipping", "Unequip any item."))

# tavern = Quest("Become an apprentice at the tavern", "Ask if there are any jobs you can do.")
# tavern.next_quests.append("Become an apprentice at the tavern", "Collect 2 Wolf Pelts for the Bartender")

# tavern.next_quests.append("Become an apprentice at the tavern", "Find two copper coins and give them to the blacksmith")

# tavern.next_quests.append("Become an apprentice at the tavern", "Give the bartender 2 copper coins.")
        
all_quests = [blacksmith_quest, equipment_quest] #Which is really 4 quests.

##########
#Users (and heroes)
"""
NOTE: password is set as plaintext here. It must (and currently is) hashed in database.py
when prebuilt_objects are preloaded into the database.
"""
##########
admin = User(username="admin", password="admin", is_admin=True)
adminHero = Hero(name="Admin", fathers_job="Priest", current_world=world, current_location=town, gold = 5000)
admin.heroes = [adminHero]
marlen = User(username="marlen", password="brunner", is_admin=True)
haldon = Hero(name="Haldon", fathers_job="Priest", current_world=world, current_location=town, gold = 5000)
QuestPath(blacksmith_quest, haldon) # What are these?
QuestPath(equipment_quest, haldon)  # ///
marlen.heroes = [haldon]
users = [marlen, admin]

##########
#Items
##########
all_store_items = [One_Handed_Weapon("Small Dagger", buy_price=5, min_damage=30,
        max_damage=60, attack_speed=1),
    One_Handed_Weapon("Big Dagger", buy_price=10, min_damage=300, max_damage=600,
        attack_speed=2),
    Shield("Small Shield", buy_price=10),
    Two_Handed_Weapon("Small Polearm", buy_price=5, min_damage=30, max_damage=60,
        attack_speed=1),
    Two_Handed_Weapon("Medium Polearm", buy_price=5, min_damage=30, max_damage=60,
        attack_speed=1),
    Leg_Armour("Medium Pants", 7, 25),
    Chest_Armour("Medium Tunic", 2, 25),
    Chest_Armour("Strong Tunic", 5, 250),
    Head_Armour("Weak Helmet", 2, 1),
    Head_Armour("Medium Helmet", 4, 3),
    Feet_Armour("Light Boots", 3, 3),
    Arm_Armour("Light Sleeves", 4, 5),
    Hand_Armour("Light Gloves", 5, 7),
    Ring("Silver Ring", 8),
    Shield("Wooden Buckler", buy_price=5)
                   ]

all_marketplace_items = [
    Consumable("Minor Health Potion", 3, healing_amount=10),
    Consumable("Major Health Potion", 6, healing_amount=50),
    Consumable("Major Faith Potion", 6, sanctity_amount=50),
    Consumable("Major Awesome Max Potion", 6000, sanctity_amount=50)
    ]

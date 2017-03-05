from locations import Location, Cave, Town, WorldMap, Display
from abilities import Ability, Archetype_Ability, Class_Ability, Religious_Ability
from game import User, Hero
from quests import Quest
import complex_relationships #MUST be imported last.

"""
Consider having this class preload all of its objects directly into the database or doing nothing
if the objects already exists in the database. Then all access to these object would
occur through the database interface directly.
"""

#------------------------------------
 #
 #  Initializing Game Worlds
 #  (To be moved to a common
 #   init function later)
 #
 #------------------------------------

test_locations = []
test_locations2 = []

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
 
for i in range(0, 12):
    test_location = Location(name=("location " + str(i)),id=i)
    test_locations2.append(test_location)

test_locations2[5] = Town(name="Thornwall", id=5)
town = test_locations2[5]
test_locations2[2] = Cave(name="Creepy cave", id=2)
cave = test_locations2[2]

""" Define all connections

#------------------------------------
#
#  Initializing Game Worlds
#  (To be moved to a common
#   init function later)
#
#------------------------------------
TEST_WORLD_ID = 999 # ...

test_locations = []

'''
Test Map Visual Representation:

0 ---- 1 ---- 2 (Creepy Cave)
| \    |
|  \   |
|   \  |
3    \ |
|     5 ---- 6 ---- 7
|    / \     |
4   /   \    |
   /     \   |
  /       \  |
 /         \ |
8           9


Thornwall at location 5
Creepy Cave at location 2
'''

for i in range(0,10):
    test_location = Location("location " + str(i),i)
    test_locations.append(test_location)

test_locations[5] = Town("Thornwall", 5, "Test_World")
test_locations[2] = Cave("Creepy cave", 2, "Test_World")

# Define all connections
test_locations[0].adjacent_locations = [1, 3, 5]
test_locations[1].adjacent_locations = [0, 2, 5]
test_locations[2].adjacent_locations = [1]
test_locations[3].adjacent_locations = [0, 4]
test_locations[4].adjacent_locations = [3]
test_locations[5].adjacent_locations = [0, 1, 6, 8, 9]
test_locations[6].adjacent_locations = [5, 7, 9]
test_locations[7].adjacent_locations = [6]
test_locations[8].adjacent_locations = [5]
test_locations[9].adjacent_locations = [5, 6]"""

test_locations2[1].adjacent_locations = [2, 3, 4]
test_locations2[2].adjacent_locations = [1, 5]
test_locations2[3].adjacent_locations = [1, 4]
test_locations2[4].adjacent_locations = [1, 3, 5, 7]
test_locations2[5].adjacent_locations = [2, 4, 6, 8]
test_locations2[6].adjacent_locations = [5, 9, 10]
test_locations2[7].adjacent_locations = [4, 8]
test_locations2[8].adjacent_locations = [5, 7, 9]
test_locations2[9].adjacent_locations = [6, 8]
test_locations2[10].adjacent_locations = [6]

world = WorldMap(name="Test_World2", all_map_locations=test_locations2)

#Note: Displays must be added after all objects are defined. Or you get error that I was to lazy to fix.
world.display = Display(world, page_heading="You are wandering in the world", paragraph="Be safe")

town.display = Display(town, page_heading="You are in {}".format(town.name),
    paragraph="There are many places to visit within the town. Have a look!",
    places_of_interest=[("/store/greeting", "Blacksmith", "Shops"),
        ("/barracks", "Barracks"),
        ("/marketplace/greeting", "Marketplace"),
        ("/tavern", "Tavern", "Other"),
        ("/old_mans_hut", "Old Man's Hut"),
        ("/leave_town", "Village Gate", "Outskirts"),
        ("/WorldMap/{}/{}".format(town.location_world.name, town.id), "World Map")])
        
cave.display = Display(cave, page_heading="You are in a cave called {}".format(cave.name),
    paragraph="There are many scary places to die within the cave. Have a look!",
    places_of_interest=[("/WorldMap/{}/{}".format(cave.location_world.name, cave.id), "World Map")])

current_location = town
game_worlds = [world] #Just chop this out and use world instead.


#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
#game_worlds = [World_Map("Test_World", TEST_WORLD_ID, test_locations)]

#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]

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
    
all_store_items = []
all_marketplace_items = []

###########
#Quests
##########
quest1 = Quest("Get Acquainted with the Blacksmith", "Go talk to the blacksmith.")
quest1.next_quests.append(Quest("Get Acquainted with the Blacksmith", "Buy your first item.", reward_xp=7))
quest2 = Quest("Equipping/Unequipping", "Equip any item.")
quest2.next_quests.append(Quest("Equipping/Unequipping", "Unequip any item."))
        
testing_quests = [quest1, quest2] #Which is really 4 quests.

##########
#Users (and heroes)
"""
NOTE: password is set as plaintext here. It must (and currently is) hashed in database.py
when prebuilt_objects are preloaded into the database.
"""
##########
marlen = User(username="marlen", password="brunner")
haldon = Hero(name="Haldon", fathers_job="Priest", current_world=world, current_location=town, gold = 5000)
haldon.active_quests = testing_quests
marlen.heroes = [haldon]
users = [marlen]

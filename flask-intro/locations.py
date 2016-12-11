"""
Author: Marlen Brunner

1. This module should provide a class for each type of location within the game.
2. These classes should use inheritance as much as possible.
3. Each class should provide a render function which uses a flask template and
can be inserted into the main website.

Basic layout should be:
Game Objects (from other module maybe?) I am just going to start with Location as "progenitor".
-Location
--Town
---Shop
----display
---Blacksmith, etc.
---display
--leave
--enter
--display
"""

class Location(object):
    #Globals
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.location_type = None
        self.adjacent_locations = []
        pass

class World_Map(Location):
    def __init__(self, name, id, all_map_locations):
        super(World_Map, self).__init__(name, id)
        self.location_type = "World_Map"
        #self.map_coordinates = [0,0]
        #self.all_map_ids = all_map_ids
<<<<<<< HEAD
=======

>>>>>>> 57de2172e0aa81a34937ab07c88b55b31a1fac1c
        self.all_map_locations = all_map_locations
        self.current_location = all_map_locations[0]
        self.map_cities = []
        self.page_title = self.name
        self.page_heading = "You are wandering in the world"
        self.page_image = "map"
        self.paragraph = "Be safe"
        self.page_image = name
        self.places_of_interest = []

    def show_directions(self):
        directions = self.current_location.adjacent_locations
<<<<<<< HEAD
        if directions == []:
            directions = [1,2,3]
=======
>>>>>>> 57de2172e0aa81a34937ab07c88b55b31a1fac1c
        self.map_cities = [location for location in self.all_map_locations if (location == self.current_location and (location.location_type == "Town" or location.location_type == "Cave"))] # too long, but will refactor later
        if len(self.map_cities) > 0:
            self.places_of_interest = [("/" + self.map_cities[0].location_type + "/" + self.map_cities[0].name, self.map_cities[0].name)]
        else:
            self.places_of_interest = []
        return directions

# temporarily location_id is the same as the index in the list of all_map_locations
    def find_location(self, location_id):
        id = int(location_id)
        if (id == self.id): # To be Dealt with later
            id = 0
        return self.all_map_locations[int(id)]
            
    # temporarily location_id is the same as the index in the list of all_map_locations
    def find_location(self, location_id):
        id = int(location_id)
        if (id == self.id): # To be Dealt with later
            id = 0
        return self.all_map_locations[int(id)]
        
class Town(Location):
    def __init__(self, name, id, location_world):
        super(Town, self).__init__(name, id)
        self.location_type = "Town"
        self.location_world = location_world
        #self.location_coordinate = [0,0]
        self.page_title = self.name
        self.page_heading = "You are in " + self.name
        self.page_image = "town"
        self.paragraph = "There are many places to visit within the town. Have a look!"
        self.places_of_interest = [("/store/greeting", "Blacksmith", "Shops"),
                                  ("/barracks", "Barracks"),
                                  ("/marketplace/greeting", "Marketplace"),
                                  ("/tavern", "Tavern", "Other"),
                                  ("/old_mans_hut", "Old Man's Hut"),
                                  ("/leave_town", "Village Gate", "Outskirts"),
                                  ("/World_Map/" + self.location_world + "/" + str(self.id), "World Map")]

class Cave(Location):
    def __init__(self, name, id, location_world):
        super(Cave, self).__init__(name, id)
        self.location_type = "Cave"
        self.location_world = location_world
        #self.location_coordinate = [1,1]
        self.page_title = self.name
        self.page_heading = "You are in a cave called " + self.name
        self.page_image = "cave"
        self.paragraph = "There are many scary places to die within the cave. Have a look!"
        self.places_of_interest = [("/World_Map/" + self.location_world + "/" + str(self.id), "World Map")]


"""
    def get_locations(self):
        
        with open("data\town." + name + ".txt", 'r') as f:
            data = f.read()
            return Town.parse(data)
        
    def display(self):
        Return an html object of the town built from a template.
        
        This should be able to be "popped" into the main post-login site in the content section.
        pass
    
    def parse(data):
        pass
"""
<<<<<<< HEAD
        

 #------------------------------------
 #
 #  Initializing Game Worlds 
 #  (To be moved to a common 
 #   init function later)
 #
 #------------------------------------
TEST_WORLD_ID = 999 # ...
TEST_WORLD_ID2 = 998 # ...
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

for i in range(0, 11):
    test_location = Location("location " + str(i),i)
    test_locations2.append(test_location)
    
test_locations2[5] = Town("5: Thornwall", 5, "Test_World")
test_locations2[2] = Cave("2: Creepy cave", 2, "Test_World")

""" Define all connections
=======

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
>>>>>>> 57de2172e0aa81a34937ab07c88b55b31a1fac1c
test_locations[0].adjacent_locations = [1, 3, 5]
test_locations[1].adjacent_locations = [0, 2, 5]
test_locations[2].adjacent_locations = [1]
test_locations[3].adjacent_locations = [0, 4]
test_locations[4].adjacent_locations = [3]
test_locations[5].adjacent_locations = [0, 1, 6, 8, 9]
test_locations[6].adjacent_locations = [5, 7, 9]
test_locations[7].adjacent_locations = [6]
test_locations[8].adjacent_locations = [5]
<<<<<<< HEAD
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

game_worlds = [World_Map("Test_World2", TEST_WORLD_ID2, test_locations2)]
#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
#game_worlds = [World_Map("Test_World", TEST_WORLD_ID, test_locations)]
=======
test_locations[9].adjacent_locations = [5, 6]

game_worlds = [World_Map("Test_World", TEST_WORLD_ID, test_locations)]

#game_locations = [World_Map("Test_World", 999, [Town("Thornwall", "Test_World"), Cave("Samplecave", "Test_World")]), World_Map("Test_World2", [(0,0), (0,1), (0,2), (1,2), (1, 3), (1, 4), (2, 1), (2, 2)], [])]
>>>>>>> 57de2172e0aa81a34937ab07c88b55b31a1fac1c


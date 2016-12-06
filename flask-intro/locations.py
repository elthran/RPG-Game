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
    def __init__(self, name):
        self.name = name
        self.location_type = None
        pass

class World_Map(Location):
    def __init__(self, name, map_coordinates=[0,0]):
        super(World_Map, self).__init__(name)
        self.location_type = "World_Map"
        self.map_coordinates = map_coordinates
        self.all_map_cities = [Town("Thornwall", self.name), Cave("Samplecave", self.name)]
        self.map_cities = []
        self.page_title = self.name
        self.page_heading = "You are wandering in the world"
        self.page_image = "map"
        self.paragraph = "Be safe"
        self.places_of_interest = []

    def show_directions(self):
        directions = [("north", "North"), ("east", "East")]
        if self.map_coordinates[0] > 0:
            directions.append(("west", "West"))
        if self.map_coordinates[1] > 0:
            directions.append(("south", "South"))
        self.map_cities = [city for city in self.all_map_cities if city.location_coordinate == self.map_coordinates]
        if len(self.map_cities) > 0:
            self.places_of_interest = [("/" + self.map_cities[0].location_type + "/" + self.map_cities[0].name, self.map_cities[0].name)]
        else:
            self.places_of_interest = []
        return directions
            
        
class Town(Location):
    def __init__(self, name, location_world):
        super(Town, self).__init__(name)
        self.location_type = "Town"
        self.location_world = location_world
        self.location_coordinate = [0,0]
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
                                  ("/World_Map/" + self.location_world + "/" + str(self.location_coordinate[0]) + str(self.location_coordinate[1]), "World Map")]

class Cave(Location):
    def __init__(self, name, location_world):
        super(Cave, self).__init__(name)
        self.location_type = "Cave"
        self.location_world = location_world
        self.location_coordinate = [1,1]
        self.page_title = self.name
        self.page_heading = "You are in a cave called " + self.name
        self.page_image = "cave"
        self.paragraph = "There are many scary places to die within the cave. Have a look!"
        self.places_of_interest = [("/World_Map/" + self.location_world + "/" + str(self.location_coordinate[0]) + str(self.location_coordinate[1]), "World Map")]


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
        
game_locations = [World_Map("Test_World")]


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

class Location:
	#Globals
	def __init__(self):
		pass
	def display(self):
		pass
		
def Town(Location):
	def __init__(self, name):
		self.name = name
		self.locations = self.get_locations()
		
	def get_locations(self):
		
		with open("data\town." + name + ".txt", 'r') as f:
			data = f.read()
			return Town.parse(data)
		
	def display(self):
		"""Return an html object of the town built from a template.
		
		This should be able to be "popped" into the main post-login site in the content section.
		"""
		pass
	
	def parse(data):
		pass
		
"""
Old code
@app.route('/town/<town_name>')
@login_required
def town(town_name):
    page_title = str(town_name)
    page_heading = "You are in " + page_title
    page_image = "town"
    paragraph = page_title + ". There are many places to visit within the town. Have a look!"
    if town_name == "placeholder_name":
        town_links = [("/store/greeting", "Blacksmith", "Shops"),
                      ("/barracks", "Barracks"),
                      ("/under_construction", "Marketplace"),
                      ("/tavern", "Tavern", "Other"),
                      ("/old_mans_hut", "Old Man's Hut"),
                      ("/leave_town", "Village Gate", "Outskirts")]
    if town_name == "temporary_second_town":
        town_links = [("/store/greeting", "Blacksmith", "Shops")]   
    return render_template('home.html', myHero=myHero, page_title=page_title, page_heading=page_heading, page_image=page_image, paragraph=paragraph, town_links=town_links)
"""
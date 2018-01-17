"""
Notes:
    "wolf pelts" quest needs to be completed before you get
    the "2 coins" quest.

    "2 coins" quest has an invisible subquest to "kill goblins"
    or maybe "find goblins", "kill for coins" ...

    Drink quest can be taken at any time throughout ...
    ("Drink", "Jobs", "Leave the tavern.") are one level ...
    I guess you can see that by seeing what occurs on level 1
    of all lists?
    "Jobs move forward" and "Jobs still working on it" are one level.
]
"""

path_1 = [
    "Leave the tavern."
]

path_2 = [
    "Try and buy a drink for 25 gold. (This fully heals you)",
    "Pay me 25 gold first if you want to see your drink.",
]
path_3 = [
    "Try and buy a drink for 25 gold. (This fully heals you)",
    "You give the bartender 25 gold and he pours you a drink.",
    "You drink the beer",
    "You feel very refreshed!",
]

path_4 = [
    "Ask if there are any jobs you can do.",
    "The bartender has asked you to find 2 wolf pelts!",
]

# Can be asked after any quest stage? I think that is implement correctly here.
path_5 = [
    "Ask if there are any jobs you can do.",
    "The bartender has asked you to {quest_stage_name}",
    "I'm still working on {quest_stage_name}",
    "Don't take too long!",
]

path_6 = [
    "Ask if there are any jobs you can do.",
    "The bartender has asked you to find 2 wolf pelts!",
    "Collect 2 Wolf Pelts for the Bartender",
    "Give the bartender 2 wolf pelts.",
    "You have given the bartender 2 wolf pelts and completed your quest! He has rewarded you with 5000 gold.",
    "Ask if there are any jobs you can do.",
    "Actually, I could use a hand with something if you are interested in becoming my apprentice. First I will need 2 copper coins. Some of the goblins around the city are carrying them.",
    "Choose to attempt to Become an apprentice at the tavern.",
    "You need to find two copper coins and give them to the blacksmith",
    "Find 2 coins",
    "Hand them to the Blacksmith.",
    "Tell the bartender you succeeded.",
    "Ask if there are any jobs you can do.",
    "Now the bartender wants you to find a spider leg.",
    "Find a spider.",
    "Kill it.",
    "Take its leg."
    "Hand the bartender a spider leg",
    "You are now my apprentice!"
    "Welcome, my apprentice!",
]

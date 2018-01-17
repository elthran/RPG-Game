path_b = [
    "Leave the tavern."
]

path_c = [
    "Drink",
    "Buy a drink for 25 gold. (This fully heals you)",
    "You give the bartender 25 gold and he pours you a drink. You feel very refreshed!",
    "Leave the tavern."
]

path_d = [
    "Drink",
    "Buy a drink for 25 gold. (This fully heals you)",
    "Pay me 25 gold first if you want to see your drink.",
    "Leave the tavern."
]

path_e = [
    "Jobs",
    "Ask if there are any jobs you can do.",
    "The bartender has asked you to find 2 wolf pelts!",
    "Leave the tavern."
]

path_f = [
    "Jobs",
    "Collect 2 Wolf Pelts for the Bartender"
    "Quest not finished",
    "I'm still looking for the 2 wolf pelts.",
    "Don't take too long!",
    "Leave the tavern."
]

path_g = [
    "Jobs",
    "Collect 2 Wolf Pelts for the Bartender",
    "Hand in Quest",
    "Give the bartender 2 wolf pelts.",
    "You have given the bartender 2 wolf pelts and completed your quest! He has rewarded you with 5000 gold.",
    "Leave the tavern."
]

path_h = [
    "Jobs",
    "Actually, I could use a hand with something if you are interested in becoming my apprentice. First I will need 2 copper coins. Some of the goblins around the city are carrying them.",
    "Attempt to Become an apprentice at the tavern.",
    "You need to find two copper coins and give them to the blacksmith",
    "Leave the tavern."
]

path_i = [
    "Jobs",
    "Attempt to Become an apprentice at the tavern.",
    "You need to find two copper coins and give them to the blacksmith",
    "QuestNotFinished",
    "Don't take too long!",
    "Leave the tavern."
]

path_j = [
    "Jobs",
    "Attempt to Become an apprentice at the tavern.",
    "You need to find two copper coins and give them to the blacksmith",
    "HandInQuest",
    "Give the bartender 2 copper coins.",
    "Now the bartender wants you to find a spider leg.",
    "Leave the tavern."
]

path1 = [
    "Welcome, my apprentice!",
    "Leave the tavern."
]

path2 = [
    "Welcome, my apprentice!",
    "Buy a drink for 25 gold. (This fully heals you)",
    "You give the bartender 25 gold and he pours you a drink. You feel very refreshed!",
    "Drink",
    "Leave the tavern."
]

path3 = [
    "Welcome, my apprentice!",
    "Pay me 25 gold first if you want to see your drink.",
    "Leave the tavern."
]



if "Become an apprentice at the tavern." in hero.completed_quests:
    paragraph = "Welcome, my apprentice!"
# else:
#     paragraph = "Greetings traveler! What can I get for you today?"
page_links = [("Return to ", "/tavern", "tavern", ".")]  # I wish it looked like this
dialogue_options = {"Drink": "Buy a drink for 25 gold. (This fully heals you)"}

if "Collect 2 Wolf Pelts for the Bartender" not in hero.errands and "Collect 2 Wolf Pelts for the Bartender" not in hero.completed_quests:
    dialogue_options["Jobs"] = "Ask if there are any jobs you can do."
if "Collect 2 Wolf Pelts for the Bartender" in hero.errands:
    if any(item.name == "Wolf Pelt" and item.amount_owned >= 2 for item in hero.inventory):
        dialogue_options["HandInQuest"] = "Give the bartender 2 wolf pelts."
    else:
        dialogue_options["QuestNotFinished"] = "I'm still looking for the 2 wolf pelts."
if "Collect 2 Wolf Pelts for the Bartender" in hero.completed_quests:
    if any(quest[0] == "Become an apprentice at the tavern." and quest[2] == 1 for quest in hero.current_quests):
        if any(item.name == "Copper Coin" and item.amount_owned >= 2 for item in hero.inventory):
            dialogue_options["HandInQuest2"] = "Give the bartender 2 copper coins."
        else:
            dialogue_options["QuestNotFinished"] = "I'm still looking for the two copper coins."
    elif any(quest[0] == "Become an apprentice at the tavern." and quest[2] == 2 for quest in hero.current_quests):
        if any(item.name == "Spider Leg" and item.amount_owned >= 1 for item in hero.inventory):
            dialogue_options["HandInQuest3"] = "Give the bartender a spider leg."
        else:
            dialogue_options["QuestNotFinished"] = "I'm still looking for the spider leg."
    elif "Become an apprentice at the tavern." not in hero.completed_quests:
        dialogue_options["Jobs2"] = "Do you have any other jobs you need help with?"
if request.method == 'POST':
    tavern = False
    paragraph = ""
    dialogue_options = {}
    tavern_choice = request.form["tavern_choice"]
    if tavern_choice == "Drink":
        if hero.gold >= 25:
            hero.health = hero.health_maximum
            hero.gold -= 25
            page_heading = "You give the bartender 25 gold and he pours you a drink. You feel very refreshed!"
        else:
            page_heading = "Pay me 25 gold first if you want to see your drink."
    elif tavern_choice == "Jobs":
        hero.errands.append("Collect 2 Wolf Pelts for the Bartender")
        page_heading = "The bartender has asked you to find 2 wolf pelts!"
        page_image = ""
    elif tavern_choice == "HandInQuest":
        hero.gold += 5000
        hero.errands = [(name, stage) for name, stage in hero.current_quests if
                        name != "Collect 2 Wolf Pelts for the Bartender"]
        hero.completed_quests.append(("Collect 2 Wolf Pelts for the Bartender"))
        page_heading = "You have given the bartender 2 wolf pelts and completed your quest! He has rewarded you with 5000 gold."
    elif tavern_choice == "QuestNotFinished":
        page_heading = "Don't take too long!"
    elif tavern_choice == "Jobs2":
        page_heading = "Actually, I could use a hand with something if you are interested in becoming my apprentice. First I will need 2 copper coins. Some of the goblins around the city are carrying them."
        hero.current_quests.append(["Become an apprentice at the tavern.",
                                    "You need to find two copper coins and give them to the blacksmith", 1])
    elif tavern_choice == "HandInQuest2":
        hero.current_quests[0][1] = "Now the bartender wants you to find a spider leg."
        hero.current_quests[0][2] += 1
        page_heading = "Fantastic! Now I just need a spider leg."
    elif tavern_choice == "HandInQuest3":
        hero.current_quests = [quest for quest in hero.current_quests if
                               quest[0] != "Become an apprentice at the tavern."]
        hero.completed_quests.append("Become an apprentice at the tavern.")
        page_heading = "You are now my apprentice!"
        """

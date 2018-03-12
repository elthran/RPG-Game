"""
Name, Description, Attribute_Type, Type, [(Values Name, Value type,
    (Modifiers of value), Decimal Places)]
Linear: (Level multiplier), (Starting Value)
Root: Not finished. Looks like square root function. Used for diminishing
    returns and things that get better the larger they are. (Starting value)
    [Currently approaches 100]

Curvy: (larger "0" means it reaches the cap quicker) (smaller [1] means it
    reaxhes the cap quicker) ([2] is the cap or maximum possible value)
    ([3] is the negative amount)
Sensitive: Like curvy but has decimals (larger [0] means it reaches the cap
    quicker) (smaller [1] means it reaches the cap quicker) ([2] is the cap
    or maximum possible value) ([3] is the negative amount)
Modifier: (larger [0] means greater amplitude), (larger [1] means greater
    steepness and faster increase), (greater [2]  means greater frequency of
    waves)
Percent: ???
Empty: Sets this value to take on the value of "maximum". Must be placed after
    "Maximum" in the list of variables
"""

"""
Prof_Name, Prof_Descr, Prof_Attrib, [Formula_Type, Base_Value, Weight, # of Decimals], hidden_boolean, percent_boolean
"""

from build_code import normalize_attrib_name

PROFICIENCY_INFORMATION = [
    ("Health", "When your health reahes zero you fall unconscious.", "Vitality", ["linear", 5, 2, 0], False),
    ("Regeneration", "How many health points you recover each day.", "Vitality", ["linear", 1, 0.5, 1], False),
    ("Recovery", "How quickly you recover from poisons and negative effects.", "Vitality", ["linear", 1, 0, 0], False),
    ("Climbing", "The difficulty of objects of which you are able to climb.", "Agility", ["linear", 0, 1, 0], False),
    ("Storage", "The amount of weight that you can carry.", "Brawn", ["linear", 10, 3, 0], False),
    ("Encumbrance", "How much your are slowed down in combat by your equipment.", "Brawn", ["linear", 100, -1, 0], False),
    ("Endurance", "Number of actions you can perform each day.", "Resilience", ["linear", 3, 0.5, 0], False),
    ("Stamina", "How many endurance points you recover each day.", "Resilience", ["linear", 1, 0.5, 1], False),
    ("Damage minimum", "Mimimum damage you do on each hit", "Brawn", ["linear", 0, 1, 0], False),
    ("Damage maximum", "Maximum damage you do on each hit", "Brawn", ["linear", 1, 1, 0], False),
    ("Speed", "How fast you attack.", "Quickness", ["linear", 1, 0.05, 2], False),
    ("Accuracy", "The chance of your attacks hitting their target.", "Agility", ["linear_percent", 1, 1, 0], False),
    ("First strike", "Chance to strike first", "Quickness", ["linear", 1, 1, 0], False),
    ("Killshot", "Damage multiplier when performing a critical hit.", "Agility", ["linear", 1.5, 0.1, 1], False),
    ("Precision", "Ability to critically hit enemies.", "Agility", ["linear", 1, 1, 0], False),
    ("Defence", "Amount of all damage reduced.", "Resilience", ["linear", 0, 1, 0], False),
    ("Evade", "Chance to dodge.", "Quickness", ["linear", 1, 1, 0], False),
    ("Parry", "Chance to parry.", "Quickness", ["linear", 1, 1, 0], False),
    ("Flee", "Chance to run from a battle.", "Quickness", ["linear", 1, 1, 0], False),
    ("Riposte", "Chance to riposte an enemy attack.", "Agility", ["linear", 1, 1, 0], False),
    ("Fatigue", "How quickly you tire in combat.", "Resilience", ["linear", 1, 1, 0], False),
    ("Block", "Ability to block if a shield is equipped.", "Resilience", ["linear", 1, 1, 0], False),
    ("Stealth", "Chance to avoid detection.", "Agility", ["linear", 1, 1, 0], False),
    ("Pickpocketing", "Skill at stealing from others.", "Agility", ["linear", 1, 1, 0], False),
    ("Faith", "Strength of spells you cast.", "Divinity", ["linear", 1, 1, 0], False),
    ("Sanctity", "Amount of sanctity you can have.", "Divinity", ["linear", 1, 1, 0], False),
    ("Redemption", "Amount of sanctity you recover each day.", "Divinity", ["linear", 0, 0.5, 1], False),
    ("Resist holy", "Ability to resist holy damage", "Divinity", ["linear", 1, 1, 0], False),
    ("Bartering", "Discount from negotiating prices.", "Charisma", ["linear", 1, 1, 0], True),
    ("Oration", "Proficiency in speaking to others.", "Charisma", ["linear", 1, 1, 0], False),
    ("Charm", "How quickly other people will like you.", "Charisma", ["linear", 1, 1, 0], False),
    ("Trustworthiness", "How much other players trust you.", "Charisma", ["linear", 1, 1, 0], False),
    ("Renown", "How much your actions affect your reputation.", "Charisma", ["linear", 1, 1, 0], False),
    ("Knowledge", "Ability to understand.", "Intellect", ["linear", 1, 1, 0], False),
    ("Literacy", "Ability to read.", "Intellect", ["linear", 1, 1, 0], False),
    ("Understanding", "How much more quickly you level up.", "Intellect", ["linear", 0, 2, 0], False),
    ("Luckiness", "Chance to have things turn your way against all odds.", "Fortuity", ["linear", 1, 1, 0], False),
    ("Adventuring", "Chance to discover treasure.", "Fortuity", ["linear", 1, 1, 0], False),
    ("Logistics",  "How far you can move on the map", "Pathfinding", ["linear", 1, 1, 0], False),
    ("Mountaineering", "Modifier for mountain movement.", "Pathfinding", ["linear", 1, 1, 0], False),
    ("Woodsman", "Modifier for forest movement.", "Pathfinding", ["linear", 1, 1, 0], False),
    ("Navigator", "Modifier for water movement.", "Pathfinding", ["linear", 1, 1, 0], False),
    ("Detection", "Chance to discover enemy stealth and traps.", "Survivalism", ["linear", 1, 1, 0], False),
    ("Caution",  "See information about a new grid before going there", "Survivalism", ["linear", 1, 1, 0], False),
    ("Explorer", "Additional options on the map, such as foraging", "Survivalism", ["linear", 1, 1, 0], False),
    ("Huntsman", "Learn additional information about enemies.", "Survivalism", ["linear", 1, 1, 0], False),
    ("Survivalist", "Create bandages, tents, and other useful objects", "Survivalism", ["linear", 1, 1, 0], False),
    ("Resist frost", "Ability to resist frost damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Resist flame", "Ability to resist flame damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Resist shadow", "Ability to resist shadow damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Resist poison", "Ability to resist poison damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Resist blunt", "Ability to resist blunt damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Resist slashing", "Ability to resist slashing damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Resist piercing", "Ability to resist piercing damage", "Resilience", ["linear", 1, 1, 0], False),
    ("Courage", "Your ability to overcome fears.", "Willpower", ["linear", 1, 1, 0], False),
    ("Sanity", "Your ability to resist mind altering affects.", "Willpower", ["linear", 1, 1, 0], False),
    ("Thorns", "Amount of damage that attackers take.", None, ["",0,0,0], True),
    #("Lifesteal", "Amount of health that you heal on each successful hit.", None, ["",0,0,0], True)
]

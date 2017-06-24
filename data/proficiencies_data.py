# Name, Description, Attribute_Type, Type, [(Values Name, Value type, (Modifiers of value))]
# Linear: Level multiplier, Base Value
# Curvy: (larger "0" means it reaches the cap quicker) (smaller "1" means it reaxhes the cap quicker) ("2" is the cap or maximum possible value) ("3" is the negative amount)
# Sensitive: Like curvy but has decimals (larger "0" means it reaches the cap quicker) (smaller "1" means it reaxhes the cap quicker) ("2" is the cap or maximum possible value) ("3" is the negative amount)
# Modifier: (larger "a" means greater amplitude), (larger "b" means greater steepness andfaster increase), (greater "c" means greater frequency of waves)
# Empty: Sets this value to take on the value of "maximum". Must be placed after "Maximum" in the list of variables
PROFICIENCY_INFORMATION = [
    ("Health", "How much you can take before you die", "Vitality", [("Maximum", "linear", (5, 0)), ("Current", "empty")]),
    ("Regeneration", "How quickly your wounds heal", "Vitality", [("Maximum", "linear", (5, 0)), ("Current", "empty")]),
    ("Recovery", "How quickly you recover from poisons and negative effects", "Vitality",[("Maximum", "linear", (5, 0)), ("Current", "empty")]),
    ("Climbing", "Your ability to climb obstacles", "Agility", [("Chance", "percent", (0.5, 20, 65, 0))]),
    ("Storage", "Your carrying capacity", "Brawn", [("Maximum", "linear", (2.5, 8)), ("Current", "empty")]),
    ("Encumbrance", "How much your are slowed down in combat by your equipment", "Brawn", [("Accuracy", "percent", (2, 10, 5, 5))]),
    ("Endurance", "Actions performed each day", "Resilience", [("Maximum", "linear", (0.25, 5)), ("Current", "empty")]),
    ("Damage", "How much damage you do on each hit", "Brawn", [("Minimum", "curvy", (0.5, 0.1, 0.1, 0)), ("Maximum",  "curvy", (0.5, 0.2, 0.1, 1))]),
    ("Speed", "How fast you attack", "Quickness", [("Speed", "sensitive", (0.1, 0.1, 0.7, 1))]),
    ("Accuracy", "The chance of your attacks hitting their target.", "Agility", [("Accuracy", "percent", (2, 10, 5, 5))]),
    ("First strike", "Chance to strike first", "Quickness", [("Chance", "percent", (0.5, 5, 50, -30))]),
    ("Killshot", "Ability to hit enemies in their weak spot", "Agility", [("Chance", "percent", (0.3, 5, 50, -22)), ("Modifier", "percent", (0.5, 1, 0.5, 0))]),
    ("Defence", "Damage reduction", "Resilience", [("Modifier", "percent", (0.1, 7, 35, 0))]),
    ("Evade", "Chance to dodge", "Quickness", [("Chance", "percent", (0.1, 10, 15, 0))]),
    ("Parry", "Chance to parry", "Quickness", [("Chance", "percent", (0.2, 15, 15, 0))]),
    ("Flee", "Chance to run from a battle", "Quickness", [("Chance", "percent", (0.2, 15, 15, 0))]),
    ("Riposte", "Chance to riposte an enrmy attack", "Agility", [("Chance", "percent", (0.3, 20, 15, 0))]),
    ("Fatigue", "How quickly you tire in combat", "Resilience", [("Maximum", "linear", (2, -1)), ("Current", "empty")]),
    ("Block", "Ability to block if a shield is equipped", "Resilience", [("Chance", "percent", (0.25, 25, 60, 0)), ("Modifier", "percent", (1.5, 20, 100, 0))]),
    ("Stealth", "Chance to avoid detection", "Agility", [("Chance", "percent", (0.5, 20, 65, 0))]),
    ("Pickpocketing", "Skill at stealing from others", "Agility", [("Chance", "percent", (0.6, 15, 70, 0))]),
    ("Faith", "Strength of spells you cast", "Divinity", [("Modifier", "percent", (2, 10, 5, 0))]),
    ("Sanctity", "Amount of sanctity you can have", "Divinity", [("Maximum", "linear", (5, 0)), ("Current", "empty")]),
    ("Resist holy", "Ability to resist holy damage", "Divinity", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Bartering", "Chance to negotiate prices", "Charisma", [("Chance", "percent", (0.5, 20, 60, 0))]),
    ("Oration", "Proficiency in speaking to others", "Charisma", [("Modifier", "percent", (0.75, 15, 60, 0))]),
    ("Charm", "How quickly other people will like you", "Charisma", [("Modifier", "percent", (0.75, 15, 60, 0))]),
    ("Trustworthiness", "How much other players trust you", "Charisma", [("Modifier", "percent", (0.75, 15, 60, 0))]),
    ("Renown", "How much your actions affect your reputation", "Charisma", [("Modifier", "percent", (0.75, 15, 60, 0))]),
    ("Knowledge", "Ability to understand", "Intellect", [("Modifier", "percent", (0.1, 5, 50, 0))]),
    ("Literacy", "Ability to read", "Intellect", [("Modifier", "percent", (0.25, 10, 75, 0))]),
    ("Understanding", "How quickly you level up", "Intellect", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Luckiness", "Chance to have things turn your way against all odds", "Fortuity", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Adventuring", "Chance to discover treasure", "Fortuity", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Logistics",  "How far you can move on the map", "Pathfinding", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Mountaineering", "Modifier for mountain movement", "Pathfinding", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Woodsman", "Modifier for forest movement", "Pathfinding", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Navigator", "Modifier for water movement", "Pathfinding", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Luck", "Chance to have things turn your way against all odds", "Survivalism", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Detection", "Chance to discover enemy stealth and traps", "Survivalism", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Caution",  "See information about a new grid before going there", "Survivalism", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Explorer", "Additional options on the map, such as foraging", "Survivalism", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Huntsman", "Learn additional information about enemies", "Survivalism", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Survivalist", "Create bandages, tents, and other useful objects", "Survivalism", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Resist frost", "Ability to resist frost damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist flame", "Ability to resist flame damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist shadow", "Ability to resist shadow damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist poison", "Ability to resist poison damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist blunt", "Ability to resist blunt damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist slashing", "Ability to resist slashing damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist piercing", "Ability to resist piercing damage", "Resilience", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Courage", "Your ability to overcome fears", "Willpower", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Sanity", "Your ability to resist mind altering affects", "Willpower", [("Modifier", "percent", (1, 50, 100, -15))])
    ]


ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

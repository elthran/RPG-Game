# Name, Description, Attribute_Type, Type, [(Values Name, Value type, (Modifiers of value))]
# Linear: Level multiplier, Base Value
# Curvy: (larger "0" means it reaches the cap quicker) (smaller "1" means it reaxhes the cap quicker) ("2" is the cap or maximum possible value) ("3" is the negative amount)
# Sensitive: Like curvy but has decimals (larger "0" means it reaches the cap quicker) (smaller "1" means it reaxhes the cap quicker) ("2" is the cap or maximum possible value) ("3" is the negative amount)
# Modifier: (larger "a" means greater amplitude), (larger "b" means greater steepness andfaster increase), (greater "c" means greater frequency of waves)
# Empty: Sets this value to take on the value of "maximum". Must be placed after "Maximum" in the list of variables
PROFICIENCY_INFORMATION = [
    ("Health", "How much you can take before you die", "Vitality", "Offense", [("Maximum", "linear", (5, 0)), ("Current", "empty")]),
    ("Sanctity", "Casting points", "Divinity", "Offense", [("Maximum", "linear", (1.5, -1)), ("Current", "empty")]),
    ("Storage", "Carrying capacity", "Strength", "Offense", [("Maximum", "linear", (2.5, 8)), ("Current", "empty")]),
    ("Endurance", "Actions performed each day", "Fortitude", "Offense", [("Maximum", "linear", (0.25, 5)), ("Current", "empty")]),
    ("Attack damage", "How hard you hit", "Strength", "Offense", [("Minimum", "curvy", (0.5, 0.1, 0.1, 0)), ("Maximum",  "curvy", (0.5, 0.2, 0.1, 1))]),
    ("Attack speed", "How fast you attack", "Agility", "Offense", [("Speed", "sensitive", (0.1, 0.1, 0.7, 1))]),
    ("Attack accuracy", "Chance to hit", "Agility", "Offense", [("Accuracy", "percent", (2, 10, 5, 5))]),
    ("First strike", "Chance to strike first", "Agility", "Offense", [("Chance", "percent", (0.5, 5, 50, -30))]),
    ("Critical hit", "Ability to hit your enemy's weakspots", "Perception", "Offense", [("Chance", "percent", (0.3, 5, 50, -22)), ("Modifier", "percent", (0.5, 1, 0.5, 0))]),
    ("Defence", "Damage reduction", "Fortitude", "Defence", [("Modifier", "percent", (0.1, 7, 35, 0))]),
    ("Evade", "Chance to dodge", "Reflexes", "Defence", [("Chance", "percent", (0.1, 10, 15, 0))]),
    ("Parry", "Chance to parry", "Reflexes", "Defence", [("Chance", "percent", (0.2, 15, 15, 0))]),
    ("Riposte", "Chance to riposte", "Agility", "Defence", [("Chance", "percent", (0.3, 20, 15, 0))]),
    ("Fatigue", "How quickly you tire in combat", "Fortitude", "Defence", [("Maximum", "linear", (2, -1)), ("Current", "empty")]),
    ("Block", "Ability to block if a shield is equipped", "Strength", "Defence", [("Chance", "percent", (0.25, 25, 60, 0)), ("Modifier", "percent", (1.5, 20, 100, 0))]),
    ("Stealth", "Chance to avoid detection", "Perception", "Stealth", [("Chance", "percent", (0.5, 20, 65, 0))]),
    ("Pickpocketing", "Chance to steal", "Agility", "Stealth", [("Chance", "percent", (0.6, 15, 70, 0))]),
    ("Faith", "Ability to cast spells", "Divinity", "Holiness", [("Modifier", "percent", (2, 10, 5, 0))]),
    ("Bartering", "Chance to negotiate prices", "Charisma", "Diplomacy", [("Chance", "percent", (0.5, 20, 60, 0))]),
    ("Oration", "Ability to speak", "Strength", "Wisdom", [("Modifier", "percent", (0.75, 15, 60, 0))]),
    ("Knowledge", "Ability to understand", "Wisdom", "Diplomacy", [("Modifier", "percent", (0.1, 5, 50, 0))]),
    ("Literacy", "Ability to read", "Wisdom", "Diplomacy", [("Modifier", "percent", (0.25, 10, 75, 0))]),
    ("Luck", "Chance to have things turn your way against all odds", "Fortuity", "Diplomacy", [("Chance", "percent", (0.2, 5, 10, 0))]),
    ("Resist frost", "Ability to resist frost damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist flame", "Ability to resist flame damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist shadow", "Ability to resist shadow damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist holy", "Ability to resist holy damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist poison", "Ability to resist poison damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist blunt", "Ability to resist blunt damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist slashing", "Ability to resist slashing damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))]),
    ("Resist piercing", "Ability to resist piercing damage", "Resilience", "Resistance", [("Modifier", "percent", (1, 50, 100, -15))])
    ]


ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

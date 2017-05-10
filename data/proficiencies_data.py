# Name, Description, Attribute_Type, Type, [(Values Name, Value type, (Modifiers of value))]
PROFICIENCY_INFORMATION = [
    ("Attack damage", "How hard you hit", "Strength", "Offense", [("Minimum", "damage", (0.5, 0.3, 1.5)), ("Maximum",  "damage", (0.6, 0.3, 1.5)), ("Average",  "damage", (0.55, 0.3, 1.5))]),
    ("Attack speed", "How fast you attack", "Agility", "Offense", [("Speed", "percent", (2, 10, 5))]),
    ("Attack accuracy", "Chance to hit", "Agility", "Offense", [("Accuracy", "percent", (2, 10, 5))]),
    ("First strike", "Chance to strike first", "Agility", "Offense", [("Chance", "percent", (2, 1, 5))]),
    ("Critical hit", "Ability to hit your enemy's weakspots", "Agility", "Offense", [("Chance", "percent", (2, 10, 5)), ("Modifier", "percent", (2, 10, 5))]),
    ("Defence", "Damage reduction", "Fortitude", "Defence", [("Modifier", "percent", (2, 10, 5))]),
    ("Evade", "Chance to dodge", "Strength", "Defence", [("Chance", "percent", (2, 10, 5))]),
    ("Parry", "Chance to parry", "Strength", "Defence", [("Chance", "percent", (2, 10, 5))]),
    ("Riposte", "Chance to riposte", "Strength", "Defence", [("Chance", "percent", (2, 10, 5))]),
    ("Block", "Ability to block if a shield is equipped", "Strength", "Defence", [("Chance", "percent", (2, 10, 5)), ("Modifier", "percent", (2, 10, 5))]),
    ("Stealth", "Chance to avoid detection", "Strength", "Stealth", [("Chance", "percent", (2, 10, 5))]),
    ("Pickpocketing", "Chance to steal", "Strength", "Stealth", [("Chance", "percent", (2, 10, 5))]),
    ("Faith", "Ability to cast spells", "Strength", "Holiness", [("Modifier", "percent", (2, 10, 5))]),
    ("Bartering", "Chance to negotiate prices", "Strength", "Diplomacy", [("Chance", "percent", (2, 10, 5))]),
    ("Oration", "Ability to speak", "Strength", "Diplomacy", [("Modifier", "percent", (2, 10, 5))]),
    ("Knowledge", "Ability to understand", "Strength", "Diplomacy", [("Modifier", "percent", (2, 10, 5))]),
    ("Literacy", "Ability to read", "Strength", "Diplomacy", [("Modifier", "percent", (2, 10, 5))]),
    ("Luck", "Chance to have things turn your way against all odds", "Strength", "Diplomacy", [("Chance", "percent", (2, 10, 5))]),
    ("Resist frost", "Ability to resist frost damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist flame", "Ability to resist flame damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist shadow", "Ability to resist shadow damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist holy", "Ability to resist holy damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist poison", "Ability to resist poison damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist blunt", "Ability to resist blunt damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist slashing", "Ability to resist slashing damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist piercing", "Ability to resist piercing damage", "Strength", "Resistance", [("Modifier", "percent", (2, 10, 5))])
    ]


ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

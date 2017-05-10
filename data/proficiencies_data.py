# Name, Description, Attribute_Type, Type, [Values]
PROFICIENCY_INFORMATION = [
    ("Attack damage", "How hard you hit", "Strength", "Offense", [("Minimum", 1), ("Maximum", 2), ("Average", 1.5)]),
    ("Attack speed", "How fast you attack", "Agility", "Offense", [("Speed", 1)]),
    ("Attack accuracy", "Chance to hit", "Agility", "Offense", [("Accuracy", 1)]),
    ("First strike", "Chance to strike first", "Agility", "Offense", [("Chance", 1)]),
    ("Critical hit", "Ability to hit your enemy's weakspots", "Agility", "Offense", [("Chance", 1), ("Modifier", 1)]),
    ("Defence", "Damage reduction", "Fortitude", "Defence", [("Modifier", 1)]),
    ("Evade", "Chance to dodge", "Strength", "Defence", [("Chance", 1)]),
    ("Parry", "Chance to parry", "Strength", "Defence", [("Chance", 1)]),
    ("Riposte", "Chance to riposte", "Strength", "Defence", [("Chance", 1)]),
    ("Block", "Ability to block if a shield is equipped", "Strength", "Defence", [("Chance", 1), ("Modifier", 1)]),
    ("Stealth", "Chance to avoid detection", "Strength", "Stealth", [("Chance", 1)]),
    ("Pickpocketing", "Chance to steal", "Strength", "Stealth", [("Chance", 1)]),
    ("Faith", "Ability to cast spells", "Strength", "Holiness", [("Modifier", 1)]),
    ("Bartering", "Chance to negotiate prices", "Strength", "Diplomacy", [("Chance", 1)]),
    ("Oration", "Ability to speak", "Strength", "Diplomacy", [("Modifier", 1)]),
    ("Knowledge", "Ability to understand", "Strength", "Diplomacy", [("Modifier", 1)]),
    ("Literacy", "Ability to read", "Strength", "Diplomacy", [("Modifier", 1)]),
    ("Luck", "Chance to have things turn your way against all odds", "Strength", "Diplomacy", [("Chance", 1)]),
    ("Resist frost", "Ability to resist frost damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist flame", "Ability to resist flame damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist shadow", "Ability to resist shadow damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist holy", "Ability to resist holy damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist poison", "Ability to resist poison damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist blunt", "Ability to resist blunt damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist slashing", "Ability to resist slashing damage", "Strength", "Resistance", [("Modifier", 1)]),
    ("Resist piercing", "Ability to resist piercing damage", "Strength", "Resistance", [("Modifier", 1)])
    ]


ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

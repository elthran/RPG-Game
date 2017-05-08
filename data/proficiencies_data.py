# Name, Description, Attribute_Type, Type, [Values]
PROFICIENCY_INFORMATION = [
    ("Attack damage", "How hard you hit", "Strength", "Offense", ["Minimum", "Maximum", "Average"]),
    ("Attack speed", "How fast you attack", "Agility", "Offense", ["Speed"]),
    ("Attack accuracy", "Chance to hit", "Agility", "Offense", ["Accuracy"]),
    ("First strike", "Chance to strike first", "Agility", "Offense", ["Chance"]),
    ("Critical hit", "Ability to hit your enemy's weakspots", "Agility", "Offense", ["Chance", "Modifier"]),
    ("Defence", "Damage reduction", "Fortitude", "Defence", ["Modifier"]),
    ("Evade", "Chance to dodge", "Strength", "Defence", ["Chance"]),
    ("Parry", "Chance to parry", "Strength", "Defence", ["Chance"]),
    ("Riposte", "Chance to riposte", "Strength", "Defence", ["Chance"]),
    ("Block", "Ability to block if a shield is equipped", "Strength", "Defence", ["Chance", "Modifier"]),
    ("Stealth", "Chance to avoid detection", "Strength", "Stealth", ["Chance"]),
    ("Pickpocketing", "Chance to steal", "Strength", "Stealth", ["Chance"]),
    ("Faith", "Ability to cast spells", "Strength", "Holiness", ["Modifier"]),
    ("Bartering", "Chance to negotiate prices", "Strength", "Diplomacy", ["Chance"]),
    ("Oration", "Ability to speak", "Strength", "Diplomacy", ["Modifier"]),
    ("Knowledge", "Ability to understand", "Strength", "Diplomacy", ["Modifier"]),
    ("Literacy", "Ability to read", "Strength", "Diplomacy", ["Modifier"]),
    ("Luck", "Chance to have things turn your way against all odds", "Strength", "Diplomacy", ["Chance"]),
    ("Resist frost", "Ability to resist frost damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist flame", "Ability to resist flame damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist shadow", "Ability to resist shadow damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist holy", "Ability to resist holy damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist poison", "Ability to resist poison damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist blunt", "Ability to resist blunt damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist slashing", "Ability to resist slashing damage", "Strength", "Resistance", ["Modifier"]),
    ("Resist piercing", "Ability to resist piercing damage", "Strength", "Resistance", ["Modifier"])
    ]


ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

# Name, Description, Attribute_Type, Type, [Values]
PROFICIENCY_INFORMATION = [
    ("Attack damage", "How hard you hit", "Strength", "Offense", ["Minimum_damage", "Maximum_damage"]),
    ("Attack speed", "How fast you attack", "Agility", "Offense", ["Speed"]),
    ("Attack accuracy", "", "Agility", "Offense", ["Accuracy"]),
    ("First strike", "", "Agility", "Offense", ["First_strike"]),
    ("Critical hit", "", "Agility", "Offense", ["Critical_chance", "Critical_modifier"]),
    ("Defence", "", "Endurance", "Defence", ["test"]),
    ("Evade", "", "Strength", "Defence", ["test"]),
    ("Parry", "", "Strength", "Defence", ["test"]),
    ("Riposte", "", "Strength", "Defence", ["test"]),
    ("Block", "", "Strength", "Defence", ["test"]),
    ("Stealth", "", "Strength", "Stealth", ["test"]),
    ("Pickpocketing", "", "Strength", "Stealth", ["test"]),
    ("Faith", "", "Strength", "Holiness", ["test"]),
    ("Bartering", "", "Strength", "Diplomacy", ["test"]),
    ("Oration", "", "Strength", "Diplomacy", ["test"]),
    ("Knowledge", "", "Strength", "Diplomacy", ["test"]),
    ("Luck", "", "Strength", "Diplomacy", ["test"]),
    ("Resist frost", "", "Strength", "Resistance", ["test"]),
    ("Resist flame", "", "Strength", "Resistance", ["test"]),
    ("Resist shadow", "", "Strength", "Resistance", ["test"]),
    ("Resist holy", "", "Strength", "Resistance", ["test"]),
    ("Resist blunt", "", "Strength", "Resistance", ["test"]),
    ("Resist slashing", "", "Strength", "Resistance", ["test"]),
    ("Resist piercing", "", "Strength", "Resistance", ["test"])
]

ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

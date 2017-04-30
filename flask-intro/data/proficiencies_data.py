PROFICIENCY_INFORMATION = [
    ("Attack damage", "", "Strength", "Offense"),
    ("Attack speed", "", "Agility", "Offense"),
    ("Attack accuracy", "", "Agility", "Offense"),
    ("First strike", "", "Agility", "Offense"),
    ("Critical hit", "", "Agility", "Offense"),
    ("Defence", "", "Endurance", "Defence"),
    ("Evade", "", "Strength", "Defence"),
    ("Parry", "", "Strength", "Defence"),
    ("Riposte", "", "Strength", "Defence"),
    ("Block", "", "Strength", "Defence"),
    ("Stealth", "", "Strength", "Stealth"),
    ("Pickpocketing", "", "Strength", "Stealth"),
    ("Faith", "", "Strength", "Holiness"),
    ("Bartering", "", "Strength", "Diplomacy"),
    ("Oration", "", "Strength", "Diplomacy"),
    ("Knowledge", "", "Strength", "Diplomacy"),
    ("Resist frost", "", "Strength", "Resistance"),
    ("Resist flame", "", "Strength", "Resistance"),
    ("Resist shadow", "", "Strength", "Resistance"),
    ("Resist holy", "", "Strength", "Resistance"),
    ("Resist blunt", "", "Strength", "Resistance"),
    ("Resist slashing", "", "Strength", "Resistance"),
    ("Resist piercing", "", "Strength", "Resistance")
]

ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

PROFICIENCY_INFORMATION = [
    ("Attack damage", "", 'Strength', "Offense"),
    ("Attack speed", "", 'Unspecified', "Offense"),
    ("Attack accuracy", "", 'Unspecified', "Offense"),
    ("First strike", "", 'Unspecified', "Offense"),
    ("Critical hit", "", 'Unspecified', "Offense"),
    ("Defence", "", 'Unspecified', "Defence"),
    ("Evade", "", 'Unspecified', "Defence"),
    ("Parry", "", 'Unspecified', "Defence"),
    ("Riposte", "", 'Unspecified', "Defence"),
    ("Block", "", 'Unspecified', "Defence"),
    ("Stealth", "", 'Unspecified', "Stealth"),
    ("Pickpocketing", "", 'Unspecified', "Stealth"),
    ("Faith", "", 'Unspecified', "Holiness"),
    ("Bartering", "", 'Unspecified', "Diplomacy"),
    ("Oration", "", 'Unspecified', "Diplomacy"),
    ("Knowledge", "", 'Unspecified', "Diplomacy"),
    ("Resist frost", "", 'Unspecified', "Resistance"),
    ("Resist flame", "", 'Unspecified', "Resistance"),
    ("Resist shadow", "", 'Unspecified', "Resistance"),
    ("Resist holy", "", 'Unspecified', "Resistance"),
    ("Resist blunt", "", 'Unspecified', "Resistance"),
    ("Resist slashing", "", 'Unspecified', "Resistance"),
    ("Resist piercing", "", 'Unspecified', "Resistance")
]

ALL_PROFICIENCIES = [attrib[0].lower().replace(' ', '_') for attrib in PROFICIENCY_INFORMATION]

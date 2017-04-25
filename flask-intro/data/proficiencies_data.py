PROFICIENCY_INFORMATION = [
    ("Attack damage", "", 'Unspecified'),
    ("Attack speed", "", 'Unspecified'),
    ("Attack accuracy", "", 'Unspecified'),
    ("First strike", "", 'Unspecified'),
    ("Critical hit", "", 'Unspecified'),
    ("Defence", "", 'Unspecified'),
    ("Evade", "", 'Unspecified'),
    ("Parry", "", 'Unspecified'),
    ("Riposte", "", 'Unspecified'),
    ("Block", "", 'Unspecified'),
    ("Stealth", "", 'Unspecified'),
    ("Pickpocketing", "", 'Unspecified'),
    ("Faith", "", 'Unspecified'),
    ("Bartering", "", 'Unspecified'),
    ("Oration", "", 'Unspecified'),
    ("Knowledge", "", 'Unspecified'),
    ("Resist frost", "", 'Unspecified'),
    ("Resist flame", "", 'Unspecified'),
    ("Resist shadow", "", 'Unspecified'),
    ("Resist holy", "", 'Unspecified'),
    ("Resist blunt", "", 'Unspecified'),
    ("Resist slashing", "", 'Unspecified'),
    ("Resist piercing", "", 'Unspecified')
]

ALL_PROFICIENCIES = [attrib[0].lower().replace(' ', '_') for attrib in PROFICIENCY_INFORMATION]

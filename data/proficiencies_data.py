# Name, Description, Attribute_Type, Type, [(Values Name, Value type, (Modifiers of value))]
PROFICIENCY_INFORMATION = [
    ("Health", "How fast you attack", "Vitality", "Offense", [("Maximum", "damage", (2, 10, 5))]),
    ("Sanctity", "How fast you attack", "Divinity", "Offense", [("Maximum", "damage", (2, 10, 5))]),
    ("Storage", "How fast you attack", "Strength", "Offense", [("Maximum", "damage", (2, 10, 5))]),
    ("Endurance", "How fast you attack", "Fortitude", "Offense", [("Maximum", "damage", (2, 10, 5))]),
    ("Attack damage", "How hard you hit", "Strength", "Offense", [("Minimum", "damage", (0.5, 0.3, 1.5)), ("Maximum",  "damage", (0.6, 0.3, 1.5)), ("Average",  "damage", (0.55, 0.3, 1.5))]),
    ("Attack speed", "How fast you attack", "Agility", "Offense", [("Speed", "percent", (2, 10, 5))]),
    ("Attack accuracy", "Chance to hit", "Agility", "Offense", [("Accuracy", "percent", (2, 10, 5))]),
    ("First strike", "Chance to strike first", "Agility", "Offense", [("Chance", "percent", (2, 10, 5))]),
    ("Critical hit", "Ability to hit your enemy's weakspots", "Perception", "Offense", [("Chance", "percent", (2, 10, 5)), ("Modifier", "percent", (2, 10, 5))]),
    ("Defence", "Damage reduction", "Fortitude", "Defence", [("Modifier", "percent", (2, 10, 5))]),
    ("Evade", "Chance to dodge", "Reflexes", "Defence", [("Chance", "percent", (2, 10, 5))]),
    ("Parry", "Chance to parry", "Reflexes", "Defence", [("Chance", "percent", (2, 10, 5))]),
    ("Riposte", "Chance to riposte", "Agility", "Defence", [("Chance", "percent", (2, 10, 5))]),
    ("Block", "Ability to block if a shield is equipped", "Strength", "Defence", [("Chance", "percent", (2, 10, 5)), ("Modifier", "percent", (2, 10, 5))]),
    ("Stealth", "Chance to avoid detection", "Perception", "Stealth", [("Chance", "percent", (2, 10, 5))]),
    ("Pickpocketing", "Chance to steal", "Agility", "Stealth", [("Chance", "percent", (2, 10, 5))]),
    ("Faith", "Ability to cast spells", "Divinity", "Holiness", [("Modifier", "percent", (2, 10, 5))]),
    ("Bartering", "Chance to negotiate prices", "Charisma", "Diplomacy", [("Chance", "percent", (2, 10, 5))]),
    ("Oration", "Ability to speak", "Strength", "Wisdom", [("Modifier", "percent", (2, 10, 5))]),
    ("Knowledge", "Ability to understand", "Wisdom", "Diplomacy", [("Modifier", "percent", (2, 10, 5))]),
    ("Literacy", "Ability to read", "Wisdom", "Diplomacy", [("Modifier", "percent", (2, 10, 5))]),
    ("Luck", "Chance to have things turn your way against all odds", "Fortuity", "Diplomacy", [("Chance", "percent", (2, 10, 5))]),
    ("Resist frost", "Ability to resist frost damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist flame", "Ability to resist flame damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist shadow", "Ability to resist shadow damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist holy", "Ability to resist holy damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist poison", "Ability to resist poison damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist blunt", "Ability to resist blunt damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist slashing", "Ability to resist slashing damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))]),
    ("Resist piercing", "Ability to resist piercing damage", "Resilience", "Resistance", [("Modifier", "percent", (2, 10, 5))])
    ]


ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]

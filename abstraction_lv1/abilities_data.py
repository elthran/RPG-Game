ALL_ABILITIES = [
    ("scholar", "AuraAbility",
     "AuraAbility('scholar', 5, 'Gain +1% experience gain per level', locked=False, understanding_modifier=1)"),
    ("reflexes", "AuraAbility",
     "AuraAbility('reflexes', 3, 'Gain +2% dodge chance per level', locked=False, evade_chance=2)"),
    ("cure", "CastableAbility",
    "CastableAbility('cure', 3, 'Recover 3 health', sanctity_cost=1, heal_amount=3)"),
    ("testgold", "CastableAbility",
     "CastableAbility('testgold', 3, 'Gain 3 gold', locked=False, endurance_cost=1, gold_amount=3)"),
    ("gainexp", "CastableAbility",
     "CastableAbility('gainexp', 3, 'Gain 3 gold', locked=False, archetype='priest', endurance_cost=1, gold_amount=73)")
]

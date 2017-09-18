"""
Abilities spec goes:

name, class, class arguments (not including name as it is added later).
"""

ALL_ABILITIES = [
    ("scholar", "AuraAbility", "5, 'Gain +1% experience gain per level', learnable=True, understanding_modifier=1"),
    ("reflexes", "AuraAbility", "3, 'Gain +2% dodge chance per level', learnable=True, evade_chance=2"),
    ("cure", "CastableAbility", "3, 'Recover 3 health', learnable=True, tree='archetype', tree_type='priest', sanctity_cost=1, heal_amount=3"),
    ("free_gold", "CastableAbility", "3, 'Gain 3 gold', learnable=True, tree='archetype', tree_type='merchant', endurance_cost=1, gold_amount=3")
]


ABILITY_NAMES = [key[0] for key in ALL_ABILITIES]

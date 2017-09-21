"""
{% raw %}
Abilities spec goes:

name, class, class arguments (not including name as it is added later).
"""

ALL_ABILITIES = [
    ("scholar", "AuraAbility", "5, 'Gain +{{ level }}% experience per level', learnable=True, understanding_modifier=1"),
    ("reflexes", "AuraAbility", "3, 'Gain +{{ level * 2 }}% dodge chance per level', learnable=True, evade_chance=2"),
    ("meditation", "AuraAbility", "10, 'Regenerate 1 sanctity per day', tree='archetype', tree_type='cleric', sanctity_regeneration=1"),
    ("explorer", "AuraAbility", "3, 'See 1x more detail when moving to a new place on the map per level', tree='archetype', tree_type='woodsman', map_reveal=1"),
    ("cure", "CastableAbility", "3, 'Recover 3 health per level', tree='specialization', tree_type='priest', sanctity_cost=1, heal_amount=3"),
    ("beastmaster", "AuraAbility", "5, 'Take 5% reduced damage from beasts per level', tree='specialization', tree_type='hunter', beast_damage_reduction=5")
]


ABILITY_NAMES = [key[0] for key in ALL_ABILITIES]

"""
End of documentation.
{% endraw %}
"""

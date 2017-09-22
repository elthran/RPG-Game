"""
{% raw %}
Abilities spec goes:

name, class, class arguments (not including name as it is added later).
"""

ALL_ABILITIES = [
    ("scholar", "AuraAbility", "5, 'Gain experience {{ level }}% faster.', learnable=True, understanding_modifier=1"),
    ("reflexes", "AuraAbility", "3, 'You are {{ level * 2 }}% more likely to dodge enemy attacks.', learnable=True, evade_chance=2"),
    ("meditation", "AuraAbility", "10, 'Regenerate {{ level }} sanctity per day.', tree='archetype', tree_type='ascetic', sanctity_regeneration=1"),
    ("explorer", "AuraAbility", "3, '??? each level needsa decsription, not an integer', tree='archetype', tree_type='woodsman', map_reveal=1"),
    ("cure", "CastableAbility", "3, 'Recover {{ level * 3 }} health at the cost of {{ level }} sanctity.', tree='calling', tree_type='priest', sanctity_cost=1, heal_amount=3"),
    ("beastmaster", "AuraAbility", "5, 'Take {{ level * 5 }}% reduced damage from beasts.', tree='calling', tree_type='hunter', beast_damage_reduction=5")
]


ABILITY_NAMES = [key[0] for key in ALL_ABILITIES]

"""
End of documentation.
{% endraw %}
"""

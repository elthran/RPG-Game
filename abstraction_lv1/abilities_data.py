"""
{% raw %}
Abilities spec goes:

name, class, class arguments (not including name as it is added later).

relentless = ALL_ABILITIES[0]
name = relentless[0]
type = relentless[1]
args = relentless[2]

level_up_func = relentless[3]
This last one ends up in the form

@orm.validates('level')
def validate_level(self, key, current):
    for key in self.proficiencies:
        prof = self.proficiencies[key]
        prof.base = current {{ level_up_func }}
        # in this case:
        prof.base = current * 5
"""

ALL_ABILITIES = [
    ("Relentless",
        "AuraAbility",
        "5, 'Gain {{ level * 5 }} maximum health. Master this ability to unlock the Brute archetype.', learnable=True, proficiency_data=[('Health', {'base': 5}),]",
        '* 5'),
    ("Trickster", "AuraAbility", "5, 'Become {{ level * 5 }}% harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.', learnable=True, stealth_chance=5"),
    ("Discipline", "AuraAbility", "5, 'Gain devotion {{ level * 5 }}% faster. Master this ability to unlock the Ascetic archetype.', learnable=True"),
    ("Traveler", "AuraAbility", "5, 'Reveal {{ level * 10 }}% more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.', learnable=True"),
    ("Arcanum", "AuraAbility", "5, 'Gain {{ level * 3 }} maximum sanctity. Master this ability to unlock the Philosopher archetype.', learnable=True, sanctity_maximum=3"),
    ("Poet", "AuraAbility", "5, 'Gain fame {{ level * 5 }}% faster. Master this ability to unlock the Opportunist archetype.', learnable=True"),
    ("Blackhearted", "AuraAbility", "3, 'Lose virtue {{ level * 5 }}% faster.', tree='archetype', tree_type='scoundrel'"),
    ("Backstab", "AuraAbility", "3, 'You are {{ level * 15 }}% more likely to attack first in combat.', tree='archetype', tree_type='scoundrel', firststrike_chance=15"),
    ("MartialArts", "AuraAbility", "3, 'You deal {{ level * 5 }}% more damage in combat.', tree='archetype', tree_type='ascetic'"),
    ("Apprentice", "AuraAbility", "3, 'You are capable of learning level {{ level }} spells.', tree='archetype', tree_type='ascetic'"),
    ("Meditation", "AuraAbility", "3, 'Regenerate {{ level }} sanctity per day.', tree='archetype', tree_type='ascetic', sanctity_regeneration=1"),
    ("Bash", "AuraAbility", "3, 'You deal {{ level * 10 }}% more damage with blunt weapons.', tree='archetype', tree_type='brute'"),
    ("Student", "AuraAbility", "3, 'You are capable of learning level {{ level }} spells.', tree='archetype', tree_type='philosopher'"),
    ("Scholar", "AuraAbility", "3, 'Gain experience {{ level }}% faster.', learnable=True, tree='archetype', tree_type='philosopher', understanding_modifier=1"),
    ("Vigilance", "AuraAbility", "3, 'You are {{ level * 10 }}% less likely to be ambushed.', tree='archetype', tree_type='survivalist'"),
    ("Strider", "AuraAbility", "3, 'Traveling on the map requires {{ level * 10 }}% less endurance.', tree='archetype', tree_type='survivalist'"),
    ("Skinner", "AuraAbility", "3, 'You have a {{ level * 5 }}% chance of obtaining a usable fur after kiling a beast.', tree='archetype', tree_type='survivalist'"),
    ("Charmer", "AuraAbility", "3, 'You are {{ level * 5 }}% more likely to succeed when choosing charm dialogues.', tree='archetype', tree_type='opportunist'"),
    ("Haggler", "AuraAbility", "3, 'Prices at shops are {{ level * 3}}% cheaper.', tree='archetype', tree_type='opportunist'")
]
"""
End of abilities_data.py.
{% endraw %}
"""

"""
{% raw %}
Abilities spec goes:

name, class, class arguments (not including name as it is added later).

relentless = ALL_ABILITIES[0]
name = relentless[0]
type = relentless[1]
args = relentless[2]

NOTE:
    proficiency_data gets parsed by:
# Initialize proficiencies
# Currently doesn't add any proficiencies.
for class_name, arg_dict in proficiency_data:
    Class = getattr(proficiencies, class_name)
    # pdb.set_trace()
    obj = Class(**arg_dict)
    self.proficiencies[obj.name] = obj

Such each element must be a list of tuples:
Each tuple should have element 1 be the class name (Health)
Each tuple should have an element 2 be an arg dict corresponding to the
Proficiency argment dict ... this is expanded so that it will read
e.g.
    hero.abilities.relentless.proficiencies['health'] = Health(base=5)
which is an entirely different object than:
    hero.proficiencies['health']
"""

import pandas


profs = pandas.read_csv('abilities.csv', dtype={'Name': str, "Description": str})  #You can declare each column's data type
ABILITY_INFORMATION = []
for i, row in enumerate(profs.itertuples(), 1):
    ABILITY_INFORMATION.append((row.Name, row.Type, row.Maximum, row.Description, row.Learnable, row.Prof1, row.Value1))

for ability in ABILITY_INFORMATION:
    print(ability)

ALL_ABILITIES = [
    ("Relentless", "AuraAbility", "5, 'Gain {{ level * 5 }} maximum health. Master this ability to unlock the Brute archetype.', learnable=True, proficiency_data=[('Health', {'base': 5}),]"),
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

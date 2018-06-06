import models


def cast_spell(hero, data=None, *args, **kwargs):
    spell_id = data['id']
    spell = models.abilities.Ability.get(spell_id)
    print("Casting spell called ", spell.name, "with spell id of ", spell.id)
    spell.cast(hero)
    return "success"

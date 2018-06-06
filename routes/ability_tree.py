import flask

from elthranonline import app
import services.decorators
import models


@app.route('/ability_tree/<spec>')
@services.decorators.uses_hero
def ability_tree(spec, hero=None):
    # for prof in hero.get_summed_proficiencies():
    #     if prof.name == "stealth" or prof.name == "health":
    #         print(prof,"\n")

    # On the archetype page, but the hero doesn't have one!
    if spec == "archetype" and hero.specializations.archetype is None:
        page_title = "Archetype Abilities"
        become_type = "archetype"
        spec_choices = models.Archetype.query.all()

        # For testing!
        if not hero.specialization_access:
            philosopher = models.Archetype.filter_by(name="Philosopher").one()
            hero.set_specialization_access(philosopher)
            hero.specialization_access[philosopher.id].hidden = False
            models.Base.quick_save()

    # On the archetype page, but the hero doesn't have one!
    elif spec == "calling" and hero.specializations.calling is None:
        page_title = "Calling Abilities"
        become_type = "calling"
        spec_choices = models.Calling.query.all()

    # On the archetype page, but the hero doesn't have one!
    elif spec == "pantheon" and hero.specializations.pantheon is None:
        page_title = "Pantheon Abilities"
        become_type = "pantheon"
        spec_choices = models.Pantheon.query.all()
    else:
        page_title = "Basic Abilities"
        become_type = None
        spec_choices = []

    all_abilities = []
    for ability in hero.abilities:
        if ability.hidden is False and ability.tree == spec.title():  # This checks if the ability is the correct basic/archetpe/calling/pantheon
            if spec == "basic":  # If its basic then it passed and always gets added
                all_abilities.append(ability)
            elif spec == "archetype" and hero.specializations.archetype:  # If it's archetype and the hero has chosen an archetype...
                if hero.specializations.archetype.name == ability.tree_type:  # If the chosen archetype matches the ability's archetype add it
                    all_abilities.append(ability)

    return flask.render_template('profile_ability.html', page_title=page_title, hero=hero, ability_tree=spec, all_abilities=all_abilities, becomeType=become_type, spec_choices=spec_choices)

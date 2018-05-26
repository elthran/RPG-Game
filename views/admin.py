import pdb

import flask

from elthranonline import app
import services.decorators
import services.fetcher
import models
import controller.setup_account


@app.route('/admin/<path>/<path2>', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
@services.decorators.login_required
@services.decorators.uses_hero
def admin(path="modify_self", path2="users", hero=None):
    if not hero.account.is_admin:  # Prevent tampering
        return flask.redirect(flask.url_for('logout'))

    admin_form_mapping = [
            ("Age", "hero.age"),
            ("Experience", "hero.experience"),
            ("Experience Maximum", "hero.experience_maximum"),
            ("Renown", "hero.base_proficiencies['renown'].current"),
            ("Virtue", "hero.base_proficiencies['virtue'].current"),
            ("Devotion", "hero.base_proficiencies['devotion'].current"),
            ("Gold", "hero.gold"),
            ("Basic Ability Points", "hero.basic_ability_points"),
            ("Archetype Ability Points", "hero.archetype_ability_points"),
            ("Calling Ability Points", "hero.calling_ability_points"),
            ("Pantheon Ability Points", "hero.pantheon_ability_points"),
            ("Attribute Points", "hero.attribute_points"),
            ("Proficiency Points", "hero.proficiency_points")]
    if path == "edit_database":
        sorted_heroes = services.fetcher.fetch_sorted_heroes("id", False)
        return flask.render_template('admin.html', page_title="Admin", hero=hero, path=path, path2=path2, all_heroes=sorted_heroes)  # return a string
    elif path == "modify_self":
        page_title = "Admin"
        if flask.request.method == 'POST':
            # get("var", None(default), type=int)
            # supports type casting and default values.
            for key, attrib in admin_form_mapping:
                exec("{} = {}".format(attrib, flask.request.form.get(key, type=int)))  # Should be secure as user input is type cast to int before evaluating?
            hero.refresh_character(full=True)
            return flask.redirect(flask.url_for('home'))
    elif path == "add_new_character":
        account = models.Account.get(flask.session['id'])
        controller.setup_account.add_new_hero_to_account(account)
        return flask.redirect(flask.url_for('choose_character'))
    form_content = [(key, eval(attrib, {'hero': hero})) for key, attrib in admin_form_mapping]
    return flask.render_template('admin.html', page_title="Admin", hero=hero, form_content=form_content, path=path)  # return a string

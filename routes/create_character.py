import flask

from elthranonline import app
import services.decorators
import controller


@app.route('/create_character', methods=['GET', 'POST'])
@services.decorators.uses_hero
def create_character(hero=None):
    data = {}

    # This should prevent anyone getting here if they haven't been sent
    # by the login -> create account code.
    if not hero.creation_phase:
        return flask.redirect(flask.url_for('home'))
    # Accept regular or json form data.
    if flask.request.method == 'POST':
        if flask.request.is_json:
            data = flask.request.get_json()
            if 'form' in data:
                flask.request.form = data['form']
        if hero.name is None:
            hero.name = flask.request.form["get_data"].title()
        elif hero.background is None:
            hero.background = data["response"]
            if hero.background == "Barbarian":
                hero.attributes.brawn.level += 1
            elif hero.background == "Missionary":
                hero.attributes.intellect.level += 1

    if hero.name is None:
        page_image = "beached"
        generic_text = "You awake to great pain and confusion as you hear footsteps approaching in the sand. Unsure of where you are, you quickly look around for something to defend yourself. A firm and inquisitive voice pierces the air."
        npc_text = [("Stranger", "Who are you and what are you doing here?")]
        account_action = "get text"
        account_response = "...I don't remember what happened. My name is"
        account_text_placeholder = "Character Name"
    elif hero.background is None:
        # This is needed if the account names there hero but leaves the page and returns later. But I will write it out later.
        page_image = "character_background"
        generic_text = ""
        account_text_placeholder = ""
        npc_text = [("Stranger", "Where do you come from, child?")]
        account_action = "make choice"
        account_response = [
            ("My father was a great warlord from the north.", ["Gain", ("+1 Brawn",)], "Barbarian"),
            ("My father was a great missionary traveling to the west.", ["Gain", ("+1 Intellect",)], "Missionary")]
    else:
        controller.close_hero_creation_phase(hero)
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('generic_dialogue.html', page_image=page_image, generic_text=generic_text, npc_text=npc_text, account_action=account_action, account_response=account_response, account_text_placeholder=account_text_placeholder)

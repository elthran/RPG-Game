import flask


def turn_spellbook_page(hero, data=None, *args, **kwargs):
    page_max = data['max']
    if data['direction'] == "forward":
        hero.spellbook_page = min(hero.spellbook_page+1, page_max)
    else:
        hero.spellbook_page = max(hero.spellbook_page-1, 1)
    # The code below determines which spells to show based on what page you are on (up to 8 spells).
    spells = []
    for ability in hero.abilities:
        if ability.castable and ability.level > 0:
            spells.append(ability)
    first_index = (hero.spellbook_page - 1) * 8
    if len(spells) <= first_index + 8:
        last_index = first_index + ((len(spells) - 1) % 8) + 1
    else:
        last_index = first_index + 8
    # The code below extracts the data from the shown spells to send to JavaScript.
    spell_ids = []
    spell_imgs = []
    spell_infos = []
    for i in range(first_index, last_index):
        spell_ids.append(spells[i].id)
        spell_imgs.append(spells[i].image)
        spell_infos.append("<h1>" + spells[i].name.title() + "</h1><h2>" + spells[i].description + "</h2>")
    for i in range(8 - (last_index - first_index)):
        spell_ids.append(0)
        spell_imgs.append("empty_box")
        spell_infos.append(" ")
    for i in range(8):
        print(spell_ids[i], spell_imgs[i], spell_infos[i])
    return flask.jsonify(page=hero.spellbook_page, page_max=page_max, spell_ids=spell_ids, spell_imgs=spell_imgs, spell_infos=spell_infos)

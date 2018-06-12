from elthranonline import app


@app.template_filter()
def validate_hero_image(hero):
    """Used to handle an expected/possible error in the template.

    See https://codenhagen.wordpress.com/2015/08/20/custom-jinja2-template-filters-and-flask/
    """
    # pdb.set_trace()
    image_name = ''
    try:
        image_name = "archetype_{}.jpg".format(hero.archetype.lower())
    except AttributeError:
        image_name = "character.jpg"
    return image_name


@app.template_filter()
def validate_hero_name(hero):
    return hero.name if hero.name else "UnNamed"

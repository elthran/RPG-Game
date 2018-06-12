def update_attribute(hero, arg_dict=None, *args, **kwargs):
    attribute_id = arg_dict.get('data', None, type=int)
    if hero.attribute_points <= 0:
        return "error: no attribute points"
    for attribute in hero.attributes:
        if attribute.id == attribute_id:
            attribute.level += 1
    hero.attribute_points -= 1
    if hero.attribute_points == 0:
        return "hide_all".format()
    return "success".format()

def change_attribute_tooltip(hero, arg_dict=None, *args, **kwargs):
    """I want to pass in the actual attribute here instead of the description.

    That way I can assign the attribute name and description to the tooltip.
    Unfortunately, I don't know how to pull the attribute object from the
    database. I need a get_attribute_by_name() function in
    connect_to_database.py
    """

    tooltip = arg_dict.get('data', None, type=str)
    return "{}".format(tooltip)

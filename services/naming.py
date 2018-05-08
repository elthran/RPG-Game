def fix_camel_case(name):
    """Detect and fix camel case names.

    Otherwise these names will be lost when converting to 'title()'.
    """
    if name[0].isupper() and name[1:].islower():
        return name
    # print("Bad name:", name)
    fixed_name = name[0] + ''.join([" " + letter.lower()
                                    if (index > 0 and letter.isupper())
                                    else letter
                                    for index, letter in enumerate(name[1:])])
    # print("Fixed name:", fixed_name)
    return fixed_name


def get_names(names):
    """Pull the first item from a more complex list of data.

    Fix the naming scheme if it use camel case an use human readable instead.
    """
    sorted_names = sorted([name[0] for name in names])
    return [fix_camel_case(name) for name in sorted_names]


def normalize_attrib_name(name):
    """Normalize name to Python attribute style.

    Convert "First strike" to "first_strike"
    """
    return fix_camel_case(name).lower().replace(" ", "_")


def normalize_attrib_names(names):
    """Normalize names for columns."""
    return [normalize_attrib_name(name) for name in names]


def normalize_class_name(name):
    """Normalized name for class."""
    return fix_camel_case(name).title().replace(" ", "")


def normalize_class_names(names):
    """Normalized names for classes."""
    return [normalize_class_name(name) for name in names]

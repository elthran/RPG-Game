import pdb

import sqlalchemy as sa

import models


def get_user_id(username):
    """Return the id of the user by username from the User's table.

    """
    user = models.Account.filter_by(username=username).first()
    if user is None:
        return None
    return user.id


def fetch_sorted_heroes(attribute, descending=False):
    """Return a list of all heroes sorted by attribute.

    :param attribute: an attribute of the Hero object.
    :param descending: the desired direction for the sorted list
        ascending/descending
    :return: list sorted by attribute.

    NOTE: this code is not very flexible. If you tried to access
    hero.inventory.id it would not work.

    A more generic function might do:
    extended_attr, attr = attribute.split('.')
    join_attr = getattr(Hero, extended_attr)?
    self.session.query(Hero).join(join_attr).order_by(attr).all()

    NOTE: to order by descending:
    order_by(attribute + " desc")
    or
    order_by(desc(attribute))

    Former does not work for numbers

    https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
    """
    query = models.Hero.query
    if '.' not in attribute:
        if descending:
            return query.order_by(sa.desc(attribute)).all()
        return query.order_by(attribute).all()

    all_attrs = attribute.split('.')
    sort_attr = all_attrs.pop()  # Remove last value for use as sort key
    try:
        join_attr = getattr(models.Hero, all_attrs.pop(0))  # remove first attr
        for extended_attr in all_attrs:
            join_attr = getattr(join_attr, extended_attr)
    except AttributeError:
        raise Exception("Trying to access an attribute that this code"
                        " does not accommodate.")
    joined_query = query.join(join_attr)
    heroes = []
    if descending:
        heroes = joined_query.order_by(sa.desc(sort_attr)).all()
    else:
        heroes = joined_query.order_by(sort_attr).all()
    return heroes if heroes else models.Hero.all()


def fetch_hero_by_username(username, character_name=None):
    """Return hero objected based on username_or_id and character_name.

    If no character_name is passed just return first hero.
    Note: Providing a username when you have the hero/character id is
    redundant.
    """
    account = models.Account.filter_by(username=username).one()
    if character_name is not None:
        return models.Hero.filter_by(
            account_id=account.id, character_name=character_name).one()
    return account.heroes[0]


def get_all_monsters_by_hero_terrain(hero):
    """Return all monster template that fit the hero's terrain type."""
    if hero.current_terrain is None:
        return models.Hero.filter_by(is_monster=True, template=True).all()
    else:
        terrain = getattr(models.Hero, hero.current_terrain)
        return models.Hero.filter_by(is_monster=True, template=True).filter(terrain == True).all()


def hero_has_quest_path_named(hero, name):
    """Returns True if hero has a ques_path of the given name.

    If hero has 2 quest_paths of the same name it throws an error.
    """
    quest = models.QuestPath.filter_by(name=name, journal_id=hero.journal.id).one_or_none()

    if quest:
        return True
    return False


def get_quest_path_template(name):
    """Return the quest path template of the given name."""
    return models.QuestPath.filter_by(name=name, template=True).one()


def get_other_heroes_at_current_location(hero):
    """Return a list of heroes at the same location as this one.

    Not including self.
    This is probably inefficient ...
    """
    return [other_hero for other_hero in hero.current_location.heroes_by_current_location if other_hero.id != hero.id]

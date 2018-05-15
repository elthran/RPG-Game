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
    if '.' not in attribute:
        if descending:
            return models.Hero.query().order_by(sa.desc(attribute)).all()
        else:
            return models.Hero.query().order_by(attribute).all()
    elif attribute.startswith('account'):
        _, attribute = attribute.split('.')
        if descending:
            return models.Hero.query().join(models.Hero.account).order_by(sa.desc(attribute)).all()
        else:
            return models.Hero.query().join(models.Hero.account).order_by(attribute).all()
    else:
        raise Exception("Trying to access an attribute that this code"
                        " does not accommodate.")

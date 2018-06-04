import random

import models


def generate_monster(monsters=()):
    """Generate a random monster from passed list or all monsters.

    If ran with no input generate a monster from all monsters.
    """
    monsters = monsters if monsters else models.Hero.filter_by(is_monster=True, template=True).all()
    return random.choice(monsters).clone()


def get_random_item():
    """Return a new random item."""
    num_rows = models.Item.count()
    item_id = random.randint(1, num_rows)
    item = create_item(item_id)
    return item


def create_item(template_id):
    """Create a new item from a given template name.

    Autocommit using @safe_commit_session.
    """
    template = models.Item.get(template_id)
    item = template.clone()

    # TODO migrate away from having to visibly use sessions.
    models.Base.session.add(item)
    models.Base.quick_save()
    return item

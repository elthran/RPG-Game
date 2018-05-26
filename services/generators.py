import random

import models


def generate_monster(monsters=()):
    """Generate a random monster from passed list or all monsters.

    If ran with no input generate a monster from all monsters.
    """
    monsters = monsters if monsters else models.Hero.filter_by(is_monster=True).all()
    return random.choice(monsters)

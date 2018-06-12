import models


def consume_item(hero, arg_dict=None, *args, **kwargs):
    """Apply the effect of a potion when the hero consumes it.

    NOTE: the item is then deleted from the hero's inventory and the database.
    """
    item_id = arg_dict.get('data', None, type=int)
    item = models.Item.get(item_id)
    item.apply_effect(hero)
    item.delete()
    return "success"

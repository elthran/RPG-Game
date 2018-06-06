import flask

import commands.decorators
import services.event_service
import services.generators


@commands.decorators.set_notification_active
def buy_item(hero, data=None, *args, **kwargs):
    """Allow the hero to buy items from the Blacksmith.

    Returns an error if the character doesn't have enough gold.
    """
    item_id = data['id']
    location = data['location']
    item = services.generators.create_item(item_id)
    if hero.gold >= item.buy_price:
        hero.inventory.add_item(item)
        hero.gold -= item.buy_price
        services.event_service.spawn(
            'buy_event',
            hero,
            description="{} buys a/an {}.".format(hero.name, item.name)
        )
        return flask.jsonify(
            message="Purchased: {}: id={}".format(item.name, item.id),
            heroGold=hero.gold)
    return flask.jsonify(error="Not enough gold to buy '{}'!".format(item.name))

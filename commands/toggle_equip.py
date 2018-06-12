import flask

import commands.decorators
import services.event_service
import models


@commands.decorators.set_notification_active
def toggle_equip(hero, data=None, *args, **kwargs):
    item_id = data['id']
    item = models.Item.get(item_id)
    len_rings = None
    if item.type == "Ring":
        lowest_empty_slot = hero.inventory.get_lowest_empty_ring_pos()
        primary_slot_type = "finger-{}".format(lowest_empty_slot)
    else:
        primary_slot_type = hero.inventory.\
            js_slots_used_by_item_type[item.type][0]
    if item.equipped:
        hero.inventory.unequip(item)
        hero.refresh_character()
        services.event_service.spawn(
            'unequip_event',
            hero,
            description="{} unequips a/an {}.".format(hero.name, item.name)
        )
        return flask.jsonify(primarySlotType=primary_slot_type, command="unequip")
    else:
        ids_to_unequip = hero.inventory.equip(item)
        hero.refresh_character()
        services.event_service.spawn(
            'equip_event',
            hero,
            description="{} equips a/an {}.".format(hero.name, item.name)
        )
        return flask.jsonify(primarySlotType=primary_slot_type, command="equip", idsToUnequip=ids_to_unequip)

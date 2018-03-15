from events import Trigger, Condition
from locations import Location


class TestTrigger:
    def setup(self):
        self.blacksmith = Location('Blacksmith', 'store')
        self.blacksmith_condition = Condition('current_location', '==', self.blacksmith)
        self.blacksmith_is_parent_of_current_location_condition = Condition('current_location.parent', '==', self.blacksmith)
        self.visit_blacksmith_trigger = Trigger('move_event', conditions=[self.blacksmith_condition], extra_info_for_humans='Should activate when the hero.current_location.id == the id of the blacksmith object.')

    def test_init(self):
        buy_item_from_blacksmith_trigger = Trigger(
            'buy_event',
            conditions=[self.blacksmith_is_parent_of_current_location_condition],
            extra_info_for_humans='Should activate when buy code runs and '
                                  'hero.current_location.id == id of the blacksmith.'
        )

        assert buy_item_from_blacksmith_trigger.pretty == """
<Trigger(
completed=False
conditions='[<Condition(id=None)>]'
event_name='buy_event'
extra_info_for_humans='Should activate when buy code runs and hero.current_location.id == id of the blacksmith.'
hero=None
hero_id=None
id=None
template=True
)>
"""

        equip_item_trigger = Trigger(
            'equip_event',
            conditions=[],
            extra_info_for_humans="Should activate when equip_event spawns."
        )

        assert equip_item_trigger.pretty == """
<Trigger(
completed=False
conditions=[]
event_name='equip_event'
extra_info_for_humans='Should activate when equip_event spawns.'
hero=None
hero_id=None
id=None
template=True
)>
"""

        unequip_item_trigger = Trigger(
            'unequip_event',
            conditions=[],
            extra_info_for_humans="Should activate when unequip_event spawns."
        )

        assert unequip_item_trigger.pretty == """
<Trigger(
completed=False
conditions=[]
event_name='unequip_event'
extra_info_for_humans='Should activate when unequip_event spawns.'
hero=None
hero_id=None
id=None
template=True
)>
"""

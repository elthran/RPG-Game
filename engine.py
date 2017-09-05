"""
This file will become very important. I would like to switch to handling
events here. And everything else that the User doesn't need to know about.
"""

from events import Event
from pprint import pprint


class Engine:
    def __init__(self, database):
        self.db = database
        # self.events = {}
        # self.handlers = {}

        # move_event = Event('move_event', locals(), "The Hero visits a store.")
        # self.add_event(move_event)

    # def add_event(self, event):
    #     self.events[event.name] = event
    #
    # def add_handler(self, handler):
    #     self.handlers[handler.name] = handler

    def spawn(self, event_name, hero, *args, description=None):
        """Create and handle an event.

        Example:
        Engine.spawn('move_event', hero, "The Hero visits a store.")
            --> which then will build an event
        Event('move_event', hero, description=description)
            --> The event will then check if any triggers exist for this
            event type.
        In this case the previously created trigger:
            --> Trigger("hero.current_location.name == 'Blacksmith'")
        Will be found and handled.

        Now that I have an move event (for getting to the blacksmith) I
        want it to check to see if it triggers any other events.
        It should trigger a "visit the blacksmith quest completion event"
        And complete this quest.
        """
        pprint(locals())
        event = Event(event_name, hero_id=hero.id, description=description)
        self.db.add_object(event)
        triggers = self.db.get_all_triggers_by(event_name, hero.id)
        for trigger in triggers:
            trigger.evaluate()

        # TODO ... what objects? and what this piece of code is supposed to do.
        # I mean really? What am I trying to accomplish here?
        # I need to respec this and then it will work ...?
        # In this case should return and quest_path?
        objects = self.db.get_all_objects_with_completed_triggers(hero)
        # return the "Blacksmith" quest object ...
        # Since its completion trigger is completed ...
        # It is now completed. Run the method that you run when trigger
        # completes.
        for obj in objects:
            obj.run_if_trigger_completed()

    def on_move(self, handler, location):
        pass

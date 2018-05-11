"""
This file will become very important. I would like to switch to handling
events here. And everything else that the User doesn't need to know about.
"""
import time
from multiprocessing import Process

import werkzeug.serving

import models
import models.database
import private_config


def spawn(event_name, hero, *args, description=None):
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
    # pdb.set_trace()
    event = models.Event(event_name, hero_id=hero.id, description=description)
    models.Base.session.add(event)

    # return the "Blacksmith" quest object ...
    # Since its completion trigger is completed ...
    # It is now completed. Run the method that you run when trigger
    # completes.
    for handler in hero.handlers:
        # print("A handler with a completed trigger!")
        # handler.pprint()
        if handler.evaluate(event):
            handler.run()


def game_clock(database):
    """Run the update all heroes code every x seconds."""
    if not werkzeug.serving.is_running_from_reloader():
        while True:
            time.sleep(private_config.UPDATE_INTERVAL)
            database.update_time_all_heroes()


# Maybe make this a decorator?
def async_process(func, args=(), kwargs=None):
    """Start a new asynchronous process.

    These processes might respawn if the server restarts.
    """
    kwargs = {} if kwargs is None else kwargs  # Might not be needed?
    Process(target=func, args=args, kwargs=kwargs).start()


@models.database.sessions.scoped_session
def rest_key_timelock(database, username, timeout=5):
    """Erase the user reset key after x minutes."""

    # pdb.set_trace()
    timeout *= 60  # Convert minute time to seconds required by time.sleep.
    time.sleep(timeout)
    user = database.get_user_by_username(username)
    user.reset_key = None


if __name__ == "__main__":
    import os
    os.system("python3 -m pytest -vv rpg_game_tests/test_{}".format(__file__))
    exit()  # prevents code from trying to run file afterwards.

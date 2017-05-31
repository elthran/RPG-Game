"""
Event specification:
    -use the app.py <cmd> code.
    -transition to using a "game engine" kind of interface.
    -describe the action, person, place and thing.
    -some actions may not have a person. 
        e.g. "leaving town" would have an action "move", a place "current_location" and
            a thing "location_moving_to"
    -an event should occur whenever the User interacts with the game.
        i.e. mainly <button> and <a> tags.
    
Format:
    -<button class="command" name="consume" data="{{ item.id }}" data-function="functionName">
        AnyHTML you want.</button>
    -Where class="command" means this object runs command code.
    -Where data is the items database id or any other data you want to send.
        Id is just the simplest.
    -Where Consume is the buttons command identifier (the command function to run).

Old Format:
    -<button class="command" data="{{ item.id }}" data-function="functionName">Consume</button>
    -<button class="command" data="{{ item.id }}" onClick="remove(this)">Consume</button>
    -Where class="command" means this object runs command code.
    -Where data is the items database id.
    -Where Consume is the buttons command identifier (the command function to run).
    -Where data-function is the name of a function that can be sent data from the python
        code. This function runs after the python code returns a response. onClick
        does not. It runs first/or independantly?
    -Where onClick is a local function to run. "this" is the button object itself.
        
This should be used to create and event object such that:
    >>> event = Event(request.args)
    
    >>> event
    Event<(action: 'buy', location: ['World', 'Thornwall', 'Blacksmith'],
        person: "Steve_The_Blacksmith", thing: "Medium Helmet")>
    >>> event.action
    'buy'

Events should active triggers .. or maybe they are the same thing.

#Usage of trigger/events with Quests
use triggers .... build a game engine :P
Thus to advance a quest you would spawn an event any time the hero did anything
and the engine would check the events data against each quest. Any quest that 
met the requirements of this trigger would advance.
eg. Trigger for "Talk to the Blacksmith" quest would be:
    t1 = Trigger(Location=Blacksmith, action=talk)
    t2 = Trigger(Location=Blacksmith, action=buy)
    t3 = Trigger((Location=Blacksmith, action=sell)
While the Quest object would look like
    q1 = Quest(name="Get aquainted with Blacksmith", descript="Talk to blacksmith",
        triggers=[t1], stage=1, next_quests=[q2], past_quests=[])
    q2 = Quest(name="Get aquainted with Blacksmith", descript="Buy or sell an item.",
        triggers=[t2, t3], stage=2, next_quests=[], past_quests=[q1])

A Trigger can have multiple actions. A Quest can have multiple Triggers. Only one needs to be met
to cause the Quest to advance? 
"""

#Response spec
"""
A response object could be:
respose type: do nothing
respose type: update, plus a list of id tags to update and their new values.
This might need to be written in JS.
"""

class Event:
    def __init__(self, arg_dict):
        self.action = arg_dict['action']
        self.location = arg_dict['location']
        self.person = arg_dict['person']
        self.thing = arg_dict['thing']
        

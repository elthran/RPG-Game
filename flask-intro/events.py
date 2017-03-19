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
    
Format
    -use html "value" tag (<button class="command" value="buy?item_name={{ item.name }}">Buy</button>)
    -format should be:
        #generic
        event_action?location=location, location2, {{ page_title }}&&person=person_name&&thing={{ variable }}
        #specific
        buy?location=World, Thornwall, Blacksmith&&person=Steve_The_Blacksmith&&thing="Medium Helmet"
        Note: location=l1, l2 is the same as location=l1,l2
    NOTE: location=url (pathname) of the current page. So you don't need to add that in as it is attached
    automagically.
        
This should be used to create and event object such that:
    >>> event = Event(request.args)
    
    >>> event
    Event<(action: 'buy', location: ['World', 'Thornwall', 'Blacksmith'],
        person: "Steve_The_Blacksmith", thing: "Medium Helmet")>
    >>> event.action
    'buy'

Considering:
    Use the html 'data-*' tag instead of 'value' tag.
    i.e. <a data-trigger="event_action?etc.></a> or <button data-trigger="event_action?etc.></button>
    
    Make location a URL? Sounds kind of awesome really. 

Testing:
    location url is auto-attached to command/event.
    
    
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

class Event:
    def __init__(self, arg_dict):
        self.action = arg_dict['action']
        self.location = arg_dict['location']
        self.person = arg_dict['person']
        self.thing = arg_dict['thing']
        

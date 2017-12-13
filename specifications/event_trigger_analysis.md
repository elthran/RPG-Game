#### CREATION PHASE, PHASE I
_Set up the trigger._
> quests.py
```python
class QuestPath(HandlerMixin):

    # The when the QuestPath is added to the Journal/Hero
    # It is activated .. which activates the trigger of the first quest.
    # Basically it is a 3 or 4 layer fallthrough? to the HandlerMixin?
    def activate(self, hero):
        """Activate a current quest's trigger.

        This is assumed to deactivate the old trigger but I haven't tested
        this.
        """
        super().activate(self.current_quest.trigger, hero)
```
_Move event occurs._
> app.py
```python
def update_current_location(f):
    @wraps(f)
    def wrap_current_location(*args, **kwargs):
        # some other code.
        engine.spawn(
            'move_event',
            hero,
            description="The {} visits {}.".format(hero.name, location.url)
        )
        # some other code.

@app.route('/store/<name>')
@login_required
@uses_hero_and_update
@update_current_location  # spawn happens here!
def store(name, hero=None, location=None):
    pass
```

#### BUILD PHASE, PHASE II
_Move event is built as an object and stored for later (maybe journal)_
> engine.py
```python
def spawn(self, event_name, hero, *args, description=None):
    event = Event(event_name, hero_id=hero.id, description=description)
    self.db.add_object(event)
    self.db.update()
```

#### TRIGGER PHASE, PHASE III
_Test to see if any triggers are in place to handle this event. Note that the trigger must be "pre-built". Set all triggers with valid Conditions to 'completed'_
```python
    triggers = self.db.get_all_triggers_by(event_name, hero.id)
    for trigger in triggers:
        trigger.evaluate()
```

#### HANDLE PHASE, PHASE IV
_This should find all database objects that have completed triggers and run any code they have that is set to run if a trigger completes. This needs some work._
```python
    handlers = self.db.get_all_handlers_with_completed_triggers(hero)
    # return the "Blacksmith" quest object ...
    # Since its completion trigger is completed ...
    # It is now completed. Run the method that you run when trigger
    # completes.
    for handler in handlers:
        handler.run()
```

_I am currently using a Handler parent class. To make this work you need
2 steps:_
```python
class QuestPath(HandlerMixin):
    def run(self):
        """Special handler method over ride.

        In this case run the local 'advance()' method.
        """
        self.advance()
        super().run(self.current_quest.trigger)
```


# NOTE: Templating plays a role here too but it is too complicated to explain right now. :P





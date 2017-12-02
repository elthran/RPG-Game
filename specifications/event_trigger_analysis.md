#### CREATION PHASE, PHASE I
_Move event occurs_
> app.py
```python
@app.route('/store/<name>')
@login_required
@uses_hero_and_update
@update_current_location
def store(name, hero=None, location=None):
    engine.spawn('move_event', hero,
                 description="The {} visits {}.".format(hero.name, name))
```

#### BUILD PHASE, PHASE II
Move event is built as an object and stored for later (maybe journal)
> engine.py
```python
def spawn(self, event_name, hero, *args, description=None):
    event = Event(event_name, hero_id=hero.id, description=description)
    self.db.add_object(event)


    # Test to see if any triggers are in place to handle this event
    # Note that the trigger must be "pre-built".
    # Set all triggers with valid Conditions to 'completed'
    # TRIGGER PHASE, PHASE III
    triggers = self.db.get_all_triggers_by(event_name, hero.id)
    for trigger in triggers:
        trigger.evaluate()


    # This should find all database objects that have completed triggers
    # and run any code they have that is set to run if a trigger completes.
    # This needs some work.
    # HANDLE PHASE, PHASE IV
    handlers = self.db.get_all_handlers_with_completed_triggers(hero)
    # return the "Blacksmith" quest object ...
    # Since its completion trigger is completed ...
    # It is now completed. Run the method that you run when trigger
    # completes.
    for handler in handlers:
        handler.run_handler()

    # When all code has been run, save everything.
    # UPDATE PHASE, PHASE V
    self.db.update()
```

I am currently using a Handler parent class. To make this work you need
2 steps:
```python
class QuestPath(Handler):

    # The when the QuestPath is added to the Journal/Hero
    # It is activated .. which activates the trigger of the first quest.
    # Basically it is a 3 or 4 layer fallthrough? to the HandlerMixin?
    def activate(self, hero):
        """Activate a current quest's trigger.

        This is assumed to deactivate the old trigger but I haven't tested
        this.
        """
        super().activate(
            completion_trigger=self.current_quest.completion_trigger,
            hero=hero
        )

    def run_if_trigger_completed(self):
        """Special handler method over ride.

        In this case run the local 'advance()' method.
        """
        self.advance()
        return None if self.completed \
            else self.current_quest.completion_trigger
```





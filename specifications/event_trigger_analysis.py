# Move event occurs - CREATION PHASE, PHASE I
# app.py
@app.route('/store/<name>')
@login_required
@uses_hero_and_update
@update_current_location
def store(name, hero=None, location=None):
    engine.spawn('move_event', hero, description="The Hero visits a store.")


# Move event is built as an object and stored for later (maybe journal)
# BUILD PHASE, PHASE II
# engine.py
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


"""
I am currently using a Handler parent class. To make this work you need
6 steps:
class QuestPath(Handler):
    id = Column(Integer, ForeignKey('handler.id'), primary_key=True)
    
    # If there is a column override (most common with be hero_id)
    hero_id = column_property(Column(Integer, ForeignKey('hero.id')),
                              Handler.hero_id)
                              
    __mapper_args__ = {
        'polymorphic_identity': 'quest_path',
    }
    
    def __init__(self, etc.)
        super().__init__(completion_trigger=quest.completion_trigger,
                         hero=hero)
    
    def run_if_trigger_completed(self):
        '''Special handler method over ride.

        In this case run the local 'advance()' method.
        '''
        self.advance()
"""



"""
#################
uses Handler decorator?
NOTE: currently only a theory.
I might need to combine decorators and meta-classing?
Here I am trying to decorate a class with a class.
The basic steps are:
    1. add completion trigger to __init__
    2. add link/try except.
    3. add relationship to trigger (back_population my be unneeded)
    4. add run_if_completed code.
    4a. unlink old trigger
    4b. do the thing that the whole party if for (e.g. quest.advance())
    4c. link next trigger if available.
################
"""
class Decorator(object):
    def __init__(self, arg):
        self.arg = arg
        # Add connection to cls init
        completion_trigger = None

        # Make Trigger available!
        # Some kind of linkage between trigger and hero.
        # Instantiated triggers must relate to a specific hero.
        try:
            self.quest.completion_trigger.link(hero)
        except AttributeError as ex:
            print("Warning: The quest with the description '{}' has no "
                  "completion trigger set up.".format(quest.description))
            print('See error "{}"'.format(ex))

    def __call__(self, cls):
        class Wrapped(cls):
            classattr = self.arg

            # Add relationship to cls spec.
            trigger_id = Column(Integer, ForeignKey('trigger.id'))
            completion_trigger = relationship("Trigger",
                                              back_populates='quests')

            # Add generic run if completed method to new class.
            def run_if_trigger_completed(self):
                """Deactivate trigger and run activation code.

                In this case ... unlink the trigger from the given quest
                and the advance the quest to the next stage.

                In theory ... this would bring the new trigger in to play
                through activation of a new quest? Or have I not set that up right?
                """
                self.quest.completion_trigger.unlink()
                self.advance()
                # Make Trigger available!
                try:
                    self.quest.completion_trigger.link(self.hero)
                except AttributeError as ex:
                    print(
                        "Warning: The quest with the description '{}' has no "
                        "completion trigger set up.".format(
                            self.quest.description))
                    print('See error "{}"'.format(ex))

        return Wrapped


@Decorator("decorated class")
class SomeClassThatUsesTriggers:
    pass


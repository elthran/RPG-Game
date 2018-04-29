import sqlalchemy as sa
import sqlalchemy.ext.declarative

from models.events import Handler


class HumanReadableTimeMixin(object):
    @classmethod
    @sa.ext.declarative.declared_attr
    def timestamp(cls):
        return sa.Column(sa.DateTime)

    def human_readable_time(self):
        """Human readable datetime string.

        See https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior

        Currently returns formatted like:
        Jan. 28 1:17pm
        """
        return self.timestamp.strftime("%b. %d %I:%M%p")


class HandlerMixin(object):
    """Handler mixin to adds handler functionality to a class.

    The basic steps are:
        1. add and 'activate' method to sub-class that can be run when a
            hero and trigger are available

    e.g. In quests.py -> QuestPath I have built a journal class validator.
    @validates('journal')
    def activate_path(self, key, journal):
        assert self.template is False
        assert self.handler is None
        self.handler = self.new_handler()
        self.handler.activate(self.current_quest.trigger, journal.hero)
        return journal

        2. Add a run method to the subclass that is a stub to whatever the
        subclass actually does. This method needs to deactivate the handler
        appropriately.

    e.g. In quests.py -> QuestPath
    def advance(self):
        if self.completed:
            raise AssertionError("This path '{}' is completed and should have been deactivated!".format(self.name))

        if self.stage == self.stages-1:
            self.completed = True
            self.reward_hero(final=True)
            self.handler.deactivate()
            self.handler = None
        else:
            self.reward_hero()  # Reward must come before stage increase.
            self.stage += 1
            # Activate the latest trigger. This should deactivate the trigger if 'completed'.
            self.handler.activate(self.current_quest.trigger, self.journal.hero)

    def run(self):
        self.advance()
    """

    # Add relationship to cls spec.
    # noinspection PyMethodParameters
    @sa.ext.declarative.declared_attr
    def handler_id(cls):
        return sa.Column(sa.Integer, sa.ForeignKey('handler.id', ondelete="CASCADE"))

    # The backref here populates the list of handler mixin stubs.
    # noinspection PyUnresolvedReferences
    # noinspection PyMethodParameters
    @sa.ext.declarative.declared_attr
    def handler(cls):
        return sa.orm.relationship(
            "Handler",
            backref=sa.orm.backref(cls.__tablename__, uselist=False, cascade="all, delete-orphan"))

    # noinspection PyUnresolvedReferences
    @property
    def new_handler(self):
        return lambda: Handler(self.__tablename__)

    def run(self):
        raise NotImplementedError("You need to override this on the '{}' class.".format(self.__class__))


class SessionHoistMixin:
    """Hoist the _sa_instance_state.session attribute of this object.

    I have no idea about the side effect of this. There is probably a proper
    way to do this .. that doesn't access a protected member of the class.
    """
    @property
    def session(self):
        return self._sa_instance_state.session

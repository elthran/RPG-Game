import sqlalchemy as sa
import sqlalchemy.ext.declarative


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

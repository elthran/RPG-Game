import datetime


def now():
    """Return current UTC time as datetime object in string form.

    NOTE: I am using UTC as we are working in different time
    zones and I think it might screw up otherwise.
    """
    return datetime.datetime.utcnow()


def timeout_in(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return now() + datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

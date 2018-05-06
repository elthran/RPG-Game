import datetime


def now():
    """Return current UTC time as datetime object in string form.

    NOTE: I am using UTC as we are working in different time
    zones and I think it might screw up otherwise.
    """
    return datetime.datetime.utcnow()

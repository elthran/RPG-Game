import functools


def set_notification_active(f):
    """Tack data onto a response that activates the notification button.

    This is a decorator that will be used to un-hide the
    globalNotificationButton.

    Add the isNotice=true/false into any response.
    If the response is a json type then it adds it to the JSON object
        (at the front, but as this is a dictionary it isn't that important).
    If the response is a string it tacks it on the end as a
        keyword=variable pair.
    """

    @functools.wraps(f)
    def wrap_set_notice_active(hero, *args, **kwargs):
        response = f(hero, *args, **kwargs)
        # print("Using the set notification active code!")
        # notice = str(bool(hero.journal.notification)).lower()
        notice = str(False).lower()  # debugging
        try:
            new_data = b'\n  "isNotice": ' + notice.encode() + b', '
            response.data = b"{" + new_data + response.data[1:]
        except AttributeError:
            # Convert the string from binary.
            response += "&&isNotice={}".format(notice)
        return response
    return wrap_set_notice_active

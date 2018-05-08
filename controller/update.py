import models


def update():
    """Save the all current data.

    This usually will auto-run after each request.
    It calls the models.database.session.save() method.
    The session is committed/flushed/rebuilt.
    """
    models.Base.save()

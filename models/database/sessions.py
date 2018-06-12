from functools import wraps
import contextlib

import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.orm.exc import UnmappedInstanceError

# configure Session class with desired options
Session = sa.orm.sessionmaker()


def scoped_session(f):
    """Provide a transactional scope around a series of operations.

    NOTE: don't use this on any function that returns a database object as
    you will get a detached instance error!
    """

    @wraps(f)
    def wrap_scoped_session(self, *args, **kwargs):
        if self.session:
            old_session = self.session
        self.session = self.Session()
        retval = f(self, *args, **kwargs)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            if old_session:
                self.session = old_session
        if hasattr(retval, '_sa_instance_state'):
            raise Exception("Don't use scoped_session when you are returning a database object!")
        return retval
    return wrap_scoped_session


def safe_commit_session(f):
    """Wrap a commit and rollback in one. Add and commit returned value.

    I don't really know what happens if this crashes and rollsback ..
    is the session clean or corrupt? Does it loose the data?
    I guess it throws and exception .. so maybe that is ok.
    """
    @wraps(f)
    def wrap_safe_commit_session(self, *args, **kwargs):
        retval = f(self, *args, **kwargs)
        try:
            self.session.add(retval)
        except UnmappedInstanceError:
            pass
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return retval

    return wrap_safe_commit_session


def quick_save(self):
    """Wrap a commit and rollback in one.

    Don't clear the session.
    """
    try:
        self.session.commit()
    except:
        self.session.rollback()
        raise


# Seems to build sessions that expire too quickly.
# I'm probably using this wrong.
# noinspection PyPep8Naming
@contextlib.contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def save(self):
    """Commit, handle errors, close the session, open a new one.

    Provide a context manager type behavior for the session.
    See:
    http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """
    try:
        self.session.commit()
    except:
        self.session.rollback()
        raise
    finally:
        self.session.close()
        self.session = self.Session()

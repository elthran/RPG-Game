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

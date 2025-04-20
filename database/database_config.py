from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from .base_models import Base

DATABASE_URI = "sqlite:///University.db"
engine = create_engine(DATABASE_URI, echo=True)  # connect to the database
_SessionFactory = sessionmaker(bind=engine)


def session_factory():
    return _SessionFactory()


def init_db():
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")


@contextmanager
def get_session():
    session = session_factory()
    try:
        yield session              # <-- gives the session to your code
        session.commit()           # <-- commits if no exception occurred
    except:
        session.rollback()         # <-- undoes all changes if there was an error
        raise                      # <-- re-raises the error so you know what happened
    finally:
        session.close()            # <-- always closes the session

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base_models import UserBase, ProjectBase

# GLOBAL DB
USER_DB_URI = "sqlite:///data/user_info.db"

user_engine = create_engine(USER_DB_URI, echo=True)


def init_user_db():
    UserBase.metadata.create_all(user_engine)
    print("GlobalBase and its tables created successfully.")


# PROJECT DB — You can change this dynamically later
def get_project_engine(project_name: str):
    project_path = f"data/{project_name}/database.db"
    return create_engine(f"sqlite:///{project_path}", echo=True)


def init_project_db(project_name: str):
    project_folder = os.path.join("data", project_name)
    os.makedirs(project_folder, exist_ok=True)  # Create folder if missing

    db_path = os.path.join(project_folder, "database.db")
    PROJECT_DB_URI = f"sqlite:///{db_path}"
    project_engine = create_engine(PROJECT_DB_URI, echo=True)

    ProjectBase.metadata.create_all(project_engine)
    print(f"database DB for '{project_name}' created at {db_path}")


# Global SessionFactory
UserSessionFactory = sessionmaker(bind=user_engine)


# Project SessionFactory (dynamic)
def get_project_session_factory(project_name: str):
    project_engine = get_project_engine(project_name)
    return sessionmaker(bind=project_engine)


@contextmanager
def get_session(source: str = "user", project_name: str = None):
    """
    Context manager to get session.
    - source: 'user' or 'database'
    - project_name: required if source is 'database'
    """
    if source == "user":
        session_factory = UserSessionFactory
    elif source == "database":
        if not project_name:
            raise ValueError("project_name is required for project session")
        session_factory = get_project_session_factory(project_name)
    else:
        raise ValueError("Invalid source. Choose 'global' or 'project'.")

    session = session_factory()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

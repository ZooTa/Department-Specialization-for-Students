import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base_models import GlobalBase, ProjectBase

# GLOBAL DB
GLOBAL_DB_URI = "sqlite:///database/global.db"

global_engine = create_engine(GLOBAL_DB_URI, echo=True)


def init_global_db():
    GlobalBase.metadata.create_all(global_engine)
    print("GlobalBase and its tables created successfully.")


# PROJECT DB — You can change this dynamically later
def get_project_engine(project_name: str):
    project_path = f"projects/{project_name}/project.db"
    return create_engine(f"sqlite:///{project_path}", echo=True)


def init_project_db(project_name: str):
    project_folder = os.path.join("projects", project_name)
    os.makedirs(project_folder, exist_ok=True)  # Create folder if missing

    db_path = os.path.join(project_folder, "project.db")
    PROJECT_DB_URI = f"sqlite:///{db_path}"
    project_engine = create_engine(PROJECT_DB_URI, echo=True)

    ProjectBase.metadata.create_all(project_engine)
    print(f"Project DB for '{project_name}' created at {db_path}")


# Global SessionFactory
GlobalSessionFactory = sessionmaker(bind=global_engine)


# Project SessionFactory (dynamic)
def get_project_session_factory(project_name: str):
    project_engine = get_project_engine(project_name)
    return sessionmaker(bind=project_engine)


@contextmanager
def get_session(source: str = "global", project_name: str = None):
    """
    Context manager to get session.
    - source: 'global' or 'project'
    - project_name: required if source is 'project'
    """
    if source == "global":
        session_factory = GlobalSessionFactory
    elif source == "project":
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

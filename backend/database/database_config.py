from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .base_models import UserBase, ProjectBase
import os
BASE_PATH = "../data/"
# GLOBAL DB
USER_DB_URI = "sqlite:///../data/user_info.db"
user_engine = create_engine(USER_DB_URI, echo=True)

def init_user_db():
    """Initialize the global user database."""
    UserBase.metadata.create_all(user_engine)
    print("GlobalBase and its tables created successfully.")

def get_project_engine(project_path: str):
    """Get the SQLAlchemy engine for the project database."""
    db_path = os.path.join(project_path, "database.db")
    return create_engine(f"sqlite:///{db_path}", echo=True)

def init_project_database(project_name: str):
    """Initialize the project database at the specified path."""
    project_path = os.path.join(BASE_PATH, project_name)
    os.makedirs(project_path, exist_ok=True)  # Ensure the project directory exists
    db_path = os.path.join(project_path, "database.db")
    project_engine = create_engine(f"sqlite:///{db_path}", echo=True)

    ProjectBase.metadata.create_all(project_engine)
    print(f"Database for project created at '{db_path}'")


def copy_fixed_tables_to_project(
    university_folder: str,
    project_name: str,
    skip_existing_tables: bool = False,
    clear_existing_data: bool = False
):
    """Copy fixed tables from university DB to project DB."""
    tables_to_copy = ["faculty", "department", "program", "specialization", "subjects_required", "department_head"]
    university_db_path = os.path.join(university_folder, "database.db")

    project_path = os.path.join(BASE_PATH, project_name)
    project_db_path = os.path.join(project_path, "database.db")

    source_engine = create_engine(f"sqlite:///{university_db_path}", echo=True)
    target_engine = create_engine(f"sqlite:///{project_db_path}", echo=True)

    source_metadata = MetaData()
    source_metadata.reflect(bind=source_engine, only=tables_to_copy)

    target_metadata = MetaData()
    target_metadata.reflect(bind=target_engine)

    with source_engine.connect() as source_conn, target_engine.connect() as target_conn:
        for table in source_metadata.sorted_tables:
            table_name = table.name
            if skip_existing_tables and table_name in target_metadata.tables:
                print(f"Skipping '{table_name}' (already exists).")
                continue

            # Create the table in the target if not exists
            table.metadata.create_all(target_engine)

            if clear_existing_data:
                target_conn.execute(table.delete())  # Use table.delete() to clear the table

            # Fetch data and convert each row to a dictionary format
            rows = source_conn.execute(table.select()).fetchall()
            column_names = [column.name for column in table.columns]

            # Convert rows to dictionaries
            rows_to_insert = [dict(zip(column_names, row)) for row in rows]

            if rows_to_insert:
                print(f"Inserting {len(rows_to_insert)} row(s) into '{table_name}'...")
                target_conn.execute(table.insert(), rows_to_insert)

    print("Finished copying selected university tables.")
UserSessionFactory = sessionmaker(bind=user_engine)

def get_project_session_factory(project_path: str):
    """Get session factory for the project database."""
    project_engine = get_project_engine(project_path)
    return sessionmaker(bind=project_engine)

@contextmanager
def get_session(source: str = "user", project_path: str = None):
    """Context manager for obtaining a database session."""
    if source == "user":
        session_factory = UserSessionFactory
    elif source == "database":
        if not project_path:
            raise ValueError("project_path is required for project session")
        session_factory = get_project_session_factory(project_path)
    else:
        raise ValueError("Invalid source. Choose 'user' or 'database'.")

    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

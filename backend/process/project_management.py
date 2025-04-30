# backend/database/process/project_management.py

from ..database.database_config import init_project_database, copy_fixed_tables_to_project


def init_new_project(project_name):
    """Initialize a new project by creating a folder in the base path with the given name."""
    init_project_database(project_name)



def start_new_project_with_university_data(project_name, university_folder):
    """Initialize a new project, copying university data into it."""
    init_new_project(project_name)
    copy_fixed_tables_to_project(
        university_folder=university_folder,
        project_name=project_name,
        # skip_existing_tables=True,
        # clear_existing_data=False
    )


def open_existing_project(project_path):
    """Open an existing project located at the given path."""
    # Initialize the project database if it's not already initialized
    init_project_database(project_path)

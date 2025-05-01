# backend/database/process/project_management.py

from ..database.database_config import init_project_database, copy_fixed_tables_to_project, get_session
from ..services.project_service import ProjectService


def start(operation="existing",
          exist_db_folder=None,
          year=None,
          level=None,
          term=None,
          ptype=None,
          student_file=None,
          prefrence_file=None,
          note=None):

    if operation == "existing":
        # Open an existing project
        init_project_database(exist_db_folder)

    elif operation == "new":
        project_name = f"ClassInfo_{year}_{level}_{term}_{ptype}"

        init_project_database(project_name)

        if exist_db_folder:
            copy_fixed_tables_to_project(
                university_folder=exist_db_folder,
                project_name=project_name,
                # skip_existing_tables=True,
                # clear_existing_data=False
            )

        session = get_session("database", project_name)

        project_service = ProjectService(session)
        project_service.create(
            name=project_name,
            type=ptype,
            excel_file_name=student_file,
            directory=project_name,
            note=note
        )



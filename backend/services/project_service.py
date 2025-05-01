# services/project_service.py

from sqlalchemy.orm import Session
from ..database.models import ProjectInfo

class ProjectService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, type, excel_file_name, directory, note=None):
        new_project = ProjectInfo(
            name=name,
            type=type,
            excel_file_name=excel_file_name,
            directory=directory,
            Note=note
        )
        self.session.add(new_project)
        self.session.commit()
        return new_project

    def get(self, project_id):
        return self.session.get(ProjectInfo, project_id)

    def get_all(self):
        return self.session.query(ProjectInfo).all()

    def update(self, project_id, name=None, type=None, excel_file_name=None, directory=None, note=None):
        project = self.get(project_id)
        if not project:
            print("Project not found.")
            return None

        updated = False

        if name is not None:
            project.name = name
            updated = True
        if type is not None:
            project.type = type
            updated = True
        if excel_file_name is not None:
            project.excel_file_name = excel_file_name
            updated = True
        if directory is not None:
            project.directory = directory
            updated = True
        if note is not None:
            project.Note = note
            updated = True

        if updated:
            self.session.commit()
            print("Project updated successfully.")
        else:
            print("Nothing to update.")

        return project

    def delete(self, project_id):
        project = self.get(project_id)
        if not project:
            print("Project not found.")
            return

        self.session.delete(project)
        self.session.commit()
        return project

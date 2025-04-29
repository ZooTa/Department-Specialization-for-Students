from sqlalchemy.orm import Session
from database.models import Project, ProjectInfo


class ProjectService:
    def __init__(self, project_session: Session, project_info_session: Session):
        self.project_session = project_session
        self.project_info_session = project_info_session

    def create(self, name, type, excel_file_name, directory):
        new_project = Project(
            name=name,
            type=type,
            excel_file_name=excel_file_name,
            directory=directory
        )
        self.project_session.add(new_project)
        self.project_session.flush()  # Assigns ID

        new_info = ProjectInfo(
            id=new_project.id,
            name=name,
            type=type
        )
        self.project_info_session.add(new_info)

        self.project_session.commit()
        self.project_info_session.commit()

        return new_project

    def get(self, project_id):
        return self.project_session.get(Project, project_id)

    def get_all(self):
        return self.project_session.query(Project).all()

    def update(self, project_id, name=None, type=None, excel_file_name=None, directory=None):
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

        if updated:
            self.project_session.commit()
            print("Project updated successfully.")
        else:
            print("Nothing to update.")

        return project

    def delete(self, project_id):
        project = self.get(project_id)
        if not project:
            print("Project not found.")
            return

        # Delete the corresponding ProjectInfo
        project_info = self.project_info_session.get(ProjectInfo, project_id)
        if project_info:
            self.project_info_session.delete(project_info)
            self.project_info_session.commit()

        self.project_session.delete(project)
        self.project_session.commit()
        return project

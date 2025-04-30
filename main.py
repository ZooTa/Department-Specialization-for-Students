# from backend.services.admin_service import AdminService
# from backend.database.database_config import get_session, init_user_db, init_project_db
#
#
#
# # Initialize the database
#
# init_user_db()
# init_project_db("Class 2025")
#
# # Create a session
# with get_session() as session:
#     # Example usage of the session
#     admin_service = AdminService(session)
#
#     # Add a new admin
#     # admin_service.create("Ahmed Hussein", "ramen_goblin", "123", "admin")
#
#     # # Method to set password (hashing)
#     # admin_service.login("ramen_goblin", "123")
#     # print("hi hi \n")
#     # admin_service.login("ramen_goblin", "000")


from backend.process.project_management import (
    init_new_project,
    start_new_project_with_university_data,
    open_existing_project
)
from backend.database.database_config import get_session
from backend.services.faculty_service import FacultyService
import os


# Define project names and paths
new_project_name = "Class 2027"
existing_project_path = "../data/Class 2025"

# # Initialize new project
#
# init_new_project(new_project_name)
#
# project_path = os.path.join("../data/", new_project_name)
#
# with get_session("database", project_path) as session:
#
#     faculity_service = FacultyService(session)
#
#     faculity_service.create("Engineering")


# # Initialize new project with university data

start_new_project_with_university_data(new_project_name, existing_project_path)





# # Initialize new project with university data
# start_new_project_with_university_data(new_project_name, "../data/university")

# Open existing project
# open_existing_project(existing_project_path)
#
# with get_session("database", existing_project_path) as session:
#
#     faculity_service = FacultyService(session)
#
#     faculity_service.create("Engineering")

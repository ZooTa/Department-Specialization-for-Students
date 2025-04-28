
# from database.database_config import get_session, init_global_db, init_project_db
#
# from services.faculty_service import FacultyService
# from services.department_service import DepartmentService


# Initialize the database
# init_db()

# Create a session
# session = session_factory()

# Initialize the FacultyService
# faculty = FacultyService(session)

# Create a new faculty
# faculty_sci = faculty.create("Science")
# faculty_cs = faculty.create("Computer Science")


# delete a faculty
#
# fac1 = faculty.delete(4)
# print("Faculity", fac1.name,  "is Deleted")
#
# # update a faculty
# fac2 = faculty.update(3, "Midicine")
# print("Faculity with id:", fac2.id,  "is updated to", fac2.name)
#
# # Read all faculties
# faculties = faculty.get_all()
#
# print("All faculties:")
# for fac in faculties:
#     print("id:", fac.id, "name:", fac.name)

# session.close()


# with get_session() as session:
#     # Initialize the DepartmentService
#     department_service = DepartmentService(session)
#
#     # Create a new faculty
#     dept1 = department_service.create("IS", 300, 2)
#     dept2 = department_service.create("CS", 500, 2)
#
#     # Update a department
#     dept3 = department_service.update(5, "AI", 80, 2)
#
#     # Delete a department
#     dept4 = department_service.delete(6)
#
#
#     # Read all departments
#     departments = department_service.get_all()
#     print("All departments:")
#     for dept in departments:
#         print("id:", dept.id, "name:", dept.name, "faculty_name:", dept.faculty.name)
































from database.database_config import get_session, init_global_db, init_project_db

from services.faculty_service import FacultyService
from services.department_service import DepartmentService
# Initialize the database

init_global_db()
init_project_db("Class 2025")


# Create a session
with get_session("global") as session:

    # Initialize the FacultyService
    faculty = FacultyService(session)


    # faculty.delete(1)

    # Create a new faculty

    # faculty_sci = faculty.create("Science")
    # faculty_cs = faculty.create("Computer Science")
    # faculty_eng = faculty.create("Engineering")
    # faculty_med = faculty.create("Medicine")

    # # Update a faculty
    # fac2 = faculty.update(3, "Midicine")
    #
    # department_service = DepartmentService(session)
    #
    # # Create a new department
    #
    # dept1 = department_service.create("Mathematics", 300, 1)
    # dept2 = department_service.create("Chemistry", 300, 1)

from services.student_service import StudentService

with get_session("project", "Class 2025") as session:

    # initialize student service
    student_service = StudentService(session)






